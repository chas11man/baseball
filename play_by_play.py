from datetime import date, timedelta
from draw.plays import ScoreBox
import xml.etree.ElementTree as ET
import os
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
    def __init__(self, id, num, box, pos, team, first, last):
        self.id = id
        self.num = num
        self.boxname = box
        self.position = pos
        self.team = team
        self.first = first
        self.last = last

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

def parse_event(atbat, box):
    clean = re.sub(' +', ' ', atbat.attrib['des'])
    split = clean.split()
    events = {}
    start = 0

    for num,i in enumerate(split):
        if '.' in i:
            end = num+1
            event = split[start:end]

            r = re.compile('[A-Z]')
            m = r.match(event[2])

            if event[0] == 'With':
                last = event[2]
            elif m:
                last = event[1] + ' ' + event[2]
            else:
                last = event[1]

            player_id = get_player(last=last).id
            player = boxes[inning_num][half.tag][player_id]
            ab = min(player.keys(), key=lambda x:abs(int(x)-int(atbat.attrib['num'])))
            box = boxes[inning_num][half.tag][player_id][ab]
            events.update({box:event})
            start = end

    batter_num = get_player(id=atbat.attrib['batter']).num
    for box, play in events.iteritems():
        print play
        if 'scores.' in play:
            box.first_second()
            box.second_third()
            box.third_home(batter_num)
            box.score()
        elif '1st.' in play:
            box.home_first('FC')
        elif '2nd.' in play:
            if 'to' in play:
                box.first_second(batter_num)
            elif 'out' in play and 'at' in play:
                box.out_at_2nd('x-x', 'x')
        elif '3rd.' in play:
            if 'to' in play:
                box.first_second()
                box.second_third(batter_num)
            elif 'out' in play and 'at' in play:
                box.out_at_3rd('x-x', 'x')
        elif 'singles' in play:
            box.home_first('1B')
        elif 'doubles' in play:
            box.home_first()
            box.first_second('2B')
        elif 'triples' in play:
            box.home_first()
            box.first_second()
            box.second_third('3B')
        elif 'homers' in play:
            box.home_first()
            box.first_second()
            box.second_third()
            box.third_home('HR')
            box.score()
        elif 'walks.' in play:
            box.home_first('BB')


    e = atbat.attrib['event']
    if e == 'Strikeout':
        box.big_out('K', int(atbat.attrib['o']))
    elif e == 'Hit By Pitch':
        box.home_first('HP')
    elif e == 'Groundout' or e == 'Bunt Groundout':
        r = re.compile('([A-Za-z\s\.]+)( bunt)? grounds out(,| sharply,| softly,) ([a-z\s]+) ([A-Za-z\s\.]+) to ([a-z\s]+) ([A-Za-z\s\.]+)\. ')
        m = r.match(atbat.attrib['des'])
        if m:
            box.big_out('%d-%d' % (pos(m.group(4)), pos(m.group(6))) , int(atbat.attrib['o']))
        else:
            r = re.compile('([A-Za-z\s\.]+) grounds out( softly)? to ([a-z\s]+) ([A-Za-z\s\.]+)\. ')
            m = r.match(atbat.attrib['des'])
            if m:
                box.big_out('%dU' % pos(m.group(3)), int(atbat.attrib['o']))
    elif e == 'Grounded Into DP':
        r = re.compile('([A-Za-z\s\.]+) grounds into a double play, ([a-z\s]+) ([A-Za-z\s\.]+) to ([a-z\s]+) ([A-Za-z\s\.]+) to ([a-z\s]+) ([A-Za-z\s\.]+)\. ')
        m = r.match(atbat.attrib['des'])
        if m:
            box.big_out('%d-%d-%d' % (pos(m.group(2)), pos(m.group(4)), pos(m.group(6))), int(atbat.attrib['o']))
    elif e == 'Flyout':
        r = re.compile('([A-Za-z\s\.]+) flies out to ([a-z\s]+) ([A-Za-z\s\.]+)\. ')
        m = r.match(atbat.attrib['des'])
        if m:
            box.big_out('F%d' % pos(m.group(2)), int(atbat.attrib['o']))
    elif e == 'Lineout':
        r = re.compile('([A-Za-z\s\.]+) lines out (sharply )?to ([a-z\s]+) ([A-Za-z\s\.]+)\. ')
        m = r.match(atbat.attrib['des'])
        if m:
            box.big_out('L%d' % pos(m.group(3)), int(atbat.attrib['o']))
    elif e == 'Pop Out':
        r = re.compile('([A-Za-z\s\.]+) pops out( softly)? to ([a-z\s]+) ([A-Za-z\s\.]+)\. ')
        m = r.match(atbat.attrib['des'])
        if m:
            box.big_out('P%d' % pos(m.group(3)), int(atbat.attrib['o']))
    elif e == 'Field Error':
        r = re.compile('[A-Za-z\s]+ error by ([a-z\s]+) ([A-Za-z\s\.]+)\. ')
        m = r.match(atbat.attrib['des'])
        if m:
            box.home_first('E%d' % pos(m.group(1)))

    # if atbat.attrib['b2'] and atbat.attrib['b2'] != atbat.attrib['batter']:
    #     try:
    #         runner2 = boxes[inning_num][half.tag][atbat.attrib['b2']]
    #         ab = min(runner2.keys(), key=lambda x:abs(int(x)-int(atbat.attrib['num'])))
    #         boxes[inning_num][half.tag][atbat.attrib['b2']][ab].first_second(get_player(id=atbat.attrib['batter']).num)
    #     except KeyError:
    #         pass

    # if atbat.attrib['b3'] and atbat.attrib['b3'] != atbat.attrib['batter']:
    #     try:
    #         runner2 = boxes[inning_num][half.tag][atbat.attrib['b3']]
    #         ab = min(runner2.keys(), key=lambda x:abs(int(x)-int(atbat.attrib['num'])))
    #         boxes[inning_num][half.tag][atbat.attrib['b3']][ab].first_second()
    #         boxes[inning_num][half.tag][atbat.attrib['b3']][ab].second_third(get_player(id=atbat.attrib['batter']).num)
    #     except KeyError:
    #         pass


