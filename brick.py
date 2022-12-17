from turtle import RawTurtle
import pygame
from matplotlib import colors

pygame.init()

O1 = ['#b7e4c7', '#95d5b2', '#74c69d', '#52b788', '#40916c']
O2 = ['#03045e', '#023e8a', '#0077b6', '#0096c7', '#00b4d8']
O3 = ['#b7e4c7', '#95d5b2', '#74c69d', '#52b788', '#40916c']
O4 = ['#ff6d00', '#ff5400', '#ff0054', '#9e0059', '#390099']
O5 = ['#ff6d00', '#ff7900', '#ff8500', '#ff9100', '#ff9e00']

C1 = ['#9d4edd', '#7b2cbf', '#5a189a', '#3c096c', '#240046']
C2 = ['#ffbd00', '#ff5400', '#ff0054', '#9e0059', '#390099']
C3 = ['#004b23', '#006400', '#007200', '#008000', '#38b000']
C4 = ['#6a0d83', '#ce4993', '#ee5d6c', '#fb9062', '#eeaf61']
C5 = ['#240046', '#3c096c', '#5a189a', '#7b2cbf', '#9d4edd']

OUTLINES = [O1, O2, O3, O4, O5]
COLORS = [C1, C2, C3, C4, C5]


class Brick(RawTurtle):
    def __init__(self, t, n, x, y, i):

        super().__init__(t)
        self.x = x
        self.y = y
        self.i = i
        self.n = n
        self.turtlesize(1, 3.857)
        self.hideturtle()
        self.shape('square')
        self.penup()
        self.speed(0)
        self.reset_brick()

    def get_color(self):
        return self.color()

    def reset_brick(self):
        self.setpos(self.x, self.y)
        self.color(COLORS[self.i][self.n])
        self.pencolor(OUTLINES[self.i][self.n])
        self.pensize(2000)

    def hit_brick(self, b):
        color_index = COLORS[self.i].index(colors.to_hex(b.color()[1]))
        if colors.to_hex(b.color()[1]) == COLORS[self.i][-1]:  # if that brick is green
            b.hideturtle()  # it disappears
            b.goto(-500, -500)  # and moves off-screen
            return 0
        else:
            b.color(COLORS[self.i][color_index + 1])  # set next color
            b.pencolor(OUTLINES[self.i][color_index + 1])
            return len(COLORS[0]) - color_index - 1
