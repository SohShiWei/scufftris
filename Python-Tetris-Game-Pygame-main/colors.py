class Colors:
# Colours
    CREAM = (254, 250, 224)
    LIGHT_CREAM = (254, 252, 235)
    GREEN = (2, 156, 84)
    ORANGE = (245, 91, 27)
    BLUE = (163, 230, 238)
    PURPLE = (217, 199, 249)
    YELLOW = (249, 251, 83)
    PINK = (255, 164, 208)
    GREY = (225, 225, 225)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    @classmethod
    def get_cell_colors(cls):
        return [cls.CREAM, cls.LIGHT_CREAM, cls.GREEN, cls.ORANGE, cls.BLUE, cls.PURPLE, cls.YELLOW, cls.PINK,cls.GREY,cls.BLACK,cls.WHITE]