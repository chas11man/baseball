from PIL import Image, ImageDraw, ImageFont
import os

class ScoreBox():
    def __init__(self):
        self.image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blank.gif'))
        self.draw = ImageDraw.Draw(self.image)
        self.main()

    def save(self, file_name='test.gif'):
        del self.draw
        self.image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file_name), )

    def _coord(self, x, y, frac):
        div = self.image.size[0]/frac
        return (div*x, div*(frac-y))

    def coord_10(self, x, y):
        return self._coord(x, y, 10)

    def coord_20(self, x, y):
        return self._coord(x, y, 20)

    def get_font(self, size):
        return ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

    def play(self, scoring, base=1):
        if base == 1:
            c = self.coord_20(16,7)
        elif base == 2:
            c = self.coord_20(12,19)
        elif base == 3:
            c = self.coord_20(1,16)
        else:
            c = self.coord_20(5,3)

        font = self.get_font(40)
        self.draw.text(c, str(scoring), font=font)

    def draw_diamond(self):
        self.draw.line([self._coord(0,0,1), self._coord(0,1,1)], width=2)
        self.draw.line([self._coord(0,1,1), self._coord(1,1,1)], width=2)
        self.draw.line([self._coord(1,1,1), self._coord(1,0,1)], width=2)
        self.draw.line([self._coord(1,0,1), self._coord(0,0,1)], width=2)

        self.draw.line([self.coord_10(5,1), self.coord_10(9,5)], width=2, fill=128) # Home - 1st
        self.draw.line([self.coord_10(9,5), self.coord_10(5,9)], width=2, fill=128) #  1st - 2nd
        self.draw.line([self.coord_10(5,9), self.coord_10(1,5)], width=2, fill=128) #  2nd - 3rd
        self.draw.line([self.coord_10(1,5), self.coord_10(5,1)], width=2, fill=128) #  3rd - Home

    def draw_count(self):
        self.draw.line([self.coord_10(7,1), self.coord_10(10,1)], width=2, fill=64)
        self.draw.line([self.coord_10(8,2), self.coord_10(10,2)], width=2, fill=64)
        self.draw.line([self.coord_10(9,0), self.coord_10(9, 2)], width=2, fill=64)
        self.draw.line([self.coord_10(8,0), self.coord_10(8, 2)], width=2, fill=64)
        self.draw.line([self.coord_10(7,0), self.coord_10(7, 1)], width=2, fill=64)

        self.draw.line([self.coord_10(0,2), self.coord_10(2,2)], width=2, fill=64)
        self.draw.line([self.coord_10(2,0), self.coord_10(2,2)], width=2, fill=64)

    def home_first(self, scoring=None):
        self.draw.line([self.coord_10(5,1), self.coord_10(9,5)], width=8)
        if scoring:
            self.play(scoring, 1)

    def first_second(self, scoring=None):
        self.draw.line([self.coord_10(9,5), self.coord_10(5,9)], width=8)
        if scoring:
            self.play(scoring, 2)

    def second_third(self, scoring=None):
        self.draw.line([self.coord_10(5,9), self.coord_10(1,5)], width=8)
        if scoring:
            self.play(scoring, 3)

    def third_home(self, scoring=None):
        self.draw.line([self.coord_10(1,5), self.coord_10(5,1)], width=8)
        if scoring:
            self.play(scoring, 4)

    def score(self):
        self.draw.polygon((self.coord_10(5,1), self.coord_10(9,5), self.coord_10(5,9), self.coord_10(1,5)), fill=100)

    def big_out(self, scoring, num):
        font = self.get_font(80)
        width = font.getsize(scoring)[0]/2
        self.draw.text((self.image.size[0]/2-width,self.image.size[1]*.325), scoring, font=font)
        self.out(num)

    def out(self, num):
        font = self.get_font(50)
        self.draw.text(self.coord_20(1,4), str(num), font=font)

    def out_at_2nd(self, scoring, num):
        self.draw.line([self.coord_10(9,5), self.coord_20(13,15)], width=8)
        self.draw.line([self.coord_10(6,7), self.coord_10(7,8)], width=6)
        self.play(scoring, 2)
        self.out(num)

    def out_at_3rd(self, scoring, num):
        self.draw.line([self.coord_10(5,9), self.coord_20(5,13)], width=8)
        self.draw.line([self.coord_10(2,7), self.coord_10(3,6)], width=6)
        self.play(scoring, 3)
        self.out(num)

    def out_at_home(self, scoring, num):
        self.draw.line([self.coord_10(1,5), self.coord_20(7,5)], width=8)
        self.draw.line([self.coord_10(3,2), self.coord_10(4,3)], width=6)
        self.play(scoring, 4)
        self.out(num)

    def strikes(self, num):
        if num > 2:
            num = 2
        for i in xrange(num):
            self.draw.line([self.coord_10(10-i,1), self.coord_10(9-i,2)], width=2)
            self.draw.line([self.coord_10(9-i,1), self.coord_10(10-i,2)], width=2)

    def balls(self, num):
        if num > 3:
            num = 3
        for i in xrange(num):
            self.draw.line([self.coord_10(10-i,0), self.coord_10(9-i,1)], width=2)
            self.draw.line([self.coord_10(9-i,0), self.coord_10(10-i,1)], width=2)

    def draw_box(self):
        self.draw_diamond()
        self.draw_count()

    def main(self):
        self.draw_box()

if __name__ == '__main__':
    box = ScoreBox()
    box.balls(3)
    box.strikes(2)
    box.home_first('1B')
    box.out_at_2nd('6-4', 1)
    box.save()
