from PIL import Image, ImageDraw, ImageFont
import sys, os

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

def home_first():
    draw.line([coord_10(5,1), coord_10(9,5)], width=8)

def first_second():
    draw.line([coord_10(9,5), coord_10(5,9)], width=8)

def second_third():
    draw.line([coord_10(5,9), coord_10(1,5)], width=8)

def third_home():
    draw.line([coord_10(1,5), coord_10(5,1)], width=8)

def score():
    draw.polygon((coord_10(5,1), coord_10(9,5), coord_10(5,9), coord_10(1,5)), fill=100)

def big_out(play, num):
    font = get_font(80)
    width = font.getsize(play)[0]/2
    draw.text((image.size[0]/2-width,image.size[1]*.4), play, font=font)
    out(num)

def play(play, base=1):
    if base == 1:
        c = coord_20(16,7)
    elif base == 2:
        c = coord_20(14,17)
    elif base == 3:
        c = coord_20(3,16)
    else:
        c = coord_20(5,3)

    font = get_font(40)
    draw.text(c, str(play), font=font)

def single():
    home_first()
    play('1B', 1)

def double():
    home_first()
    first_second()
    play('2B', 2)

def tripple():
    home_first()
    first_second()
    second_third()
    play('3B', 3)

def home_run():
    home_first()
    first_second()
    second_third()
    third_home()
    score()
    play('HR', 4)

def out(num):
    font = get_font(80)
    draw.text(coord_20(1,4), str(num), font=font)

def out_at_1st(num):
    draw.line([coord_20(10,5), coord_20(13,8)], width=6)
    draw.line([coord_20(12,9), coord_20(14,7)], width=3)

def out_at_2nd(num):
    draw.line([coord_20(15,10), coord_20(12,13)], width=6)
    draw.line([coord_20(11,12), coord_20(13,14)], width=3)

def out_at_3rd(num):
    draw.line([coord_20(10,15), coord_20(7,12)], width=6)
    draw.line([coord_20(8,11), coord_20(6,13)], width=3)

def out_at_home(num):
    draw.line([coord_20(5,10), coord_20(8,7)], width=6)
    draw.line([coord_20(7,6), coord_20(9,8)], width=3)

def strikes(num):
    for i in xrange(num):
        draw.line([coord_10(10-i,1), coord_10(9-i,2)])
        draw.line([coord_10(9-i,1), coord_10(10-i,2)])

def balls(num):
    for i in xrange(num):
        draw.line([coord_10(10-i,0), coord_10(9-i,1)])
        draw.line([coord_10(9-i,0), coord_10(10-i,1)])

def draw_box():
    draw_diamond()
    draw_count()

def main():
    draw_box()

if __name__ == '__main__':
    image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blank.png'))
    draw = ImageDraw.Draw(image)
    main()
    del draw
    image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'test.png'))
