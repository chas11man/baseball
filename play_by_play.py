from datetime import date, timedelta
from draw.baseball import ScoreBox
from sets import Set
import xml.etree.ElementTree as ET
import sys, os
import argparse
import urllib2
import bs4
import re

class Team(object):
	def __init__(self, code, abbrev, id, name, name_full, name_brief):
		self.code = code
		self.abbrev = abbrev
		self.id = id
		self.name = name
		self.name_full = name_full
		self.name_brief = name_brief

class Player(object):
	pass
	#self.id
	#self.num
	#self.boxname
	#self.position
	#self.team

class Play(object):
	pass

class Game(object):
	def __init__(self, home, away, location):
		self.home = home
		self.away = away
		self.location = location

def pos(string):
	if string == 'pitcher':
		return 1
	elif string == 'catcher':
		return 2
	elif string == 'first baseman':
		return 3
	elif string == 'second baseman':
		return 4
	elif string == 'third baseman':
		return 5
	elif string == 'shortstop':
		return 6
	elif string == 'left fielder':
		return 7
	elif string == 'center fielder':
		return 8
	elif string == 'right fielder':
		return 9
	else:
		return 0

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='options')
	yes = date.today()-timedelta(days=1)
	def_team = 'was'
	parser.add_argument('-y', '--year', default=yes.strftime('%Y'), help='Year of game', metavar='Year')
	parser.add_argument('-m', '--month', default=yes.strftime('%m'), help='Month of game', metavar='Month')
	parser.add_argument('-d', '--day', default=yes.strftime('%d'), help='Day of game', metavar='Day')
	parser.add_argument('-t', '--team', default=def_team, help='One of the teams', metavar='Team')

	args = vars(parser.parse_args())
	day_url = 'http://gd2.mlb.com/components/game/mlb/year_%(year)s/month_%(month)s/day_%(day)s/' % args
	day_data = urllib2.urlopen(day_url)
	soup = bs4.BeautifulSoup(day_data)
	game_url = day_url + soup.find_all(text=re.compile(args['team']))[0]
	game_url = game_url.replace(' ', '')

	game_response = urllib2.urlopen(game_url + 'game.xml')
	game_xml = game_response.read()
	game_root = ET.fromstring(game_xml)

	location = game_root.findall('stadium')[0].attrib['location']

	for team in game_root.iter('team'):
		a = team.attrib
		t = Team(a['code'], a['abbrev'], a['id'], a['name'], a['name_full'], a['name_brief'])
		if a['type'] == 'home':
			home = t
		elif a['type'] == 'away':
			away = t
	g = Game(home, away, location)

	game_events_response = urllib2.urlopen(game_url + 'game_events.xml')
	print game_url + 'game_events.xml'
	game_events_xml = game_events_response.read()
	game_events_root = ET.fromstring(game_events_xml)

	boxes = {}

	for inning in game_events_root:
		if inning.tag == 'inning':
			inning_num = int(inning.attrib['num'])
			boxes.update({inning_num: {}})
			for half in inning:
				boxes[inning_num].update({half.tag: {}})
				for atbat in half:
					if atbat.tag == 'atbat':
						boxes[inning_num][half.tag].update({atbat.attrib['num']: ScoreBox()})
						box = boxes[inning_num][half.tag][atbat.attrib['num']]

						box.strikes(int(atbat.attrib['s']))
						box.balls(int(atbat.attrib['b']))

						e = atbat.attrib['event']
						if e == 'Strikeout':
							box.big_out('K', int(atbat.attrib['o']))
						elif e == 'Walk':
							box.home_first('BB')
						elif e == 'Hit By Pitch':
							box.home_first('HBP')
						elif e == 'Single':
							box.home_first('1B')
						elif e == 'Double':
							box.home_first()
							box.first_second('2B')
						elif e == 'Triple':
							box.home_first()
							box.first_second()
							box.second_third('3B')
						elif e == 'Home Run':
							box.home_first()
							box.first_second()
							box.second_third()
							box.third_home('HR')
							box.score()
						elif e == 'Groundout' or e == 'Bunt Groundout':
							r = re.compile('([A-Za-z\s\.]+)( bunt)? grounds out(,| sharply,| softly,) ([a-z\s]+) ([A-Za-z\s\.]+) to ([a-z\s]+) ([A-Za-z\s\.]+).*')
							m = r.match(atbat.attrib['des'])
							if m:
								box.big_out('%d-%d' % (pos(m.group(4)), pos(m.group(6))) , int(atbat.attrib['o']))
							else:
								r = re.compile('([A-Za-z\s\.]+) grounds out( softly)? to ([a-z\s]+) ([A-Za-z\s\.]+).*')
								m = r.match(atbat.attrib['des'])
								if m:
									box.big_out('%dU' % pos(m.group(3)), int(atbat.attrib['o']))
						elif e == 'Flyout':
							r = re.compile('([A-Za-z\s\.]+) flies out to ([a-z\s]+) ([A-Za-z\s\.]+).*')
							m = r.match(atbat.attrib['des'])
							if m:
								box.big_out('F%d' % pos(m.group(2)), int(atbat.attrib['o']))
						elif e == 'Lineout':
							r = re.compile('([A-Za-z\s\.]+) lines out (sharply )?to ([a-z\s]+) ([A-Za-z\s\.]+).*')
							m = r.match(atbat.attrib['des'])
							if m:
								box.big_out('L%d' % pos(m.group(3)), int(atbat.attrib['o']))
						elif e == 'Pop Out':
							r = re.compile('([A-Za-z\s\.]+) pops out( softly)? to ([a-z\s]+) ([A-Za-z\s\.]+).*')
							m = r.match(atbat.attrib['des'])
							if m:
								box.big_out('P%d' % pos(m.group(3)), int(atbat.attrib['o']))
						elif e == 'Field Error':
							r = re.compile('[A-Za-z\s]+ error by ([a-z\s]+) ([A-Za-z\s\.]+).*')
							m = r.match(atbat.attrib['des'])
							if m:
								box.home_first('E%d' % pos(m.group(1)))



	for inn,halves in boxes.items():
		for half,atbats in halves.items():
			for ab,box in atbats.items():

				args.update({'inn': str(inn).zfill(2), 'half': half, 'num': ab.zfill(3), 'home': home.abbrev, 'away': away.abbrev})

				games_dir = 'games'
				day_dir = '%(year)s_%(month)s_%(day)s' % args
				teams_dir = '%(home)s_%(away)s' % args
				image_name = '%(num)s_%(inn)s_%(half)s.bmp' % args

				dir_path = os.path.abspath(os.path.join(games_dir, day_dir, teams_dir))
				file_path = os.path.join(dir_path, image_name)

				if not os.path.exists(dir_path):
					os.makedirs(dir_path)

				print 'saving %s' % file_path

				box.save(file_name=file_path)
