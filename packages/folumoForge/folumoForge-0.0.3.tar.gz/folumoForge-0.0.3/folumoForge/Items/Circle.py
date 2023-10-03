import pygame

from .Screen import Screen
from ..Mods.base import modBase


class Circle:
    def __init__(self, screen: Screen, center=(0, 0), radius=90, color="white", width=0,
                 top_right=False,
                 top_left=False,
                 bottom_left=False,
                 bottom_right=False):
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.mods = {}

        self.screen = screen
        screen.Items.append(self)
        self.center = center
        self.radius = radius
        self.color = color
        self.width = width
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

    def config(self, center, radius, color, width=0,
               top_right=False,
               top_left=False,
               bottom_left=False,
               bottom_right=False):
        self.center = center
        self.radius = radius
        self.color = color
        self.width = width
        self.top_right = top_right
        self.top_left = top_left
        self.bottom_left = bottom_left
        self.bottom_right = bottom_right

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod

    def update(self):
        self.rect = pygame.draw.circle(self.screen.root.MainRoot, self.color, self.center, self.radius, self.width,
                                       self.top_right,
                                       self.top_left,
                                       self.bottom_left,
                                       self.bottom_right)
