from tkinter import *
from random import randrange as rnd
from cannon_shall import CannonShell
import math
import time

class Gun():
    def __init__(self, root, canv, targets, game, start_point = (100, 475)):
        self.root = root
        self.root.bind('<Motion>', self.mouse_move)
        self.root.bind("<ButtonPress-1>", self.mouse_down)
        self.root.bind("<ButtonRelease-1>", self.mouse_up)
        self.game = game

        self.canv = canv
        self.targets = targets
        self.barrel = None
        self.rear_barrel = None

        self.is_mouse_up = True
        self.length = 100
        self.width = 30
        self.power = 0
        self.alpha = 0
        self.color = "black"

        self.x = start_point[0]
        self.y = start_point[1]

    def mouse_move(self, event):
        dx = event.x - self.x
        dy = event.y - self.y
        self.alpha = math.atan2(dy, dx)
        self.paint_gun()

    def mouse_pressing(self):
        if self.is_mouse_up:
            return

        if self.power < 100:
            self.power += 1

        if self.power > 90:
            self.color = "red"
        elif self.power > 15:
            self.color = "orange"
        else:
            self.color = "black"

        self.paint_gun()
        self.root.after(15, self.mouse_pressing)

    def mouse_down(self, event):

        self.is_mouse_up = False
        self.root.after(15, self.mouse_pressing)

    def mouse_up(self, event):
        self.is_mouse_up = True
        self.on_shoot()
        self.power = 0
        self.color = "black"
        self.paint_gun()

    def paint_gun(self):
        if self.barrel:
            self.canv.delete(self.barrel)
            self.canv.delete(self.rear_barrel)

        length = self.length*(1 + self.power * 0.0015)
        x2 = self.x + length * math.cos(self.alpha)
        y2 = self.y + length * math.sin(self.alpha)
        r = self.width*(1 + self.power * 0.002)/2
        self.rear_barrel = self.canv.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill=self.color, outline=self.color)
        self.barrel = self.canv.create_line(self.x, self.y, x2, y2, fill=self.color, width=self.width*(1 + self.power * 0.0005))

    def on_shoot(self):
        length = self.length*(1 + self.power * 0.0015) + self.width/2
        x = self.x + length * math.cos(self.alpha)
        y = self.y + length * math.sin(self.alpha)

        v = self.power
        cannon_shell = CannonShell(self.root, self.canv, self.game, x, y, self.targets, v, self.alpha)

        self.game.score -= 2