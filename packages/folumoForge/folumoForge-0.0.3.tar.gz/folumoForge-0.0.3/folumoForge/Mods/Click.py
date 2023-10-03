import pygame

from .. import Forge
from ..Mods.base import modBase


def modThread(root: Forge, name):
    while root.Running:
        for item in root.Screens[root.Screen].Items:
            if name in item.mods:
                mod = item.mods[name]
                if root.InEvent:
                    for event in root.NewEventList:
                        print(event)

                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mod.down(item)

                        elif event.type == pygame.MOUSEBUTTONUP:
                            mod.up(item)

                        elif event.type == pygame.MOUSEWHEEL:
                            mod.wheel(item)

                        elif event.type == pygame.MOUSEMOTION:
                            mod.motion(item)


class modClick(modBase):
    def __init__(self, root: Forge, fDown=None, fUp=None, fWheel=None, fMotion=None):
        super().__init__(root, "modClick", lambda: modThread(root, "modClick"))

        self.fDown = fDown
        self.fUp = fUp
        self.fWheel = fWheel
        self.fMotion = fMotion

    def down(self, item):
        if self.fDown:
            self.fDown(item)

    def up(self, item):
        if self.fUp:
            self.fUp(item)

    def wheel(self, item):
        if self.fWheel:
            self.fWheel(item)

    def motion(self, item):
        if self.fMotion:
            self.fMotion(item)
