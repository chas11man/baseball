from PIL import Image, ImageDraw, ImageFont
import os

class ScoreCard():
	def __init__(self, file_name):
		self.image = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '%s.gif' % file_name))
		self.draw = ImageDraw.Draw(self.image)

	def save(self, file_name='test'):
		del self.draw
		self.image = self.image.convert('L')
		print self.image.__dict__
		self.image.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), '%s.gif' % file_name), 'gif')

	def get_font(self, name, size):
		return ImageFont.truetype('/usr/share/fonts/truetype/tlwg/%s.ttf' % name, size)

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
		# Horizontal Lines
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

		# Boxes
		i = 0
		for num,filename in enumerate(os.listdir(os.path.join(os.path.dirname(__file__), '..', 'games', '2014_04_30', 'HOU_WSH'))):
			if filename[7:10]=='top':
				col = int(filename[4:6])
				if col == 1:
					i += 1
					row = i%9
					x = (col + 1) * 6
					y = 74 - (row * 6)
					name = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'games', '2014_04_30', 'HOU_WSH', filename))
					box = Image.open(name)
					self.image.paste(box, self.coord(x,y))

	def text(self):
		pass
		# Fonts
		# font_big = self.get_font('Umpush', 80)
		# font_small = self.get_font('Umpush', 42)
		# script = self.get_font('Purisa-Bold', 14)
		# script_big = self.get_font('Purisa-Bold', 80)

		# Text
		# self.draw.text(self.coord(7, 78), 'Nationals', font=script_big)

		# self.draw.text(self.coord(0,93,100), '2', font=script)
		# self.draw.text(self.coord(4,93,100), 'Span', font=script)
		# self.draw.text(self.coord(15,93,100), '8', font=script)

		# self.draw.text(self.coord(0,84,100), '6', font=script)
		# self.draw.text(self.coord(4,84,100), 'Rendon', font=script)
		# self.draw.text(self.coord(15,84,100), '5', font=script)

		# self.draw.text(self.coord(0,75,100), '28', font=script)
		# self.draw.text(self.coord(4,75,100), 'Werth', font=script)
		# self.draw.text(self.coord(15,75,100), '9', font=script)

		# self.draw.text(self.coord(0,66,100), '25', font=script)
		# self.draw.text(self.coord(4,66,100), 'Laroche', font=script)
		# self.draw.text(self.coord(15,66,100), '3', font=script)



		# self.draw.text(self.coord(1,78), 'Team:', font=font_big)

		# self.draw.text(self.coord(.5,75.5), '#', font=font_small)
		# self.draw.text(self.coord(4.5,75.5), 'Name', font=font_small)
		# self.draw.text(self.coord(10.5,75.5), 'P', font=font_small)
		# self.draw.text(self.coord(14.5,75.5), '1', font=font_small)
		# self.draw.text(self.coord(20.5,75.5), '2', font=font_small)
		# self.draw.text(self.coord(26.5,75.5), '3', font=font_small)
		# self.draw.text(self.coord(32.5,75.5), '4', font=font_small)
		# self.draw.text(self.coord(38.5,75.5), '5', font=font_small)
		# self.draw.text(self.coord(44.5,75.5), '6', font=font_small)
		# self.draw.text(self.coord(50.5,75.5), '7', font=font_small)
		# self.draw.text(self.coord(56.5,75.5), '8', font=font_small)
		# self.draw.text(self.coord(62.5,75.5), '9', font=font_small)

if __name__ == '__main__':
	card = ScoreCard('blankCard')
	card.lines()
	card.text()
	card.save('card')
