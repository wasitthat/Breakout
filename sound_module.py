import pygame
import random

pygame.init()

# -------Channels-------- #
bucket_channel = 5
star_channel = 7

# -------Brix Sounds------- #

brick1 = pygame.mixer.Sound('sounds/brix/b1.oga')
brick2 = pygame.mixer.Sound('sounds/brix/b2.oga')
brick3 = pygame.mixer.Sound('sounds/brix/b3.oga')
brick4 = pygame.mixer.Sound('sounds/brix/b4.oga')
brick5 = pygame.mixer.Sound('sounds/brix/1.oga')
brix_sounds = [brick5, brick1, brick2, brick3, brick4]


# -------UFO Sounds-------- #
death = pygame.mixer.Sound('sounds/death.oga')
death.set_volume(.2)
ufo_move_head = pygame.mixer.Sound('sounds/ufo/ufo_move_head.oga')
ufo_move_tail = pygame.mixer.Sound('sounds/ufo/ufo_move_tail.oga')
fire1 = pygame.mixer.Sound('sounds/fire/fire1.oga')
fire2 = pygame.mixer.Sound('sounds/fire/fire2.oga')
fire3 = pygame.mixer.Sound('sounds/fire/fire3.oga')
warp1 = pygame.mixer.Sound('sounds/warps/warp1.oga')
warp2 = pygame.mixer.Sound('sounds/warps/warp2.oga')
warp3 = pygame.mixer.Sound('sounds/warps/warp3.oga')
warp4 = pygame.mixer.Sound('sounds/warps/warp4.oga')
warp5 = pygame.mixer.Sound('sounds/warps/warp5.oga')
warp6 = pygame.mixer.Sound('sounds/warps/warp6.oga')
warp7 = pygame.mixer.Sound('sounds/warps/warp7.oga')
fire_sounds = [fire1, fire2, fire3]
warp_sounds = [
    warp1,
    warp2,
    warp3,
    warp4,
    warp5,
    warp6,
    warp7
]

# -------Assorted Game Sounds------- #

splash_music = pygame.mixer.Sound('sounds/splash.oga')
begin = pygame.mixer.Sound('sounds/voice/begin.oga')
over = pygame.mixer.Sound('sounds/voice/over.oga')
new_game = pygame.mixer.Sound('sounds/new_game.oga')
new_game.set_volume(.2)
ready = pygame.mixer.Sound('sounds/voice/ready.oga')
over.set_volume(1.5)
tripleplay = pygame.mixer.Sound('sounds/voice/tripleplay.oga')



# -------Star Sounds------- #
blip1 = pygame.mixer.Sound('sounds/ufo/blips/1.oga')
blip2 = pygame.mixer.Sound('sounds/ufo/blips/2.oga')
blip3 = pygame.mixer.Sound('sounds/ufo/blips/3.oga')
blip4 = pygame.mixer.Sound('sounds/ufo/blips/4.oga')
blip5 = pygame.mixer.Sound('sounds/ufo/blips/5.oga')
blip6 = pygame.mixer.Sound('sounds/ufo/blips/6.oga')
blip7 = pygame.mixer.Sound('sounds/ufo/blips/7.oga')
blip8 = pygame.mixer.Sound('sounds/ufo/blips/8.oga')
blips = [blip1, blip2, blip3, blip4, blip5, blip6, blip7, blip8]


# --------Wall Sounds------- #
lw1 = pygame.mixer.Sound('sounds/walls/left_wall/1.oga')
lw2 = pygame.mixer.Sound('sounds/walls/left_wall/2.oga')
lw3 = pygame.mixer.Sound('sounds/walls/left_wall/3.oga')
lw = [lw1, lw2, lw3]
rw1 = pygame.mixer.Sound('sounds/walls/right_wall/1.oga')
rw2 = pygame.mixer.Sound('sounds/walls/right_wall/2.oga')
rw3 = pygame.mixer.Sound('sounds/walls/right_wall/3.oga')
rw = [rw1, rw2, rw3]
ce2 = pygame.mixer.Sound('sounds/walls/ceiling/3.oga')
ce1 = pygame.mixer.Sound('sounds/walls/ceiling/1.oga')
ce3 = pygame.mixer.Sound('sounds/walls/ceiling/2.oga')
ce = [ce1, ce2, ce3]


def play_ready():
    pygame.mixer.Channel(6).play(ready)


def play_tripleplay():
    pygame.mixer.Channel(7).play(tripleplay)


def play_brick(b):
    pygame.mixer.Channel(b).play(brix_sounds[b - 1])


def play_ufo_move_head():
    if not pygame.mixer.Channel(6).get_busy():
        pygame.mixer.Channel(6).play(ufo_move_head)


def play_ufo_move_tail():
    pygame.mixer.Channel(6).stop()
    pygame.mixer.Channel(6).play(ufo_move_tail)


def play_random_ufo_sound():
    pygame.mixer.Channel(5).play(random.choice(warp_sounds))


def play_ceiling():
    pygame.mixer.Channel(bucket_channel).play(ce[0])


def play_left_wall():
    pygame.mixer.Channel(star_channel).play(lw[0])


def play_right_wall():
    pygame.mixer.Channel(star_channel).play(rw[0])


def play_random_blip():
    pygame.mixer.Channel(star_channel).play(random.choice(blips))


def play_dying_sound():
    pygame.mixer.Channel(bucket_channel).stop()
    pygame.mixer.Channel(bucket_channel).play(death)


def play_splash():
    pygame.mixer.Channel(5).play(splash_music)


def play_fire():
    pygame.mixer.Channel(7).play(random.choice(fire_sounds))


def play_new_game():
    pygame.mixer.Channel(5).stop()
    pygame.mixer.Channel(5).play(new_game)


def play_begin():
    pygame.mixer.Channel(7).play(begin)


def play_over():
    pygame.mixer.Channel(7).play(over)
