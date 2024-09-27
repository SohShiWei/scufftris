class Colors:
	dark_grey = (26, 31, 40)
	green = "#00ff6b"
	red = "#fb3228"
	orange = "#ff9800"
	yellow = "#fff502"
	purple = "#9f2eff"
	cyan = "#00ffe9"
	blue = "#0053ff"
	white = (255, 255, 255)
	dark_blue = (44, 44, 127)
	light_blue = (59, 85, 162)

	@classmethod
	def get_cell_colors(cls):
		return [cls.dark_grey, cls.blue, cls.orange, cls.cyan, cls.yellow, cls.green, cls.purple, cls.red]
