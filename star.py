from turtle import RawTurtle
import math
import time
import sound_module as sm


class Star(RawTurtle):
    def __init__(self, star, brix, ufo):
        super().__init__(star)
        self.last_reflection = time.time()
        self.hideturtle()
        self.penup()
        self.setpos(ufo.pos())
        self.b = brix
        self.u = ufo
        self.shape('star_assets/stars/1/1_1.gif')
        self.fired = True
        self.num_bounces = 0


    @property
    def move(self):
        heading = self.heading()
        if 170 < heading < 181:
            self.seth(170)
        elif 180 < heading < 191:
            self.seth(190)
        self.forward(1)
        return self.check_board()


    def check_board(self):
        star_x = math.floor(self.pos()[0])
        star_y = math.floor(self.pos()[1])
        heading = self.heading()

        # check all bricks for collision
        for each in range(len(self.b)):
            for every in range(len(self.b[each])):
                brick_x, brick_y = self.b[each][every].pos()

                # get pixel exact locations
                diff_x = math.floor(brick_x - star_x)
                diff_y = math.floor(brick_y - star_y)


                # at the edge of a brick?
                if abs(diff_x) <= 41 and not abs(diff_y) == 11:
                    if 0 <= abs(diff_y) <= 11:       # within the height of the brick?
                        if 0 <= heading < 180:              # heading north
                            self.seth((360 - heading)+180)
                        elif 180 <= heading < 360:          # heading south
                            self.seth((360 - heading)+180)
                        elif 270 <= heading < 90:           # heading east
                            self.seth((360 - heading)+180)
                        elif 90 <= heading < 270:           # heading west
                            self.seth((360 - heading)+180)
                        self.last_reflection = time.time()
                        self.num_bounces += 1
                        return each, every, True

                # at top or bottom of brick?
                elif abs(diff_y) <= 11 and not abs(diff_x) == 41:
                    if 0 <= abs(diff_x) <= 41:       # within the height of the brick?
                        if 0 <= heading < 180:              # heading north
                            self.seth(360 - heading)
                        elif 180 <= heading < 360:          # heading south
                            self.seth(360 - heading)
                        elif 270 <= heading < 90:           # heading east
                            self.seth(360 - heading)
                        elif 90 <= heading < 270:           # heading west
                            self.seth(360 - heading)
                        self.last_reflection = time.time()
                        self.num_bounces += 1
                        return each, every, True

                # at the magical buggy corner of a block?
                elif abs(diff_y) <= 11 and abs(diff_x) <= 41:
                    self.seth(heading - 180)
                    self.last_reflection = time.time()
                    self.num_bounces += 1
                    return each, every, True


                # if the star has gone above the bricks, reflect
                if self.pos()[1] > 175:
                    sm.play_ceiling()
                    self.last_reflection = time.time()
                    self.seth(360-heading)
        # left side reflections

        # heading west????
        if star_x <= -400:
            sm.play_left_wall()

            if 90 <= heading <= 180:
                self.seth(180 - heading)  # correct?
            elif 270 > heading > 180:
                self.seth(360 - (heading - 180))
            return -1, -1, False

        # right side reflections

        # heading east????
        elif star_x >= 400:
            sm.play_right_wall()
            if 90 > heading >= 0:
                self.seth(181 - heading)
            elif 270 < heading < 360:
                self.seth(180 + (360 - heading))
            self.last_reflection = time.time()
            return -1, -1, False

        # heading south???
        # is the star heading towards the ufo?
        if 180 < heading < 360 and star_y <= -180:

            # take the coordinates of the ufo
            ux, uy = self.u.pos()

            # is it close to the ufo?
            if abs(star_x - ux) <= 60 and abs(star_y - uy) <= 10:
                diff = star_x - ux
                self.seth((360 - heading) - diff)
                sm.play_random_blip()
                self.last_reflection = time.time()
                self.num_bounces = 0
                return -1, -1, False

        # star went below the ufo!
        if self.pos()[1] <= -300:
            sm.play_dying_sound()
            self.num_bounces = 0
            return -1, -1, True
        return -1, -1, False
