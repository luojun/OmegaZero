from .movable import Movable

class Stone(Movable):
    def __init__(self, index, center, is_black):
        super().__init__(index, center)
        self._is_black = is_black

    @property
    def is_black(self):
        return self._is_black
