import pygame


class Tree(object):
    def __init__(self, x, y, size, colour, colour_value, timer, timer_displace, leaf_colour, type, leaf_displace=None):
        self.x = x
        self.y = y
        self.size = size
        self.colour = colour
        self.colour_value = colour_value
        self.timer = timer
        self.timer_displace = timer_displace
        self.is_grounded = False
        self.leaf_colour = leaf_colour
        self.type = type
        self.leaf_displace = leaf_displace
        self.touching = False


class Ground(object):
    def __init__(self, x, y, height, width, colour):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.colour = colour

    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height))
