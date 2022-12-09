from turtle import RawTurtle
from math import floor
import time
import json
import sound_module as sm

top_score = {'LLCoolMel': 106600}


class ScoreBoard(RawTurtle):
    def __init__(self, t, n, level):
        super().__init__(t)
        self.penup()
        self.hideturtle()
        self.goto(-390, 140)
        self.color("#ccd130")
        self.current_score = 0
        self.num_lives = n
        self.hunkset = False
        self.milset = False
        self.start_time = time.time()
        self.podiums = False
        self.scores = top_score
        self.boost = 1.0
        self.level = level
        with open('scores.json', 'r+') as file:
            self.scores = json.load(file)
        self.update_scoreboard(self.level)


    def update_scoreboard(self, level):

        highest_score = 0
        name = ''
        txt = "{:,}"
        try:
            name = max(self.scores, key=self.scores.get)
            highest_score = self.scores[name]
        except AttributeError:
            pass
        except ValueError:
            pass

        self.clear()
        self.color('#40916c')
        self.goto(-390, 150)
        self.write(
            f"Score: {txt.format(self.current_score)}",
            False,
            'left',
            font=(
                'Monospace',
                16,
                'normal'
            )
        )
        self.color('#40916c')
        self.goto(-220, 155)
        self.write(
            f"Level: {level}",
            False,
            'left',
            font=(
                'Monospace',
                12,
                'normal'
            )
        )
        self.goto(0, 157)
        self.color('#b7e4c7')
        self.write(
            f"High Score - {name}   {txt.format(highest_score)}",
            False,
            'center',
            font=(
                'monospace',
                10,
                'normal'
            )
        )
        self.goto(220, 155)
        self.color('#ff2222')
        self.write(
            f"Boost: {self.boost}x",
            False,
            'center',
            font=(
                'monospace',
                12,
                'normal'
            )
        )


        self.goto(390, 150)
        self.color('#40916c')
        self.write(
            f"Stars: {self.num_lives}",
            False,
            'right',
            font=(
                'Monospace',
                16,
                'normal'
            )
        )



    def take_star(self):
        self.num_lives -= 1
        self.update_scoreboard(self.level)
        if self.num_lives == 0:
            if len(self.scores) > 0:
                if len(self.scores) >= 10:
                    if self.current_score > min(self.scores.values()):
                        self.podiums = True
                else:
                    self.podiums = True
            else:
                self.podiums = True




    def check_leaderboard(self, name):
        if self.podiums:
            self.podiums = False
            if name in self.scores:
                if self.scores[name] < self.current_score:
                    self.scores.update({name: self.current_score})
                else:
                    return
            elif len(self.scores) >= 10:
                self.scores.pop(min(self.scores))
            self.scores[name] = self.current_score
        file = open('scores.json', 'r+')
        file.truncate()
        file.write(json.dumps(self.scores))
        file.close()




    def get_scores(self):
        return self.scores

    def increase_score(self, p, n):
        dif = time.time() - self.start_time
        if dif < 0.2:
            self.boost *= 1.1
        elif self.boost > 1:
            self.boost *= .95
        self.boost = round(self.boost, 1)
        self.start_time = time.time()
        self.current_score += floor(p*self.boost)
        if not self.hunkset:
            if self.current_score >= 100000:
                self.hunkset = True
                self.give_star()
        if not self.milset:
            if self.current_score >= 200000:
                self.milset = True
                self.give_star()
        sm.play_brick(n)
        self.update_scoreboard(self.level)

    def give_star(self):
        self.num_lives += 1
        self.update_scoreboard(self.level)
