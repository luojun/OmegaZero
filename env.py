from random import random
from math import sqrt

# TODO: add interaction interface to the environment: agents, tactile feedback, states of interaction with a stone.
# TODO: refactor into separate files under an env folder
# TODO: asychronous agent threads
# TODO: write tests
# TODO: add YAML configuration

def test():
  # env = Environment(1.0, 1.0, 19, 360, 2) # Go
  # env = Environment(1.0, 1.0, 15, 360, 2) # Gomoku
  env = Environment() # Tic-Tac-Toe

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

  def getAgents(self):
    return self._agents

  def getHoldings(self):
    return self._holdings

  def tick(self):
    for agent in self.getAgents(): # single thread: agents are all synchronized ...
      holdings = self.getHoldings()
      agentIndex = agent.getId()

      stoneHeld = holdings[agentIndex]

      action = agent.observeActCallback(None)
      if not action.press():
        stoneHeld = None
      elif stoneHeld is None:
        stoneHeld = self._pickUp(agent.getCenter(), agent.getRadius())

      agent.moveBy(action.move(), self.getBounds())
      if stoneHeld is not None:
        stoneHeld.moveTo(agent.getCenter())

      holdings[agentIndex] = stoneHeld

  def __init__(self, size_x=0.6, size_y=0.6, board_lines=4, number_of_stones=10, number_of_agents=2): # 4, 10, 2 for tic-tac-toe
    self._background_color = (8, 80, 8, 255) # RGBA
    self._size = (size_x, size_y)
    self._center = center_x, center_y = 0.0, 0.0
    min_x, min_y = center_x - size_x / 2, center_y - size_y / 2
    max_x, max_y = center_x + size_x / 2, center_y + size_y / 2
    self._bounds = (min_x, min_y, max_x, max_y)
    self._board = Board(self._size, self._center, board_lines)

    board_inset_x, board_inset_y = self._board._inset
    stone_size = min(board_inset_x, board_inset_y) / 5 * 4
    self._stones = self._init_stones(number_of_stones, stone_size)

    agent_size = stone_size * 0.8 # TODO: configuration
    self._agents = self._init_agents(number_of_agents, agent_size)
    self._holdings = self._init_holdings(number_of_agents) # for now, one agent can hold at most one stone

  def _init_stones(self, number_of_stones, stone_size):
    stone_radius = stone_size / 2
    stone_color_white = (224, 224, 224, 255)
    stone_color_black = (32, 32, 32, 255)

    center_x, center_y = self._center
    size_x, size_y = self._size
    min_x, min_y, _, _ = self._bounds

    stones = []
    for index in range(number_of_stones):
      stone_color = (stone_color_white if (index % 2) == 0 else stone_color_black)
      stone_center = (
        min_x + stone_radius + random() * (size_x - stone_size),
        min_y + stone_radius + random() * (size_y - stone_size)
      )
      stone = Stone(index, stone_color, stone_radius, stone_center)
      stones.append(stone)
    return stones

  def _init_agents(self, number_of_agents, agent_size):
    agent_radius = agent_size / 2
    agent_color = (0, 0, 224, 255)

    center_x, center_y = self._center
    size_x, size_y = self._size
    min_x, min_y, _, _ = self._bounds

    agents = []
    print("initing ...")
    for index in range(number_of_agents):
      agent_center = (
        min_x + agent_radius + random() * (size_x - agent_size),
        min_y + agent_radius + random() * (size_y - agent_size)
      )
      agent = Agent(index, agent_color, agent_radius, agent_center)
      print(id(agent))
      agents.append(agent)
    return agents

  def _init_holdings(self, number_of_agents):
    return [None for n in range(number_of_agents)]

  def _pickUp(self, center, radius):
    for stone in self.getStones():
      x, y = center
      stone_x, stone_y = stone.getCenter()
      d = sqrt((stone_x - x) * (stone_x - x) + (stone_y - y) * (stone_y - y))
      if d < radius:
        return stone
    return None
      

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
    self._color = (224, 128, 32, 255) # RGBA
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


class Movable:

  def getId(self):
    return self._id

  def getColor(self):
    return self._color

  def getRadius(self):
    return self._radius

  def getCenter(self):
    return self._center

  def moveBy(self, translation, bounds): # could use insets instead of bounds
    x, y = self._center
    tx, ty = translation
    x, y = x + tx, y + ty
    min_x, min_y, max_x, max_y = bounds
    radius = self.getRadius()
    if x < min_x + radius:
      x = min_x + radius
    if y < min_y + radius:
      y = min_y + radius
    if x > max_x - radius:
      x = max_x - radius
    if y > max_y - radius:
      y = max_y - radius
    self._center = x, y

  def moveTo(self, target):
    self._center = target

  def __init__(self, index, color, radius, center):
    self._id = index
    self._color = color
    self._radius = radius
    self._center = center


class Stone(Movable):
  pass


class Agent(Movable): # Note how stones are equivalent to super of agents, evolutionarily speaking ;-)

  def observeActCallback(self, observation):
    self._newObservation = observation
    return self._decide(self._newObservation)

  def _decide(self, observation):
    return Action(True)

class Action:

  def press(self):
    return self._press

  def move(self):
    return self._move

  def __init__(self, act_randomly=False):
    if act_randomly:
      self._press = random() < 0.2 # 20% of time
      self._move = 0.01 * (random() - 0.5), 0.01 * (random() - 0.5) # at most 1cm in one direction at a time
    else:
      raise NoImplementedError("Do not yet support generation of non-random action.")
    


#test()

