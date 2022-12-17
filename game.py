import operator
import time
import random
from tkinter import *
from turtle import *
from PIL import Image, ImageTk, ImageDraw, ImageFont
import PIL
import brick
from scoreboard import ScoreBoard
from star import Star
from ufo import Ufo
from brick import Brick
import sound_module as sm

NUMBER_OF_LIVES = 3
WINDOW_SIZE = (1000, 800)
LOGO_SIZE = (600, 280)
WIN_X = WINDOW_SIZE[0]
WIN_Y = WINDOW_SIZE[1]
NUM_STARS = 3
NUM_COLS = 8
NUM_ROWS = len(brick.COLORS[0])
NUM_BRICKS = NUM_ROWS * NUM_COLS
HELP_W = 600
HELP_H = 424


def hex_to_rgba(hexa, alpha):
    rgb = []
    for i in (1, 3, 5):
        decimal = int(hexa[i:i + 2], 16)
        rgb.append(decimal)
    rgb.append(int(alpha / .39))
    return tuple(rgb)


def imageToPhotoImage(filepath, w, h):
    img = Image.open(filepath)
    img = img.resize((w, h))
    return ImageTk.PhotoImage(img)


class Game:
    def __init__(self, root):
        root.resizable(False, False)
        root.title('Breakout 2.0')
        sm.play_splash()

        # -------Class Globals--------- #

        self.player_continues = True
        self.pause = False
        self.brix = []
        self.num_bricks = NUM_BRICKS
        self.now = time.time()
        self.fired = False
        self.first_fire = True
        self.helped = False
        self.name = StringVar()
        self.led = False
        self.stars = []
        self.tripleplay = False
        self.current_level = 1

        # --------Main Window------- #

        self.screen = Frame(
            root,
            width=WIN_X,
            height=WIN_Y,
            borderwidth=0,
            border=0
        )
        self.screen.grid()

        # --------Logo and Background Image-------- #

        self.logoImg = Image.open('screen_assets/5321941.png')  # load logo
        self.logoImg = self.logoImg.resize(LOGO_SIZE)  # resize
        self.bgImg = Image.open('screen_assets/back.png')  # background image
        self.bgImg = self.bgImg.resize(WINDOW_SIZE)  # resize
        self.mask = Image.new(  # transparent layer setup
            mode='RGBA',
            size=WINDOW_SIZE,
            color='white'
        )
        self.mask.paste(  # paste background
            self.bgImg,
            (0, 0)
        )
        self.mask.paste(  # paste logo
            self.logoImg,
            (int((WIN_X - LOGO_SIZE[0]) / 2), -40),
            self.logoImg
        )
        self.mask = ImageTk.PhotoImage(self.mask)  # convert layer to image
        self.label = Label(  # load label with image
            self.screen,
            width=WIN_X,
            height=WIN_Y,
            image=self.mask,
            borderwidth=0,
            border=0
        )
        self.label.image = self.mask  # make sure
        self.label.grid(  # put it down
            column=0,
            row=0,
            columnspan=3,
            rowspan=9
        )

        # -------Copyright-------- #

        self.copyright = Label(
            self.screen,
            text='\u00A9 John Oden 2022',
            bg='#000000',
            fg='#7777ff'
        )
        self.copyright.grid(
            column=1,
            row=8
        )

        # -------Loading Screen------- #

        self.loadingImg = imageToPhotoImage('screen_assets/loading/1.png', 250, 120)
        self.loadingScreen = Label(root, image=self.loadingImg, background='#000000')
        self.loadingScreen.grid(column=0, row=0)

        # --------Game Screen------- #

        self.game_screen = Canvas(
            self.screen,
            height=600,
            width=800,
            bg='#000000',
            borderwidth=0,
            border=0
        )

        # --------Load Game Screen to TurtleScreen------- #

        self.t = TurtleScreen(self.game_screen)
        self.t.listen()
        self.t.register_shape("ufo_assets/yoofow7.gif")

        # -------Brick Location Data-------- #

        self.start_x = (-WIN_X / 2) + 192
        self.start_y = 100
        self.pause_bit = 0
        self.brick_x = 81
        self.brick_y = 21
        self.horiz_gap = 7

        # --------Pause Button-------- #

        self.pauseImg2 = imageToPhotoImage('screen_assets/paused2.png', 200, 200)
        self.pauseButton = Button(
            root,
            image=self.pauseImg2,
            bg='#000000',
            command=self.pause_game,
            borderwidth=0,
            border=0
        )
        self.pauseButton.image = self.pauseImg2  # make sure

        # --------Yes Button-------- #

        self.yesImg = imageToPhotoImage('screen_assets/again.png', 120, 120)
        self.yes = Button(
            root,
            width=120,
            height=120,
            image=self.yesImg,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.restart(root)
        )

        # --------No Button-------- #

        self.noImg = imageToPhotoImage('screen_assets/exit.png', 120, 120)
        self.no = Button(
            root,
            width=120,
            height=120,
            image=self.noImg,
            borderwidth=0,
            highlightthickness=0,
            highlightcolor="#000000",
            command=self.quit_game
        )

        # --------Available Shapes for Turtles-------- #

        for i in range(1, 19):
            for j in range(360):
                self.t.register_shape(f'star_assets/stars/{i}/{i}_{j}.gif')

        # -------Class Instances------- #
        self.ufo = Ufo(self.t)

        # --------Stars-------- #
        for s in range(NUM_STARS):
            self.stars.append(Star(self.t, self.brix, self.ufo))
            self.stars[s].hideturtle()
            self.stars[s].setpos(self.ufo.pos())
        self.star = self.stars[0]
        self.load_board()

        # -------Play Button------- #

        self.playImg = imageToPhotoImage('screen_assets/play.png', 250, 120)
        self.scoreboard = ScoreBoard(
            self.t,
            NUMBER_OF_LIVES,
            self.current_level,
            self.brix[self.current_level - 1][0].get_color()
        )
        self.playButton = Button(
            self.screen,
            image=self.playImg,
            bg='#000000',
            command=lambda: self.play_game(root),
            borderwidth=0,
            border=0
        )
        self.playButton.image = self.playImg
        self.loadingScreen.grid_forget()
        self.playButton.grid(column=1, row=4)

        # -------KeyBindings------- #

        root.bind('<F1>', lambda e: self.show_help())
        root.bind('<F5>', lambda e: self.restart(root))
        root.bind('<F2>', lambda e: self.show_leaderboard(root))
        root.bind('<Return>', lambda e: self.playButton.invoke())

        # --------Name Entry Image-------- #

        self.nameImg = imageToPhotoImage('screen_assets/name.png', HELP_W, HELP_H)
        self.nameLbl = Label(
            root,
            image=self.nameImg,
            width=HELP_W,
            height=HELP_H,
            borderwidth=0,
            border=0,
        )
        self.nameLbl.image = self.nameImg
        self.nameEntry = Entry(
            root,
            font='Impact 20',
            justify='center',
            bg='#240046',
            fg='#ff9e00'
        )

        # --------Submit Button-------#

        self.submitImg = imageToPhotoImage('screen_assets/submit.png', 250, 97)
        self.submitBtn = Button(
            root,
            text='submit',
            image=self.submitImg,
            command=self.submit,
            borderwidth=0,
            border=0,
            bg="#000000"
        )
        self.submitBtn.image = self.submitImg

        # --------Help Image------- #

        self.helpImg = imageToPhotoImage('screen_assets/help4.png', HELP_W, HELP_H)
        self.helpLbl = Label(
            root,
            image=self.helpImg,
            width=600,
            height=424,
            borderwidth=0,
            border=0
        )

        # --------LeaderBoard------- #

        self.font = ImageFont.truetype('times', 18)
        self.leaderImg = PIL.Image.open('screen_assets/high.png').convert('RGBA')
        self.leaderImg.thumbnail((HELP_W, HELP_H))
        self.leaderMask = Image.new('RGBA', (HELP_W, HELP_H))
        self.mdr = ImageDraw.Draw(self.leaderMask)
        self.fill = '#FFFFFF'
        self.leaderLbl = Label(
            root,
            width=HELP_W,
            height=HELP_H,
            background='#ffffff'
        )

    # ======================================== #
    #                  methods                 #
    # ======================================== #

    def initializeGameScreen(self):

        pass

    def make_leaderboard(self):
        scores = self.scoreboard.get_scores()
        scores = sorted(scores.items(), key=operator.itemgetter(1), reverse=True)
        w = 132
        txt = "{:,}"
        self.leaderMask = Image.new('RGBA', (HELP_W, HELP_H))
        self.mdr = ImageDraw.Draw(self.leaderMask)
        for each in scores:
            self.mdr.text(
                xy=((HELP_H / 2) - (self.font.getsize(each[0] + ' - ' + txt.format(each[1]))[0] / 2) + 85, w),
                text=f"{each[0]} - {txt.format(each[1])}",
                fill=f"#b7e4c7ff",
                font=self.font,
                stroke_fill=f"#ffffff00",
                # stroke_width=1
            )
            w += 28

    # --------Show Leaderboard-------- #

    def show_leaderboard(self, root):
        if self.led:
            self.led = False
            self.pause = False
            self.leaderLbl.grid_forget()
            root.bind('<F1>', lambda e: self.show_help())
            root.bind('<F5>', lambda e: self.restart(root))
            root.bind('<Return>', lambda e: self.playButton.invoke())

        else:
            self.led = True
            self.pause = True
            self.make_leaderboard()
            self.leaderImg.paste(self.leaderMask, (0, 0), self.leaderMask)

            img = ImageTk.PhotoImage(self.leaderImg)
            self.leaderLbl.config(image=img)
            self.leaderLbl.image = img
            self.leaderLbl.grid(column=0, row=0)
            root.unbind('<F1>')
            root.unbind('<F5>')
            root.unbind('<Return>')
            self.screen.update()

    # -------Restart--------- #

    def restart(self, root):
        root.bind('<Left>', lambda e: self.ufo.goLeft())
        root.bind('<Right>', lambda e: self.ufo.goRight())
        root.bind('<space>', lambda e: self.fire())
        root.bind('<Escape>', lambda e: self.pauseButton.invoke())
        root.bind('<Return>', lambda e: self.playButton.invoke())

        self.scoreboard.start_time = time.time()
        self.scoreboard.penup()
        self.scoreboard.boost = 1.0
        self.scoreboard.hideturtle()
        self.scoreboard.num_lives = 3
        self.scoreboard.current_score = 0
        self.current_level = 1
        for each in range(NUM_ROWS):
            for every in self.brix[each]:
                every.i = 0
                every.reset_brick()
        self.scoreboard.update_scoreboard(
            self.current_level,
            self.brix[self.current_level - 1][0].get_color()
        )

        for each in self.stars:
            each.hideturtle()
            each.setpos(self.ufo.pos())

        self.name.set('')
        self.num_bricks = 40
        self.fired = False
        self.first_fire = True
        self.yes.grid_forget()
        self.no.grid_forget()
        self.play_game(root)

    def get_leaderImg(self):
        return self.leaderImg

    # --------Submit Name-------- #

    def submit(self):
        self.name.set(self.nameEntry.get())

        self.scoreboard.check_leaderboard(self.name.get())
        self.scoreboard.update_scoreboard(self.current_level, self.brix[self.current_level - 1][0].get_color())

        sm.play_fire()

    # --------Quit Game-------- #

    def quit_game(self):
        self.player_continues = False
        return

    # --------Show Help Screen------- #

    def show_help(self):
        if self.helped:
            self.helpLbl.grid_forget()
            self.helped = False
            self.pause = False
        else:
            self.helpLbl.grid(column=0, row=0, pady=(50, 0))
            self.helped = True
            self.pause = True
            sm.play_fire()

    # --------Load Board-------- #

    def load_board(self):
        self.t.tracer(0, 0)
        for n in range(NUM_ROWS):
            col = []
            for j in range(NUM_COLS):
                x = self.start_x + (j * self.brick_x) + (j * self.horiz_gap)
                y = self.start_y - (n * self.horiz_gap) - (self.brick_y * n)
                b = Brick(self.t, n, x, y, self.current_level - 1)
                col.append(b)
            self.brix.append(col)
        self.t.tracer(1)

    # --------Play--------- #

    def play_game(self, root):
        root.bind('<Left>', lambda e: self.ufo.goLeft())
        root.bind('<Right>', lambda e: self.ufo.goRight())
        root.bind('<space>', lambda e: self.fire())
        root.bind('<Escape>', lambda e: self.pauseButton.invoke())
        root.bind('<KeyRelease-Left>', lambda e: sm.play_ufo_move_tail())
        root.bind('<KeyRelease-Right>', lambda e: sm.play_ufo_move_tail())
        self.playButton.grid_forget()
        self.pause = False
        sm.play_new_game()
        sm.play_begin()

        for each in self.brix:
            for every in each:
                every.showturtle()
        self.t.bgpic(f'screen_assets/{self.current_level}.gif')
        self.game_screen.grid(column=0, row=4, columnspan=3, rowspan=4)
        self.ufo.showturtle()

    # --------Increase Level-------- #

    def increase_level(self):
        self.num_bricks = NUM_BRICKS
        self.current_level += 1
        self.current_level %= NUM_ROWS
        self.t.bgpic(f'screen_assets/{self.current_level}.gif')
        for each in self.stars:
            each.hideturtle()
            each.setpos(self.ufo.pos())

        for each in range(NUM_ROWS):
            for every in self.brix[each]:
                every.i += 1
                every.i %= NUM_ROWS
                every.reset_brick()
                every.showturtle()
        self.scoreboard.level += 1
        self.scoreboard.level %= NUM_ROWS
        self.scoreboard.c = self.brix[self.current_level][0].get_color()
        self.scoreboard.give_star()
        self.tripleplay = False
        sm.play_new_game()

    # --------Pause-------- #

    def pause_game(self):
        if self.pause:
            self.pauseButton.grid_forget()
            self.pause = False

        else:
            self.pauseButton.grid_forget()
            self.pauseButton.grid(column=0, row=0)
            self.pause = True
            sm.play_fire()

    # --------Game End-------- #

    def game_end(self, root):
        self.scoreboard.num_lives = NUMBER_OF_LIVES
        root.unbind('<Left>')
        root.unbind('<Right>')
        root.unbind('<space>')
        root.unbind('<Escape>')
        root.unbind('<Return>')
        root.bind('<Return>', lambda e: self.submitBtn.invoke())
        self.t.onkeyrelease(self.dummy, 'Left')
        self.t.onkeyrelease(self.dummy, 'Right')
        sm.play_over()
        self.game_screen.grid_forget()
        self.nameLbl.grid(column=0, row=0, columnspan=3, rowspan=3)
        self.nameEntry.grid(column=0, row=0, pady=(200, 0))
        self.submitBtn.grid(column=0, row=0, pady=(400, 0))
        self.submitBtn.wait_variable(self.name)
        self.scoreboard.level = 1
        self.current_level = 1
        self.scoreboard.check_leaderboard(self.name.get())
        self.scoreboard.update_scoreboard(
            self.current_level,
            self.brix[self.current_level - 1][0].get_color()
        )
        for each in range(NUM_ROWS):
            for every in self.brix[each]:
                every.i = each
        self.nameLbl.grid_forget()
        self.submitBtn.grid_forget()
        self.nameEntry.grid_forget()
        self.star.hideturtle()
        self.no.grid_forget()
        self.yes.grid_forget()
        self.no.grid(column=0, row=0, padx=(0, 175))
        self.yes.grid(column=0, row=0, padx=(175, 0))
        self.screen.update()

    def dummy(self):
        pass

    # --------Fire--------- #

    def fire(self):
        if not self.fired:
            self.star.setpos(self.ufo.pos())
            self.star.seth(random.randint(88, 93))
            self.star.showturtle()
            self.fired = True
            sm.play_fire()
