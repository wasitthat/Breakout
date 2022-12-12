from tkinter import *
import pygame
from game import Game
import time
from math import floor
import sound_module as sm
pygame.init()
splash_music = pygame.mixer.Sound('sounds/splash.oga')

window = Tk()
game = Game(window)
#game.load_board()
game.make_leaderboard()
normal_score = 500


def run_game():
    sm.play_ready()

    fb_frame = 1
    start_time = time.time()
    num_live_stars = 1

    while game.scoreboard.num_lives > 0:
        game.t.update()
        heading = 36

        # if no audio while no star is out there
        if not pygame.mixer.Channel(5).get_busy() and game.pause:
            sm.play_splash()

        if game.fired:
            if not game.tripleplay:

                # check for tripleplay status
                if game.star.num_bounces >= 10 or game.scoreboard.boost >= 5.0:
                    sm.play_tripleplay()
                    game.tripleplay = True
                    num_live_stars = 3
                    for each in range(len(game.stars)):
                        game.stars[each].setpos(game.stars[0].pos())
                        game.stars[each].seth(game.stars[0].heading()+heading*(each+1))
                        heading *= -1
                        game.stars[each].showturtle()

            fb_frame %= 18
            # fb_frame keeps track of the fireball animation frames
            if fb_frame == 0:
                fb_frame = 1
            # fireball animation timing
            if time.time() - start_time >= .025:
                # set for next frame
                fb_frame += 1
                start_time = time.time()

            if not game.pause:
                for each in game.stars:
                    if each.isvisible():
                        heading = floor(each.heading())

                        # get next animation frame
                        each.shape(f'star_assets/stars/{fb_frame}/{fb_frame}_{heading}.gif')

                        # state indicates whether the fireball is active, rebounded or out of play
                        x, y, state = each.move
                        multiplier = -1
                        if num_live_stars == 1:

                            # enable tripleplay availability
                            game.tripleplay = False

                        # -1 indicates no brick hit, state indicates star out of play
                        if state and x == -1:

                            # if not in tripleplay
                            if num_live_stars == 1:

                                # lose a star
                                game.scoreboard.take_star()
                                each.hideturtle()
                                game.scoreboard.boost = 1.0
                                game.fired = False
                                # game.scoreboard.update_scoreboard(
                                #     game.current_level,
                                #     game.brix[game.current_level-1][0].get_color()[1]
                                # )
                            else:

                                # hide that turtle
                                num_live_stars -= 1
                                each.hideturtle()
                                each.setpos(game.ufo.pos())

                        # if rebounded we have a coordinate we hit a brick
                        elif state and x >= 0:

                            # assign row specific score
                            multiplier = game.brix[x][y].hit_brick(game.brix[x][y])
                            game.scoreboard.increase_score(
                                normal_score + (normal_score * multiplier), multiplier)

                        # 0 means lowermost row, no bonus, just remove it from the board
                        if multiplier == 0:
                            game.num_bricks -= 1

                            # if out of bricks, level up!
                            if game.num_bricks <= 0:
                                game.increase_level()
                                game.fired = False

    if game.scoreboard.num_lives == 0:
        game.game_end(window)


while game.player_continues:
    run_game()
