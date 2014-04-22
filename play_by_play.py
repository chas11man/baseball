from datetime import date, timedelta
from draw import baseball
from sets import Set
import xml.etree.ElementTree as ET
import sys
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
	if string == 'first baseman':
		return 3
	elif string == 'third baseman':
		return 5
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

	atbat = game_events_root[0][0][2]
	events = Set()
	for bat in game_events_root.iter('atbat'):
		events.add(bat.attrib['event'])
	print events

	baseball.open_draw()
	baseball.main()
	baseball.strikes(int(atbat.attrib['s']))
	baseball.balls(int(atbat.attrib['b']))

	e = atbat.attrib['event']
	if e == 'Strikeout':
		baseball.big_out('K', int(atbat.attrib['o']))
	elif e == 'Single':
		baseball.home_first('1B')
	elif e == 'Double':
		baseball.home_first()
		baseball.first_second('2B')
	elif e == 'Triple':
		baseball.home_first()
		baseball.first_second()
		baseball.second_third('3B')
	elif e == 'Home Run':
		baseball.home_first()
		baseball.first_second()
		baseball.second_third()
		baseball.third_home('HR')
	elif e == 'Groundout':
		r = re.compile('([A-Za-z\s]+) grounds out, ([a-z\s]+) ([A-Za-z\s]+) to ([a-z\s]+) ([A-Za-z\s]+).*')
		m = r.match(atbat.attrib['des'])
		baseball.big_out('%d-%d' % (pos(m.group(2)), pos(m.group(4))) , int(atbat.attrib['o']))

	baseball.close_draw()