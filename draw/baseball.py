from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import sys

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

def draw_diamond(draw):
    draw.line([coord_4(2,1), coord_4(3,2)], width=4) # Home - 1st
    draw.line([coord_4(3,2), coord_4(2,3)], width=4) #  1st - 2nd
    draw.line([coord_4(2,3), coord_4(1,2)], width=4) #  2nd - 3rd
    draw.line([coord_4(1,2), coord_4(2,1)], width=4) #  3rd - Home

    draw.ellipse(bounding(_coord(19,21,40), _coord(21,19,40)), outline=128)

def draw_count(draw):
    draw.line([coord_10(7,1), coord_10(10,1)], width=4)
    draw.line([coord_10(8,2), coord_10(10,2)], width=4)
    draw.line([coord_10(9,0), coord_10(9, 2)], width=4)
    draw.line([coord_10(8,0), coord_10(8, 2)], width=4)
    draw.line([coord_10(7,0), coord_10(7, 1)], width=4)

    draw.line([coord_10(0,2), coord_10(2,2)], width=4)
    draw.line([coord_10(2,0), coord_10(2,2)], width=4)

    draw.line([coord_10(1,9), coord_10(5,9)], width=4)
    draw.line([coord_10(6,9), coord_10(9,9)], width=4)

    draw.line([coord_10(1,9), coord_10(1,10)], width=4)
    draw.line([coord_10(2,9), coord_10(2,10)], width=4)
    draw.line([coord_10(3,9), coord_10(3,10)], width=4)
    draw.line([coord_10(4,9), coord_10(4,10)], width=4)
    draw.line([coord_10(5,9), coord_10(5,10)], width=4)
    draw.line([coord_10(6,9), coord_10(6,10)], width=4)
    draw.line([coord_10(7,9), coord_10(7,10)], width=4)
    draw.line([coord_10(8,9), coord_10(8,10)], width=4)
    draw.line([coord_10(9,9), coord_10(9,10)], width=4)

def write_bats(draw):
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 25)
    font2 = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 18)
    draw.text(coord_100(11,99), 'HR', font=font)
    draw.text(coord_100(21,99), '3B', font=font)
    draw.text(coord_100(31,99), '2B', font=font)
    draw.text(coord_100(41,99), '1B', font=font)

    draw.text(coord_100(61,99), 'BB', font=font)
    draw.text(coord_100(71,98), 'SAC', font=font2)
    draw.text(coord_100(81,99), 'HP', font=font)

def home_first(draw):
    draw.line([coord_4(2,1), coord_4(3,2)], width=6)

def first_second(draw):
    draw.line([coord_4(3,2), coord_4(2,3)], width=6)

def second_third(draw):
    draw.line([coord_4(2,3), coord_4(1,2)], width=6)

def third_home(draw):
    draw.line([coord_4(1,2), coord_4(2,1)], width=6)

def score(draw):
    draw.polygon((coord_4(2,1), coord_4(3,2), coord_4(2,3), coord_4(1,2)), fill=100)

def single(draw):
    home_first(draw)
    draw.line([coord_10(4,10), coord_10(5,9)])
    draw.line([coord_10(5,10), coord_10(4,9)])

def double(draw):
    home_first(draw)
    first_second(draw)
    draw.line([coord_10(3,10), coord_10(4,9)])
    draw.line([coord_10(4,10), coord_10(3,9)])

def tripple(draw):
    home_first(draw)
    first_second(draw)
    second_third(draw)
    draw.line([coord_10(2,10), coord_10(3,9)])
    draw.line([coord_10(3,10), coord_10(2,9)])

def home_run(draw):
    home_first(draw)
    first_second(draw)
    second_third(draw)
    third_home(draw)
    score(draw)
    draw.line([coord_10(1,10), coord_10(2,9)])
    draw.line([coord_10(2,10), coord_10(1,9)])

def out_at_1st(draw):
    draw.line([coord_20(10,5), coord_20(13,8)], width=6)
    draw.line([coord_20(12,9), coord_20(14,7)], width=3)

def out_at_2nd(draw):
    draw.line([coord_20(15,10), coord_20(12,13)], width=6)
    draw.line([coord_20(11,12), coord_20(13,14)], width=3)

def out_at_3rd(draw):
    draw.line([coord_20(10,15), coord_20(7,12)], width=6)
    draw.line([coord_20(8,11), coord_20(6,13)], width=3)

def out_at_home(draw):
    draw.line([coord_20(5,10), coord_20(8,7)], width=6)
    draw.line([coord_20(7,6), coord_20(9,8)], width=3)

def big_out(draw, play):
    font = ImageFont.truetype('/usr/share/fonts/truetype/freefont/FreeMono.ttf', 100)
    img_w = image.size[0]/2
    width = draw.textsize(play, font=font)[0]/2
    # print draw.textsize(play, font=font)[1]
    draw.text((img_w-width, img_w-50), play, font=font)

def strikes(draw, num):
    for i in xrange(num):
        draw.line([coord_10(10-i,1), coord_10(9-i,2)])
        draw.line([coord_10(9-i,1), coord_10(10-i,2)])

def balls(draw, num):
    for i in xrange(num):
        draw.line([coord_10(10-i,0), coord_10(9-i,1)])
        draw.line([coord_10(9-i,0), coord_10(10-i,1)])

def draw_box(draw):
    draw_diamond(draw)
    draw_count(draw)
    write_bats(draw)

def main(image):
    draw = ImageDraw.Draw(image)
    draw_box(draw)
    big_out(draw, '6-3')
    del draw

if __name__ == '__main__':
    image = Image.open('draw/blank.bmp')
    main(image)
    image = image.convert('RGB')
    image.save('draw/test.bmp')
