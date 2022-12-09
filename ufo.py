from turtle import RawTurtle
import sound_module as sm


class Ufo(RawTurtle):

    def __init__(self, t):
        super().__init__(t)
        self.hideturtle()
        self.shape('ufo_assets/yoofow7.gif')
        self.penup()
        self.setpos(0, -200)
        self.seth(90)
        self.showturtle()

    def goLeft(self):
        sm.play_ufo_move_head()
        self.seth(180)
        self.forward(10)
        self.check_x()

    def goRight(self):
        sm.play_ufo_move_head()
        self.seth(0)
        self.forward(10)
        self.check_x()


    def check_x(self):
        if self.pos()[0] > 450:
            self.hideturtle()
            self.setx(self.pos()[0]*-1+100)
            self.showturtle()
        elif -450 > self.pos()[0]:
            self.hideturtle()
            self.setx(self.pos()[0]*-1-100)
            self.showturtle()
            sm.play_random_ufo_sound()
