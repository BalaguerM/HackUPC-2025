import pygame
import math
from settings import *

class Bullet:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.dir = direction
        self.life = 30

    def updateBullet(self):
        # Moving
        self.x += bullet_speed * math.cos(self.dir * math.pi / 180)
        self.y += bullet_speed * math.sin(self.dir * math.pi / 180)

        # Drawing
        pygame.draw.circle(gameDisplay, white, (int(self.x), int(self.y)), 3)

        # Wrapping
        if self.x > WINDOW_WIDTH:
            self.x = 0
        elif self.x < 0:
            self.x = WINDOW_WIDTH
        elif self.y > WINDOW_HEIGHT:
            self.y = 0
        elif self.y < 0:
            self.y = WINDOW_HEIGHT
        self.life -= 1
