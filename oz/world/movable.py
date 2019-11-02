class Movable:

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        self._index = new_index

    @property
    def center(self):
        return self._center

    def move_by(self, translation, bounds):
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

    def move_to(self, target):
        self._center = target

    def __init__(self, index, center):
        self._index = index
        self._center = center
