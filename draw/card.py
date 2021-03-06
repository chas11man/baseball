from PIL import Image, ImageDraw, ImageFont
import os

class ScoreCard():
    def __init__(self):
        self.image = Image.open(os.path.abspath('blanks/blankCard.gif'))
        self.draw = ImageDraw.Draw(self.image)

        self.lines()
        self.text()

    def save(self, file_name='test'):
        del self.draw
        self.image = self.image.convert('P')
        self.image.save(os.path.abspath('output/' + file_name + '.gif'))

    def get_font(self, name, size):
        return ImageFont.truetype(os.path.abspath('fonts/' + name + '.ttf'), size)

    def coord(self, x, y):
        h = self.image.size[1]
        return (40*x, h-(40*y))

    def dashed(self, coords, width=2):
        dash_px = 10 # dash length in pixels

        sx = coords[0][0] # start_x
        sy = coords[0][1] # start_y
        ex = coords[1][0] # end_x
        ey = coords[1][1] # end_y

        if sy == ey:
            tx = sx # temp_x
            while tx < ex:
                if tx + dash_px > ex:
                    self.draw.line([(tx,sy), (ex,ey)], width=width)
                else:
                    self.draw.line([(tx,sy), (tx+dash_px,ey)], width=width)
                tx += dash_px*2
        elif sx == ex:
            ty = ey # temp_y
            while ty < sy:
                if ty + dash_px > sy:
                    self.draw.line([(sx,ty), (ex,ey)], width=width)
                else:
                    self.draw.line([(sx,ty), (ex,ty+dash_px)], width=width)
                ty += dash_px*2

    def horiz_solid_line(self, y, start=0, end=90):
        self.draw.line([self.coord(start, y), self.coord(end, y)], width=4)

    def horiz_dashed_line(self, y, start=0, end=90):
        self.dashed([self.coord(start, y), self.coord(end, y)], width=4)

    def vert_solid_line(self, x, start=0, end=78):
        self.draw.line([self.coord(x, start), self.coord(x, end)], width=4)

    def lines(self):
        self.horiz_solid_line(75)
        self.horiz_solid_line(74)
        self.horiz_dashed_line(72, end=12)
        self.horiz_dashed_line(70, end=12)
        self.horiz_dashed_line(72, start=78)
        self.horiz_dashed_line(70, start=78)
        self.horiz_solid_line(68)
        self.horiz_dashed_line(66, end=12)
        self.horiz_dashed_line(64, end=12)
        self.horiz_dashed_line(66, start=78)
        self.horiz_dashed_line(64, start=78)
        self.horiz_solid_line(62)
        self.horiz_dashed_line(60, end=12)
        self.horiz_dashed_line(58, end=12)
        self.horiz_dashed_line(60, start=78)
        self.horiz_dashed_line(58, start=78)
        self.horiz_solid_line(56)
        self.horiz_dashed_line(54, end=12)
        self.horiz_dashed_line(52, end=12)
        self.horiz_dashed_line(54, start=78)
        self.horiz_dashed_line(52, start=78)
        self.horiz_solid_line(50)
        self.horiz_dashed_line(48, end=12)
        self.horiz_dashed_line(46, end=12)
        self.horiz_dashed_line(48, start=78)
        self.horiz_dashed_line(46, start=78)
        self.horiz_solid_line(44)
        self.horiz_dashed_line(42, end=12)
        self.horiz_dashed_line(40, end=12)
        self.horiz_dashed_line(42, start=78)
        self.horiz_dashed_line(40, start=78)
        self.horiz_solid_line(38)
        self.horiz_dashed_line(36, end=12)
        self.horiz_dashed_line(34, end=12)
        self.horiz_dashed_line(36, start=78)
        self.horiz_dashed_line(34, start=78)
        self.horiz_solid_line(32)
        self.horiz_dashed_line(30, end=12)
        self.horiz_dashed_line(28, end=12)
        self.horiz_dashed_line(30, start=78)
        self.horiz_dashed_line(28, start=78)
        self.horiz_solid_line(26)
        self.horiz_dashed_line(24, end=12)
        self.horiz_dashed_line(22, end=12)
        self.horiz_dashed_line(24, start=78)
        self.horiz_dashed_line(22, start=78)
        self.horiz_solid_line(20)
        self.horiz_dashed_line(18, end=12)
        self.horiz_dashed_line(16, end=12)
        self.horiz_dashed_line(18, start=78)
        self.horiz_dashed_line(16, start=78)
        self.horiz_solid_line(14)
        self.horiz_solid_line(13, start=6, end=78)
        self.horiz_solid_line(12)

        self.horiz_solid_line(11, end=32)
        self.horiz_solid_line(10, end=32)
        self.horiz_solid_line(8, end=32)
        self.horiz_solid_line(6, end=32)
        self.horiz_solid_line(4, end=32)
        self.horiz_solid_line(2, end=32)

        self.vert_solid_line(2, end=11)
        self.vert_solid_line(10, end=11)
        self.vert_solid_line(12, end=11)
        self.vert_solid_line(14, end=11)
        self.vert_solid_line(16, end=11)
        self.vert_solid_line(18, end=11)
        self.vert_solid_line(20, end=11)
        self.vert_solid_line(22, end=11)
        self.vert_solid_line(24, end=11)
        self.vert_solid_line(26, end=11)
        self.vert_solid_line(28, end=11)
        self.vert_solid_line(30, end=11)
        self.vert_solid_line(32, end=11)

        # Vertical Lines
        self.vert_solid_line(2, start=14, end=75)
        self.vert_solid_line(10, start=14, end=75)
        self.vert_solid_line(12, start=12, end=75)
        self.vert_solid_line(18, start=12, end=75)
        self.vert_solid_line(24, start=12, end=75)
        self.vert_solid_line(30, start=12, end=75)
        self.vert_solid_line(36, start=12, end=75)
        self.vert_solid_line(42, start=12, end=75)
        self.vert_solid_line(48, start=12, end=75)
        self.vert_solid_line(54, start=12, end=75)
        self.vert_solid_line(60, start=12, end=75)
        self.vert_solid_line(66, start=12, end=75)
        self.vert_solid_line(72, start=12, end=75)
        self.vert_solid_line(78, start=12, end=75)
        self.vert_solid_line(80, start=12, end=75)
        self.vert_solid_line(82, start=12, end=75)
        self.vert_solid_line(84, start=12, end=75)
        self.vert_solid_line(86, start=12, end=75)
        self.vert_solid_line(88, start=12, end=75)

        self.vert_solid_line(6, start=12, end=14)
        self.vert_solid_line(9, start=12, end=14)
        self.vert_solid_line(15, start=12, end=14)
        self.vert_solid_line(21, start=12, end=14)
        self.vert_solid_line(27, start=12, end=14)
        self.vert_solid_line(33, start=12, end=14)
        self.vert_solid_line(39, start=12, end=14)
        self.vert_solid_line(45, start=12, end=14)
        self.vert_solid_line(51, start=12, end=14)
        self.vert_solid_line(57, start=12, end=14)
        self.vert_solid_line(63, start=12, end=14)
        self.vert_solid_line(69, start=12, end=14)
        self.vert_solid_line(75, start=12, end=14)

    def boxes(self, year, month, day, home, away, half):
        i = 0
        for filename in sorted(os.listdir(os.path.abspath('games/%s_%s_%s/%s_%s' % (year, month, day, home, away)))):
            if filename[7:10] == half:
                col = int(filename[4:6])
                row = i%9
                x = (col + 1) * 6
                y = 74 - (row * 6)
                name = os.path.abspath('games/%s_%s_%s/%s_%s/%s' % (year, month, day, home, away, filename))
                box = Image.open(name)
                self.image.paste(box, self.coord(x,y))
                i += 1

    def text(self):
        font_big = self.get_font('Slabo', 80)
        font_small = self.get_font('Slabo', 42)

        self.draw.text(self.coord(1,78), 'Team:', font=font_big)

        self.draw.text(self.coord(.5,75.1), '#', font=font_small)
        self.draw.text(self.coord(4.5,75.1), 'Name', font=font_small)
        self.draw.text(self.coord(10.5,75.1), 'P', font=font_small)
        self.draw.text(self.coord(14.5,75.1), '1', font=font_small)
        self.draw.text(self.coord(20.5,75.1), '2', font=font_small)
        self.draw.text(self.coord(26.5,75.1), '3', font=font_small)
        self.draw.text(self.coord(32.5,75.1), '4', font=font_small)
        self.draw.text(self.coord(38.5,75.1), '5', font=font_small)
        self.draw.text(self.coord(44.5,75.1), '6', font=font_small)
        self.draw.text(self.coord(50.5,75.1), '7', font=font_small)
        self.draw.text(self.coord(56.5,75.1), '8', font=font_small)
        self.draw.text(self.coord(62.5,75.1), '9', font=font_small)
        self.draw.text(self.coord(68.5,75.1), '10', font=font_small)
        self.draw.text(self.coord(74.5,75.1), '11', font=font_small)

        self.draw.text(self.coord(78.25,75.1), 'AB', font=font_small)
        self.draw.text(self.coord(80.6,75.1), 'R', font=font_small)
        self.draw.text(self.coord(82.6,75.1), 'H', font=font_small)
        self.draw.text(self.coord(84.1,75.1), 'RBI', font=font_small)
        self.draw.text(self.coord(86.25,75.1), 'BB', font=font_small)
        self.draw.text(self.coord(88.25,75.1), 'SO', font=font_small)

        self.draw.text(self.coord(6.05,14.1), 'RUNS', font=font_small)
        self.draw.text(self.coord(9.3,14.1), 'HITS', font=font_small)
        self.draw.text(self.coord(6.1,13.1), 'ERRS', font=font_small)
        self.draw.text(self.coord(9.4,13.1), 'LOB', font=font_small)

        self.draw.text(self.coord(.5,11.1), '#', font=font_small)
        self.draw.text(self.coord(4,11.1), 'Pitchers', font=font_small)
        self.draw.text(self.coord(10.05,11.1), 'W-L', font=font_small)
        self.draw.text(self.coord(12.6,11.1), 'IP', font=font_small)
        self.draw.text(self.coord(14.3,11.1), 'AB', font=font_small)
        self.draw.text(self.coord(16.6,11.1), 'K', font=font_small)
        self.draw.text(self.coord(18.3,11.1), 'BB', font=font_small)
        self.draw.text(self.coord(20.6,11.1), 'H', font=font_small)
        self.draw.text(self.coord(22.6,11.1), 'R', font=font_small)
        self.draw.text(self.coord(24.3,11.1), 'ER', font=font_small)
        self.draw.text(self.coord(26.2,11.1), 'WP', font=font_small)
        self.draw.text(self.coord(28.3,11.1), 'HP', font=font_small)
        self.draw.text(self.coord(30,11.1), 'BLK', font=font_small)

    def player(self, order, name, number, position):
        if order:
            script = self.get_font('JustAnotherHand', 70)

            y = 79.4 - (float(order) * 6.0)

            self.draw.text(self.coord(0.5, y), number, font=script)
            self.draw.text(self.coord(2.5, y), name, font=script)
            self.draw.text(self.coord(10.5, y), str(position), font=script)

    def teamName(self, name):
        script_big = self.get_font('JustAnotherHand', 80)

        self.draw.text(self.coord(7, 77.5), name, font=script_big)

    def inningTotals(self, inn, runs, hits, errs, lob):
        script_small = self.get_font('JustAnotherHand', 40)

        xa = 7 + (inn * 6)
        xb = 10 + (inn * 6)

        self.draw.text(self.coord(xa, 13.8), runs, font=script_small)
        self.draw.text(self.coord(xb, 13.8), hits, font=script_small)
        self.draw.text(self.coord(xa, 12.8), errs, font=script_small)
        self.draw.text(self.coord(xb, 12.8), lob, font=script_small)

    def batterTotals(self, order, ab, run, hit, rbi, bb, so):
        script = self.get_font('JustAnotherHand', 70)

        y = 79.4 - (float(order) * 6.0)

        self.draw.text(self.coord(78.5, y), ab, font=script)
        self.draw.text(self.coord(80.5, y), run, font=script)
        self.draw.text(self.coord(82.5, y), hit, font=script)
        self.draw.text(self.coord(84.5, y), rbi, font=script)
        self.draw.text(self.coord(86.5, y), bb, font=script)
        self.draw.text(self.coord(88.5, y), so, font=script)

    def pitcherTotals(self, num, decision, ip, ab, so, bb, hits, runs, er, wp, hp, blk):
        script = self.get_font('JustAnotherHand', 70)

        y = 11.4 - (float(num) * 2.0)

        self.draw.text(self.coord(10.5,9.4), decision, font=script)
        self.draw.text(self.coord(12.5,9.4), ip, font=script)
        self.draw.text(self.coord(14.2,9.4), ab, font=script)
        self.draw.text(self.coord(16.2,9.4), so, font=script)
        self.draw.text(self.coord(18.5,9.4), bb, font=script)
        self.draw.text(self.coord(20.5,9.4), hits, font=script)
        self.draw.text(self.coord(22.5,9.4), runs, font=script)
        self.draw.text(self.coord(24.5,9.4), er, font=script)
        self.draw.text(self.coord(26.5,9.4), wp, font=script)
        self.draw.text(self.coord(28.5,9.4), hp, font=script)
        self.draw.text(self.coord(30.5,9.4), blk, font=script)


if __name__ == '__main__':
    card = ScoreCard()
    card.boxes('2014', '08', '24', 'WSH', 'SF', 'bot')
    card.save('card')
