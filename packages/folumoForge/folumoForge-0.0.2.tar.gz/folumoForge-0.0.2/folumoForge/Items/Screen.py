import pygame

from .. import Forge


class Screen:
    def __init__(self, root, name, size):
        self.root: Forge = root
        self.name = name
        self.size = size
        self.EventAble = []
        self.Items = []
        self.OnF = {}

    def SwitchScreen(self):
        self.root.MainRoot = pygame.display.set_mode(self.size)
        self.root.Screen = self.name

    def DeleteScreen(self):
        self.root.Screens.discard(self)

    def OnFrame(self, _id, func):
        self.OnF[_id] = func

    def render(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.root.Running = False

            for item in self.EventAble:
                item.update(event)

        for fr in self.OnF:
            self.OnF[fr]()

        for item in self.Items:
            item.update()

        for item in self.EventAble:
            item.update()
