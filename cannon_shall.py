from tkinter import *
from random import choice
import math
import time

class CannonShell():
    def __init__(self, root, canv, game, x, y, targets, v, angle):
        self.canv = canv
        self.root = root
        self.game = game
        self.targets = targets

        self.end_animate = False
        self.life_time = 0

        self.x = x
        self.y = y
        self.vx = v*math.cos(angle)
        self.vy = v*math.sin(angle)
        self.dx = 0
        self.dy = 0

        self.r = 25 / 2
        self.paint_tickrate = 35
        self.serv_tickrate = 5
        self.g = 9.8

        self.color = choice(['red','orange','yellow','green','blue'])

        r = self.r
        self.cannon_shell = self.canv.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill=self.color, outline=self.color)
        self.move()
        self.animate()

    def move(self):
        if self.game.game_end:
            self.delete()
            return
        
        if self.end_animate:
            return

        if self.life_time >= 12000:
            self.delete()
            return

        self.life_time += self.serv_tickrate

        self.on_shoot()
        
        dt = (self.serv_tickrate)*0.02

        self.x += dt*self.vx
        self.y += dt*self.vy
        self.dx += dt*self.vx
        self.dy += dt*self.vy

        k = 0.8
        r = self.r
        if self.x - r <= 0 and self.vx < 0:
            self.vx *= -k
            self.vy *= k
        elif self.x + r >= 800 and self.vx > 0:
            self.vx *= -k
            self.vy *= k
        
        if self.y + r >= 600 and self.vy > 0:
            self.vy *= -k
            self.vx *= k
        
        if self.y + r < 599:
            self.vy += self.g*dt
        elif self.y + r >= 600 and abs(self.vy) < 12:
            self.vy = 0
            self.vx = 0
            
        self.root.after(self.serv_tickrate, self.move)

    def paint_cannon_shell(self):
        if self.cannon_shell:
            self.canv.delete(self.cannon_shell)

        r = self.r
        self.cannon_shell = self.canv.create_oval(self.x-r, self.y-r, self.x+r, self.y+r, fill=self.color, outline=self.color)

    def on_shoot(self):
        n = len(self.targets)
        for i in range(n):
            target = self.targets[i]
            tr = target.r
            tx = target.x
            ty = target.y

            r = self.r
            x = self.x
            y = self.y

            if math.hypot(x - tx, y - ty) < r + tr:
                self.targets[i].is_shooted = True
                self.game.score += 12
                self.delete()

    def animate(self):
        if self.end_animate:
            return

        self.canv.move(self.cannon_shell, self.dx, self.dy)
        self.dx = 0
        self.dy = 0
        self.root.after(self.paint_tickrate, self.animate)

    def delete(self):
        self.end_animate = True
        self.canv.delete(self.cannon_shell)

        del self