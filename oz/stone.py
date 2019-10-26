from movable import Movable

class Stone(Movable):
    def __init__(self, index, is_black, color, edge_color, radius, edge_ratio, center):
        super().__init__(index, color, edge_color, radius, edge_ratio, center)
        self._is_black = is_black

    @property
    def is_black(self):
        return self._is_black
