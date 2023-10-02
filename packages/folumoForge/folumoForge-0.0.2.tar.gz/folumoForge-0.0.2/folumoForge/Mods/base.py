from threading import Thread

from .. import Forge


class modBase:
    def __init__(self, root: Forge, name, threadFunc):
        self.name = name
        if name not in root.modThreads:
            t = Thread(target=threadFunc)
            t.start()
            root.modThreads[name] = t

    def preRender(self, data):
        ...

    def postRender(self, data):
        ...

    def Fail(self, error):
        ...

    def Success(self):
        ...
