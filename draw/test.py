from PIL import Image, ImageDraw, ImageFont
import os

def get_font(name, size):
    return ImageFont.truetype(os.path.abspath('fonts/' + name + '.ttf'), size)

def coord(image, x, y):
    h = image.size[1]
    return (40*x, h-(40*y))

if __name__ == '__main__':
    file_name = 'blankCard'
    image = Image.open(os.path.abspath('blanks/blankCard.gif'))
    draw = ImageDraw.Draw(image)

    font_big = get_font('Slabo', 80)
    font_small = get_font('Slabo', 42)
    script = get_font('JustAnotherHand', 14)
    script_big = get_font('JustAnotherHand', 80)

    draw.text(coord(image, 0, 78), 'TITLE', font=font_big)
    draw.text(coord(image, 7, 78), 'Big text header', font=script_big)

    for i in xrange(7):
        draw.text(coord(image, i*2, 70), str(i), font=script)

    del draw
    file_name = 'test'
    image.save(os.path.abspath('output/' + file_name + '.gif'))