if __name__ == '__main__':
    base_url = 'http://gd2.mlb.com/components/game/mlb/'

    # year = raw_input("What year?")
    # month = raw_input("What month?")
    # day = raw_input("What day?")
    # day_url = 'http://gd2.mlb.com/components/game/mlb/year_%s/month_%s/day_%s/' % (year, month, day)
    args = {'year': '2014', 'month': '08', 'day': '24'}
    day_url = base_url + 'year_2014/month_08/day_24/'
    soup = bs4.BeautifulSoup(urllib2.urlopen(day_url))

    game_url = day_url + soup.find(href=re.compile('wasmlb')).get('href')

    game_response = urllib2.urlopen(game_url + 'game.xml')
    game_xml = game_response.read()
    game_root = ET.fromstring(game_xml)

    game_events_response = urllib2.urlopen(game_url + 'game_events.xml')
    game_events_xml = game_events_response.read()
    game_events_root = ET.fromstring(game_events_xml)

    players_response = urllib2.urlopen(game_url + 'players.xml')
    players_xml = players_response.read()
    players_root = ET.fromstring(players_xml)

    location = game_root.findall('stadium')[0].attrib['location']
    for team in game_root.iter('team'):
        a = team.attrib
        t = Team(a['code'], a['abbrev'], a['id'], a['name'], a['name_full'], a['name_brief'])
        if a['type'] == 'home':
            home = t
        elif a['type'] == 'away':
            away = t
    g = Game(home, away, location)

    def get_player(id=None, num=None, first=None, last=None):
        for player in players_root.iter('player'):
            a = player.attrib
            if id == a['id'] or num == a['num'] or first == a['first'] or last == a['last']:
                if a['parent_team_id'] == home.id:
                    team = home
                else:
                    team = away
                return Player(a['id'], a['num'], a['boxname'], a['current_position'], team, a['first'], a['last'])

    boxes = {}

    for inning in game_events_root:
        if inning.tag == 'inning':
            inning_num = int(inning.attrib['num'])
            boxes.update({inning_num: {}})
            for half in inning:
                boxes[inning_num].update({half.tag: {}})
                for atbat in half:
                    if atbat.tag == 'atbat':
                        boxes[inning_num][half.tag].update({atbat.attrib['batter']: {}})
                        boxes[inning_num][half.tag][atbat.attrib['batter']].update({atbat.attrib['num']: ScoreBox()})
                        box = boxes[inning_num][half.tag][atbat.attrib['batter']][atbat.attrib['num']]

                        box.strikes(int(atbat.attrib['s']))
                        box.balls(int(atbat.attrib['b']))

                        parse_event(atbat, box)

    for inn,halves in boxes.items():
        for half,batters in halves.items():
            for batter,atbats in batters.items():
                for num,box in atbats.items():
                    args.update({'inn': str(inn).zfill(2), 'half': half, 'num': num.zfill(3), 'home': home.abbrev, 'away': away.abbrev})

                    games_dir = 'games'
                    day_dir = '%(year)s_%(month)s_%(day)s' % args
                    teams_dir = '%(home)s_%(away)s' % args
                    image_name = '%(num)s_%(inn)s_%(half)s.gif' % args

                    dir_path = os.path.abspath(os.path.join(games_dir, day_dir, teams_dir))
                    file_path = os.path.join(dir_path, image_name)

                    if not os.path.exists(dir_path):
                        os.makedirs(dir_path)

                    box.save(file_name=file_path)
