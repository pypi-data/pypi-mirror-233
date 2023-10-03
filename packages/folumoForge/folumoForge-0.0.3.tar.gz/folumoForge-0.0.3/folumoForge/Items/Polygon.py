import pygame

from ..Items.Screen import Screen
from ..Mods.base import modBase


class Polygon:
    def __init__(self, screen: Screen, points=None, width=0, color="white"):
        self.mods = {}
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.screen = screen
        screen.Items.append(self)

        if points is None:
            self.points = [(100, 25), (50, 100), (150, 100)]

        self.color = color
        self.width = width

    def config(self, points=None, width=0, color="white"):
        if points is None:
            self.points = [(100, 25), (50, 100), (150, 100)]

        self.color = color
        self.width = width

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod

    def update(self):
        self.rect = pygame.draw.polygon(self.screen.root.MainRoot, self.color, self.points, self.width)
