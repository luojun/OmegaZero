# TODO: differentiate class property and instance property

class Board:

    @property
    def color(self):
        return self._color

    @property
    def size(self):
        return self._size

    @property
    def rect(self):
        return self._rect

    @property
    def line_color(self):
        return self._line_color

    @property
    def line_width(self):
        return self._line_width

    @property
    def number_of_lines(self):
        return self._number_of_lines # in one direction

    @property
    def lines(self):
        return self._lines

    @property
    def inset(self):
        return self._inset

    def is_on_board(self, point):
        point_x, point_y = point
        board_min_x, board_min_y, board_max_x, board_max_y = self.rect
        is_on_board_x = board_min_x < point_x and point_x < board_max_x
        is_on_board_y = board_min_y < point_y and point_y < board_max_y
        return is_on_board_x and is_on_board_y

    # TODO: simplify this
    def __init__(self, configs, world_size, world_center, board_lines):
        self._color = configs.board_color
        self._line_color = configs.board_line_color

        world_size_x, world_size_y = world_size
        world_center_x, world_center_y = world_center
        board_size_x = world_size_x * configs.board_size_x_ratio
        board_size_y = world_size_y * configs.board_size_y_ratio
        self._size = board_size_x, board_size_y
        board_center_x, board_center_y = world_center_x, world_center_y
        self._center = board_center_x, board_center_y
        self._number_of_lines = board_lines

        board_min_x = board_center_x - board_size_x / 2
        board_min_y = board_center_y - board_size_y / 2
        board_max_x = board_min_x + board_size_x
        board_max_y = board_min_y + board_size_y
        self._rect = (board_min_x, board_min_y, board_max_x, board_max_y)

        board_inset_x = board_size_x / (board_lines + 1)
        board_inset_y = board_size_y / (board_lines + 1)
        board_line_min_x = board_min_x + board_inset_x
        board_line_min_y = board_min_y + board_inset_y
        board_line_max_x = board_max_x - board_inset_x
        board_line_max_y = board_max_y - board_inset_y
        board_line_inc_x = board_inset_x
        board_line_inc_y = board_inset_y

        self._inset = (board_inset_x, board_inset_y)
        # Differentiate x and y in version 5.0 ;-)
        self._line_width = configs.board_line_width_ratio * board_inset_x

        self._lines = []
        for index in range(board_lines):
            x_line = ((board_line_min_x, board_line_min_y + board_line_inc_y * index),
                      (board_line_max_x, board_line_min_y + board_line_inc_y * index))
            y_line = ((board_line_min_x + board_line_inc_x * index, board_line_min_y),
                      (board_line_min_x + board_line_inc_x * index, board_line_max_y))
            self._lines.append(x_line)
            self._lines.append(y_line)
