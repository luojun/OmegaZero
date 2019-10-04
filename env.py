from random import random
from math import sqrt

from movable import Agent
from movable import Stone
from movable import Observation 

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

  def tick(self, gui_agent_action=None, env_image=None):
    holdings = self.getHoldings()
    agents = self.getAgents()

    # single thread: agents are all synchronized ...

    # receive the rendered env image here because we defer that to the GUI/Pygame
    for agent in agents: # single thread: agents are all synchronized ...
      agent.getCurrentObservation().setEnvImage(env_image)

    # TODO: config for the number of gui_agents
    agents[0].setCurrentAction(gui_agent_action)

    # apply motion. We move all agents and the stones held first before applying the press action.
    for agent in agents:
      agent.moveBy(agent.getCurrentAction().move(), self.getBounds())
      stoneHeld = holdings[agent.getId()]
      if stoneHeld is not None:
        stoneHeld.moveTo(agent.getCenter())

    # apply press and update tactile feedback.
    for agent in agents:
      pressed = agent.getCurrentAction().press()
      stoneHeld = holdings[agent.getId()]
      if not pressed:
        stoneHeld = None
      elif stoneHeld is None:
        stoneHeld = self._pickUp(agent.getCenter(), agent.getRadius())
      holdings[agent.getId()] = stoneHeld

      if not pressed:
        agent.getCurrentObservation().setFeel(Observation.FEELS_NOTHING)
      elif stoneHeld:
        agent.getCurrentObservation().setFeel(Observation.FEELS_STONE)
      elif self.getBoard().onBoard(agent.getCenter()):
        agent.getCurrentObservation().setFeel(Observation.FEELS_BOARD)
      else:
        agent.getCurrentObservation().setFeel(Observation.FEELS_BACKGROUND)

    # TODO: config for the number of gui_agents
    for agent in agents[1:]:
      agent.decideNextAction(agent.getCurrentObservation())


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
    agent_color = (96, 64, 192, 255)

    center_x, center_y = self._center
    size_x, size_y = self._size
    min_x, min_y, _, _ = self._bounds

    agents = []
    for index in range(number_of_agents):
      agent_center = (
        min_x + agent_radius + random() * (size_x - agent_size),
        min_y + agent_radius + random() * (size_y - agent_size)
      )
      agent = Agent(index, agent_color, agent_radius, agent_center)
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

  def onBoard(self, point):
    point_x, point_y = point
    board_min_x, board_min_y, board_max_x, board_max_y = self.getRect()
    return board_min_x < point_x and point_x < board_max_x and board_min_y < point_y and point_y < board_max_y

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


