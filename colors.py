class Colors:
	dark_grey = (26, 31, 40)
	green = (0, 255, 107)
	red = (251, 50, 40)
	orange = (255, 152, 0)
	yellow = (255, 245, 2)
	purple = (159, 46, 255)
	cyan = (0, 255, 233)
	blue = (0, 83, 255)
	white = (255, 255, 255)
	dark_blue = (44, 44, 127)
	light_blue = (59, 85, 162)

	@classmethod
	def get_cell_colors(cls):
		return [cls.dark_grey, cls.blue, cls.orange, cls.cyan, cls.yellow, cls.green, cls.purple, cls.red]
