class Board:

    @property
    def rect(self):
        return self._rect

    @property
    def lines(self):
        return self._lines

    def is_on_board(self, point):
        point_x, point_y = point
        board_min_x, board_min_y, board_max_x, board_max_y = self.rect
        is_on_board_x = board_min_x < point_x and point_x < board_max_x
        is_on_board_y = board_min_y < point_y and point_y < board_max_y
        return is_on_board_x and is_on_board_y

    def __init__(self, world_settings):
        board_center_x, board_center_y = world_settings.board.center
        board_size_x, board_size_y = world_settings.board.size
        board_min_x = board_center_x - board_size_x / 2
        board_min_y = board_center_y - board_size_y / 2
        board_max_x = board_min_x + board_size_x
        board_max_y = board_min_y + board_size_y
        self._rect = (board_min_x, board_min_y, board_max_x, board_max_y)

        (board_inset_x, board_inset_y) = world_settings.board.insets
        board_line_min_x = board_min_x + board_inset_x
        board_line_min_y = board_min_y + board_inset_y
        board_line_max_x = board_max_x - board_inset_x
        board_line_max_y = board_max_y - board_inset_y
        board_line_inc_x = board_inset_x
        board_line_inc_y = board_inset_y

        self._lines = []
        for index in range(world_settings.board.number_of_lines):
            x_line = ((board_line_min_x, board_line_min_y + board_line_inc_y * index),
                      (board_line_max_x, board_line_min_y + board_line_inc_y * index))
            y_line = ((board_line_min_x + board_line_inc_x * index, board_line_min_y),
                      (board_line_min_x + board_line_inc_x * index, board_line_max_y))
            self._lines.append(x_line)
            self._lines.append(y_line)
