import pygame

from .Screen import Screen
from ..Mods.base import modBase


class Arc:
    def __init__(self, screen: Screen, xy=(0, 0), wh=(50, 50), color="white", start_angle=0, stop_angle=180, width=1):
        self.rectE = pygame.Rect(xy, wh)
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.mods = {}

        self.xy = xy
        self.wh = wh
        self.color = color
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.width = width

        self.screen = screen
        screen.Items.append(self)

    def config(self, xy, wh, color, start_angle, stop_angle, width=1):
        self.rectE = pygame.Rect(xy, wh)
        self.xy = xy
        self.wh = wh
        self.color = color
        self.start_angle = start_angle
        self.stop_angle = stop_angle
        self.width = width

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod

    def update(self):
        self.rect = pygame.draw.arc(self.screen.root.MainRoot, self.color, self.rectE,
                                    self.start_angle,
                                    self.stop_angle,
                                    self.width)

        return self.rect
