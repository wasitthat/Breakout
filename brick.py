from turtle import RawTurtle
import pygame
from matplotlib import colors
pygame.init()

O1 = ['#b7e4c7', '#95d5b2', '#74c69d', '#52b788', '#40916c']
O2 = ['#03045e', '#023e8a', '#0077b6', '#0096c7', '#00b4d8']
O3 = ['#b7e4c7', '#95d5b2', '#74c69d', '#52b788', '#40916c']
O4 = ['#ff6d00', '#ff7900', '#ff8500', '#ff9100', '#ff9e00']
O5 = ['#ff6d00', '#ff7900', '#ff8500', '#ff9100', '#ff9e00']
C1 = ['#9d4edd', '#7b2cbf', '#5a189a', '#3c096c', '#240046']
C2 = ['#fbba72', '#ca5310', '#bb4d00', '#8f250c', '#691e06']
C3 = ['#ffb600', '#ff9e00', '#ff8500', '#ff6d00', '#ff4800']
C4 = ['#240046', '#3c096c', '#5a189a', '#7b2cbf', '#9d4edd']
C5 = ['#240046', '#3c096c', '#5a189a', '#7b2cbf', '#9d4edd']
OUTLINES = [O1, O2, O3, O4, O5]
COLORS = [C1, C2, C3, C4, C5]



class Brick(RawTurtle):
    def __init__(self, t, n, x, y, i):

        super().__init__(t)
        self.x = x
        self.y = y
        self.i = i

        self.turtlesize(1, 3.857)
        self.hideturtle()
        self.resizemode('user')
        self.shape('square')
        self.penup()
        self.speed(0)
        self.reset_brick(i, n)


    def reset_brick(self, i, n):
        self.setpos(self.x, self.y)
        self.color(COLORS[i][n])
        self.pencolor(OUTLINES[i][n])


    def hit_brick(self, b):
        color_index = COLORS[self.i].index(colors.to_hex(b.color()[1]))
        if colors.to_hex(b.color()[1]) == COLORS[self.i][-1]:  # if that brick is green
            b.hideturtle()  # it disappears
            b.goto(-500, -500)  # and moves off-screen
            return 0
        else:
            b.color(COLORS[self.i][color_index+1])  # set next color
            b.pencolor(OUTLINES[self.i][color_index+1])
            return len(COLORS[0]) - color_index - 1
