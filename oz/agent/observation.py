from enum import Enum, auto

class TactileQuality(Enum):
    nothing = auto()
    background = auto()
    board = auto()
    stone = auto()

class Observation:

    @property
    def feel(self):
        return self._feel

    @feel.setter
    def feel(self, feel):
        self._feel = feel

    @property
    def world_image(self):
        return self._world_image

    @world_image.setter
    def world_image(self, image):
        self._world_image = image

    @property
    def kinesthetic(self):
        return self._kinesthetic

    @kinesthetic.setter
    def kinesthetic(self, kinesthetic):
        self._kinesthetic = kinesthetic

    def __init__(self, feel=TactileQuality.nothing, image=None, kinesthetic=None):
        self._feel = feel
        self._world_image = image
        self._kinesthetic = kinesthetic
