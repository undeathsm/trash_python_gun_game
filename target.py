from tkinter import *
from random import randrange as rnd
import math
import time

class Target():
    def __init__(self, x1, y1, x2, y2, r, v, canv, root):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.vx = v*math.cos(math.atan2(y1 - y2, x1 - x2))
        self.vy = v*math.sin(math.atan2(y1 - y2, x1 - x2))

        if x1 != x2:
            self.x = rnd(min(x1, x2), max(x1, x2))
        else:
            self.vx = 0
            self.x = x1

        if y1 != y2:
            self.y = rnd(min(y1, y2), max(y1, y2))
        else:
            self.vy = 0
            self.x = x1

        self.r = r
        self.is_shooted = False

        self.canv = canv
        self.root = root
        self.paint_tickrate = 30
        self.serv_tickrate = 5
        self.target_circle = None
        self.centr_circle = None
        self.circles = []

        self.paint_target()

        self.move()
        self.animate()

    def delete(self):
        self.delete_from_canvas()
        del self

    def delete_from_canvas(self):
        if self.target_circle:
            self.canv.delete(self.target_circle)

        if self.centr_circle:
            self.canv.delete(self.centr_circle)

        if self.circles is not []:
            for i in range(len(self.circles)):
                self.canv.delete(self.circles[i])

            self.circles = []

    def paint_target(self):
        self.delete_from_canvas()

        r = self.r
        n = r // 6
        dr = r / n
        x = self.x
        y = self.y
        border_width = dr / 2

        self.target_circle = self.canv.create_oval(
            x-r,
            y-r,
            x+r,
            y+r,
            fill="yellow",
            outline=""
        )

        for i in range(n):
            self.circles.append(
                self.canv.create_oval(
                    x - dr*(i + 1),
                    y - dr*(i + 1),
                    x + dr*(i + 1),
                    y + dr*(i + 1),
                    fill="",
                    outline="black",
                    width=border_width
                )
            )

        self.centr_circle = self.canv.create_oval(
            x-border_width,
            y-border_width,
            x+border_width,
            y+border_width,
            fill="red",
            outline=""
        )

    def move(self):
        if self.is_shooted:
            return

        dt = self.serv_tickrate * 0.005
        x = self.x
        y = self.y
        x1 = self.x1
        x2 = self.x2
        y1 = self.y1
        y2 = self.y2

        if x >= max(x1, x2) or x <= min(x1, x2) or y >= max(y1, y2) or y <= min(y1, y2):
            self.vx *= -1
            self.vy *= -1

        self.x += self.vx * dt
        self.y += self.vy * dt

        self.root.after(self.serv_tickrate, self.move)


    def animate(self):
        if self.is_shooted:
            self.delete_from_canvas()
            return

        self.paint_target()
        self.root.after(self.paint_tickrate, self.animate)