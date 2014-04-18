"""
MLB Gameday Info
"""
import MySQLdb
import urllib2
import xlrd
import xml.etree.ElementTree as ET
from xlrd import open_workbook
from xlutils.copy import copy

def _getOutCell(outSheet, colIndex, rowIndex):
    row = outSheet._Worksheet__rows.get(rowIndex)
    if not row:
        return None
    cell = row._Row__cells.get(colIndex)
    return cell

def setOutCell(outSheet, col, row, value):
    previousCell = _getOutCell(outSheet, col, row)
    outSheet.write(row, col, value)
    if previousCell:
        newCell = _getOutCell(outSheet, col, row)
        if newCell:
            newCell.xf_idx = previousCell.xf_idx

def db_querry(querry):
    database = MySQLdb.connect(host="localhost",
                         user="root",
                         passwd="chasman",
                         db="gameday")
    cursor = database.cursor()
    cursor.execute(querry)
    return cursor.fetchall()

def get_lineup():
    response = urllib2.urlopen('http://gd2.mlb.com/components/game/mlb/year_2014/month_04/day_14/gid_2014_04_14_wasmlb_miamlb_1/players.xml')
    xml = response.read()
    root = ET.fromstring(xml)
    return root

def get_plays():
    return db_querry("""
                select * from gameday.atbat as atbat
                inner join (
                    select game_id from gameday.game
                    where away_team_code="was"
                    or home_team_code="was"
                ) as game
                on atbat.game_id=game.game_id;
            """)

def init_data():
    in_book = xlrd.open_workbook('test_score_sheet.xls', formatting_info=True)
    workbook = copy(in_book)
    sheets = [workbook.get_sheet(0), workbook.get_sheet(1)]

    game = get_lineup()
    for sheet in sheets:
        venue = game.attrib['venue']
        setOutCell(sheet, 11, 0, venue)
        date = game.attrib['date']
        setOutCell(sheet, 7, 2, date)

    for child in game:
        if child.tag == 'team':
            team_name = child.attrib['name']
            team_type = child.attrib['type']
            if team_type == 'home':
                i = 0
                setOutCell(sheets[1], 7, 0, team_name)
            else:
                i = 1
                setOutCell(sheets[0], 7, 0, team_name)

            setOutCell(sheets[i], 2, 0, team_name)

            for player in child:
                try:
                    order = (int(player.attrib['bat_order']) * 2) + 2
                    num = player.attrib['num']
                    setOutCell(sheets[i], 0, order, num)
                    name = player.attrib['boxname']
                    setOutCell(sheets[i], 1, order, name)
                    pos = player.attrib['current_position']
                    setOutCell(sheets[i], 2, order, pos)
                    player_id = player.attrib['id']

                except KeyError:
                    pass
        elif child.tag == 'umpires':
            for umpire in child:
                if umpire.attrib['position'] == 'home':
                    setOutCell(sheets[0], 2, 2, umpire.attrib['name'])
                    setOutCell(sheets[1], 2, 2, umpire.attrib['name'])

    sheets[1].insert_bitmap('draw/test.bmp', 4, 3)
    workbook.save('simple.xls')

def count_at_bats(player_id):
    return db_querry("""select count(batter)
                        from gameday.atbat as atbat
                        inner join (
                            select game_id
                            from gameday.game
                            where away_team_code="was"
                            or home_team_code="was") as game
                        on atbat.game_id=game.game_id
                        where batter="%s"
                        group by batter;""" % (player_id))

if __name__ == "__main__":
    init_data()
