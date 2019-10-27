class Transform:

    def __init__(self, world_size, dpm=600.0): # 600 dpm -- dots per meter
        size_x, size_y = world_size
        self._trans_x = size_x / 2.0
        self._trans_y = size_y / 2.0
        self._scale = dpm

    def scale2view(self, value):
        return round(self._scale * value)

    def scale2view2d(self, pair):
        first_value, second_value = pair
        return (self.scale2view(first_value), self.scale2view(second_value))

    def translate2view2d(self, pair):
        current_x, current_y = pair
        return (current_x + self._trans_x, current_y + self._trans_y)

    def world2view2d(self, pair):
        return self.scale2view2d(self.translate2view2d(pair))

    def world2view4d(self, quad):
        current_x1, current_y1, current_x2, current_y2 = quad
        new_x1, new_y1 = self.world2view2d((current_x1, current_y1))
        new_x2, new_y2 = self.world2view2d((current_x2, current_y2))
        return (new_x1, new_y1, new_x2, new_y2)

    def scale2world(self, value):
        return value / self._scale

    def scale2world2d(self, pair):
        current_x, current_y = pair
        return (self.scale2world(current_x), self.scale2world(current_y))

    def translate2world2d(self, pair):
        current_x, current_y = pair
        return (current_x - self._trans_x, current_y - self._trans_y)

    def view2world2d(self, pair):
        return self.translate2world2d(self.scale2world2d(pair))
