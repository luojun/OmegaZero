FEELS_NOTHING = 0
FEELS_BACKGROUND = 1
FEELS_BOARD = 2
FEELS_STONE = 3

class Observation:

    @property
    def feel(self):
        return self._feel

    @feel.setter
    def set_feel(self, feel):
        self._feel = feel

    @property
    def kinesthetic(self):
        return self._kinesthetic

    @kinesthetic.setter
    def kinesthetic(self, kinesthetic):
        self._kinesthetic = kinesthetic

    @property
    def environment_image(self):
        return self._environment_image

    @environment_image.setter
    def environment_image(self, image):
        self._environment_image = image

    def __init__(self, feel=None, image=None, kinesthetic=None):
        self._feel = feel
        self._environment_image = image
        self._kinesthetic = kinesthetic
