import pygame

from ..Items.Screen import Screen
from ..Mods.base import modBase


class Rect:
    def __init__(self, screen: Screen, xy=(0, 0), wh=(50, 50), color="white"):
        self.screen = screen
        screen.Items.append(self)

        self.xy = xy
        self.wh = wh
        self.color = color

        self.rect = pygame.Rect(xy, wh)

        self.mods = {}

    def config(self, xy=(0, 0), wh=(50, 50), color="white"):
        self.color = color
        self.xy = xy
        self.wh = wh

        self.rect = pygame.Rect(xy, wh)

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod

    def update(self):
        pygame.draw.rect(self.screen.root.MainRoot, self.color, pygame.Rect(self.xy, self.wh))
