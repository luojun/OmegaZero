from random import random

# TODO: write tests
# TODO: add YAML configuration

def test():
  env = Environment(1.0, 1.0, 19, 360)

  board = env.getBoard()

  lines = board.getLines()
  for (start_pos, end_pos) in lines:
    print(board.getLineColor(), start_pos, end_pos)

  stones = env.getStones()
  for stone in stones:
    print(stone.getColor(), stone.getCenter(), stone.getRadius())


class Environment:

  def getBackgroundColor(self):
    return self._background_color

  def getSize(self):
    return self._size

  def getBounds(self):
    return self._bounds

  def getBoard(self):
    return self._board

  def getStones(self):
    return self._stones

  def __init__(self, size_x=0.6, size_y=0.6, board_lines=4, number_of_stones=10): # 4 & 10 for tic-tac-toe
    self._background_color = (64, 128, 0, 255) # RGBA
    self._size = (size_x, size_y)
    self._center = center_x, center_y = 0.0, 0.0
    min_x, min_y = center_x - size_x / 2, center_y - size_y / 2
    max_x, max_y = center_x + size_x / 2, center_y + size_y / 2
    self._bounds = (min_x, min_y, max_x, max_y)
    self._board = Board(self._size, self._center, board_lines)

    board_inset_x, board_inset_y = self._board._inset
    stone_size = min(board_inset_x, board_inset_y) / 5 * 4
    self._stones = self._init_stones(number_of_stones, stone_size)

  def _init_stones(self, number_of_stones, stone_size):
    stone_radius = stone_size / 2
    stone_color_white = (224, 224, 224, 255)
    stone_color_black = (32, 32, 32, 255)

    center_x, center_y = self._center
    size_x, size_y = self._size
    min_x, min_y, _, _ = self._bounds

    stones = []
    for n in range(number_of_stones):
      stone_color = (stone_color_white if (n % 2) == 0 else stone_color_black)
      stone_center = (
        min_x + stone_radius + random() * (size_x - stone_size),
        min_y + stone_radius + random() * (size_y - stone_size)
      )
      stone = Stone(stone_color, stone_radius, stone_center)
      stones.append(stone)
    return stones


class Board:

  def getColor(self):
    return self._color

  def getSize(self):
    return self._size

  def getRect(self):
    return self._rect

  def getLineColor(self):
    return self._line_color

  def getNumberOfLines(self):
    return self._number_of_lines # in one direction

  def getLines(self):
    return self._lines

  def getInset(self):
    return self._inset

  def __init__(self, environment_size, environment_center, board_lines):
    self._color = (128, 64, 32, 255) # RGBA
    self._line_color = (32, 32, 32, 255) # RGBA
    environment_size_x, environment_size_y = environment_size
    environment_center_x, environment_center_y = environment_center
    self._size = board_size_x, board_size_y = environment_size_x / 3.0 * 2.0, environment_size_y / 3.0 * 2.0 # allow size_x and size_y to be different
    self._center = board_center_x, board_center_y = environment_center_x, environment_center_y # center of board
    self._number_of_lines = board_lines

    board_min_x, board_min_y = board_center_x - board_size_x / 2, board_center_y - board_size_y / 2
    board_max_x, board_max_y = board_min_x + board_size_x, board_min_y + board_size_y
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

    x_lines = [((board_line_min_x, board_line_min_y + board_line_inc_y * n), (board_line_max_x, board_line_min_y + board_line_inc_y * n)) for n in range(board_lines)]
    y_lines = [((board_line_min_x + board_line_inc_x * n, board_line_min_y), (board_line_min_x + board_line_inc_x * n, board_line_max_y)) for n in range(board_lines)]
    self._lines = x_lines + y_lines


class Stone:

  def getColor(self):
    return self._color

  def getRadius(self):
    return self._radius

  def getCenter(self):
    return self._center

  def moveBy(translation, bounds): # could use insets instead of bounds
    x, y = self._center
    tx, ty = translation
    x, y = x + tx, y + ty
    min_x, min_y, max_x, max_y = bounds
    if x < min_x + self._radius:
      x = min_x + self.radius
    if y < min_y + self.radius:
      y = min_y + self.radius
    if x > max_x - self.radius:
      x = max_x - self.radius
    if y > max_y - self.radius:
      y = max_y - self.radius

  def __init__(self, color, radius, center):
    self._color = color
    self._radius = radius
    self._center = center


#test()

