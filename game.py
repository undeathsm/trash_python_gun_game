from tkinter import *
from random import randrange as rnd
from gun import Gun
from target import Target
import math
import time

class Game():
    def __init__(self, root, rounds = 12, w = 800, h = 600):
        root = Tk()
        root.geometry("{}x{}".format(w, h))
        self.root = root

        self.round = 1
        self.rounds = rounds
        self.score = 0

        self.canv = Canvas(root,bg='white')
        self.canv.pack(fill=BOTH,expand=1)
        
        self.score_text_x = 100
        self.score_text_y = 50
        self.score_text = self.canv.create_text(self.score_text_x, self.score_text_y, text="SCORE: {}".format(self.score), justify=CENTER, font="Verdana 14")

        self.rounds_text_x = 500
        self.rounds_text_y = 50
        self.rounds_text = self.canv.create_text(self.rounds_text_x, self.rounds_text_y, text="ROUND: {} OF {}".format(self.round, self.rounds), justify=CENTER, font="Verdana 14")

        self.targets = []
        self.targets_v = 10
        self.targets.append(Target(rnd(500, 700), rnd(100, 500), rnd(500, 700), rnd(100, 500), rnd(10, 30), -1*rnd(1,2)*self.targets_v, self.canv, self.root))

        self.gun = Gun(self.root, self.canv, self.targets, self, (100, 475))
        self.game_end = False

        self.serv_tickrate = 5
        self.game_action()
        mainloop()

    def targets_action(self):
        
        new_targets = list(filter(lambda a: not a.is_shooted, self.targets))

        n = len(self.targets)
        for i in range(n):
            if self.targets[i].is_shooted == True:
                self.targets[i].delete()

        self.targets = new_targets
        self.gun.targets = self.targets

    def game_action(self):
        self.canv.delete(self.score_text)
        self.score_text = self.canv.create_text(self.score_text_x, self.score_text_y, text="SCORE: {}".format(self.score), justify=CENTER, font="Verdana 14")

        self.targets_action()
        if len(self.targets) == 0:
            self.round += 1
            if self.round <= self.rounds:
                self.canv.delete(self.rounds_text)
                self.rounds_text = self.canv.create_text(self.rounds_text_x, self.rounds_text_y, text="ROUND: {} OF {}".format(self.round, self.rounds), justify=CENTER, font="Verdana 14")

            self.targets_v *= 1.1

        if self.round > self.rounds:
            self.canv.create_text(400, 300, text="GAME IS OVER\nSCORE: {}".format(self.score), justify=CENTER, fill="orange", font="Verdana 25")
            self.game_end = True
            self.root.after(2000, self.root.destroy)
            return

        if len(self.targets) == 0:
            for i in range(self.round):
                self.targets.append(Target(rnd(500, 700), rnd(100, 500), rnd(500, 700), rnd(100, 500), rnd(10, 30), -1*rnd(1,2)*self.targets_v, self.canv, self.root))

        self.root.after(self.serv_tickrate, self.game_action)