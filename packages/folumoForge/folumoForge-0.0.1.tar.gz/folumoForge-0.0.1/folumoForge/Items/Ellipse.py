import pygame

from ..Items.Screen import Screen
from ..Mods.base import modBase


class Ellipse:
    def __init__(self, screen: Screen, xy, wh, color, width):
        self.rect = pygame.Rect((0, 0), (0, 0))

        self.mods = {}

        self.screen = screen
        self.xy = xy
        self.wh = wh
        self.color = color
        self.width = width
        self.rectE = pygame.Rect(xy, wh)

    def config(self, xy, wh, color, width):
        self.xy = xy
        self.wh = wh
        self.color = color
        self.width = width
        self.rectE = pygame.Rect(xy, wh)

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod

    def update(self):
        self.rect = pygame.draw.ellipse(self.screen.root.MainRoot, self.color, self.rectE, self.width)
