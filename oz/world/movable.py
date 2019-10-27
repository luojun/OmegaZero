class Movable:

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        self._index = new_index

    @property
    def color(self):
        return self._color

    @property
    def edge_color(self):
        return self._edge_color

    @property
    def radius(self):
        return self._radius

    @property
    def edge_width(self):
        return self._edge_width

    @property
    def center(self):
        return self._center

    def move_by(self, translation, bounds): # could use insets instead of bounds
        current_x, current_y = self._center
        delta_x, delta_y = translation
        new_x, new_y = current_x + delta_x, current_y + delta_y
        min_x, min_y, max_x, max_y = bounds
        if new_x < min_x:
            new_x = min_x
        if new_y < min_y:
            new_y = min_y
        if new_x > max_x:
            new_x = max_x
        if new_y > max_y:
            new_y = max_y

        actual_delta_x, actual_delta_y = new_x - current_x, new_y - current_y
        self._center = new_x, new_y
        return actual_delta_x, actual_delta_y # return the actual change

    # TODO: also return actual delta
    def move_to(self, target):
        self._center = target

    # TODO: do we really need to remember these?
    def __init__(self, index, color, edge_color, radius, edge_ratio, center):
        self._index = index
        self._color = color
        self._edge_color = edge_color
        self._radius = radius
        self._edge_width = radius * edge_ratio
        self._center = center
