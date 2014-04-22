from PIL import Image, ImageDraw, ImageFont
import sys, os

global image
global draw

def open_draw():
    global image
    image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blank.png'))
    global draw
    draw = ImageDraw.Draw(image)

def close_draw(file_name='test.png'):
    global draw
    del draw
    image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name))

def _coord(x, y, frac):
    div = image.size[0]/frac
    return (div*x, div*(frac-y))

def coord_4(x, y):
    return _coord(x, y, 4)

def coord_10(x, y):
    return _coord(x, y, 10)

def coord_20(x, y):
    return _coord(x, y, 20)

def coord_100(x, y):
    return _coord(x, y, 100)

def bounding(coord1, coord2):
    return (coord1[0], coord1[1], coord2[0], coord2[1])

def get_font(size):
    return ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', size)

def play(scoring, base=1):
    if base == 1:
        c = coord_20(16,7)
    elif base == 2:
        c = coord_20(12,19)
    elif base == 3:
        c = coord_20(1,16)
    else:
        c = coord_20(5,3)

    font = get_font(40)
    draw.text(c, str(scoring), font=font)

def draw_diamond():
    draw.line([coord_10(5,1), coord_10(9,5)], width=2, fill=128) # Home - 1st
    draw.line([coord_10(9,5), coord_10(5,9)], width=2, fill=128) #  1st - 2nd
    draw.line([coord_10(5,9), coord_10(1,5)], width=2, fill=128) #  2nd - 3rd
    draw.line([coord_10(1,5), coord_10(5,1)], width=2, fill=128) #  3rd - Home

def draw_count():
    draw.line([coord_10(7,1), coord_10(10,1)], width=2, fill=64)
    draw.line([coord_10(8,2), coord_10(10,2)], width=2, fill=64)
    draw.line([coord_10(9,0), coord_10(9, 2)], width=2, fill=64)
    draw.line([coord_10(8,0), coord_10(8, 2)], width=2, fill=64)
    draw.line([coord_10(7,0), coord_10(7, 1)], width=2, fill=64)

    draw.line([coord_10(0,2), coord_10(2,2)], width=2, fill=64)
    draw.line([coord_10(2,0), coord_10(2,2)], width=2, fill=64)

def home_first(scoring=None):
    draw.line([coord_10(5,1), coord_10(9,5)], width=8)
    if scoring:
        play(scoring, 1)

def first_second(scoring=None):
    draw.line([coord_10(9,5), coord_10(5,9)], width=8)
    if scoring:
        play(scoring, 2)

def second_third(scoring=None):
    draw.line([coord_10(5,9), coord_10(1,5)], width=8)
    if scoring:
        play(scoring, 3)

def third_home(scoring=None):
    draw.line([coord_10(1,5), coord_10(5,1)], width=8)
    if scoring:
        play(scoring, 4)

def score():
    draw.polygon((coord_10(5,1), coord_10(9,5), coord_10(5,9), coord_10(1,5)), fill=100)

def big_out(scoring, num):
    font = get_font(80)
    width = font.getsize(scoring)[0]/2
    draw.text((image.size[0]/2-width,image.size[1]*.4), scoring, font=font)
    out(num)

def out(num):
    font = get_font(80)
    draw.text(coord_20(1,4), str(num), font=font)

def out_at_2nd(scoring, num):
    draw.line([coord_10(9,5), coord_20(13,15)], width=8)
    draw.line([coord_10(6,7), coord_10(7,8)], width=6)
    play(scoring, 2)
    out(num)

def out_at_3rd(scoring, num):
    draw.line([coord_10(5,9), coord_20(5,13)], width=8)
    draw.line([coord_10(2,7), coord_10(3,6)], width=6)
    play(scoring, 3)
    out(num)

def out_at_home(scoring, num):
    draw.line([coord_10(1,5), coord_20(7,5)], width=8)
    draw.line([coord_10(3,2), coord_10(4,3)], width=6)
    play(scoring, 4)
    out(num)

def strikes(num):
    if num > 2:
        num = 2
    for i in xrange(num):
        draw.line([coord_10(10-i,1), coord_10(9-i,2)])
        draw.line([coord_10(9-i,1), coord_10(10-i,2)])

def balls(num):
    if num > 3:
        num = 3
    for i in xrange(num):
        draw.line([coord_10(10-i,0), coord_10(9-i,1)])
        draw.line([coord_10(9-i,0), coord_10(10-i,1)])

def draw_box():
    draw_diamond()
    draw_count()

def main():
    draw_box()

if __name__ == '__main__':
    open_draw()
    main()
    close_draw()