from config import MovableConfig
from world import movable

class Stone(movable.Movable):
    def __init__(self, index, is_black, stone_configs, radius, center):
        if is_black:
            color = stone_configs.color_black
            edge_color = stone_configs.edge_color_black
        else:
            color = stone_configs.color_white
            edge_color = stone_configs.edge_color_white
        movable_configs = MovableConfig(color, edge_color, stone_configs.edge_width_ratio)
        super().__init__(index, movable_configs, radius, center)
        self._is_black = is_black

    @property
    def is_black(self):
        return self._is_black
