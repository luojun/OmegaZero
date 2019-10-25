# TODO: understand how to do modules
# TODO: understand how to do from ... import ...
# TODO: understand the convention for random and sqrt
# TODO: move test to tests/
# TODO: understand convention for relationship between Python classes and Python files vs. Java
# TODO: follow Python style guide
# TODO: Python's way with setters and getters

from random import random
from math import sqrt

from movable import Agent
from movable import Stone
from movable import Observation 

import config

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

    def getStoneRadius(self):
        return self._stone_radius

    def getStoneColorBlack(self):
        return self._stone_color_black

    def getStoneColorWhite(self):
        return self._stone_color_white

    def getStoneEdgeColorBlack(self):
        return self._stone_edge_color_black

    def getStoneEdgeColorWhite(self):
        return self._stone_edge_color_white

    def getStoneBlackEdgeWidthRatio(self):
        return self._stone_black_edge_width_ratio

    def getStoneWhiteEdgeWidthRatio(self):
        return self._stone_white_edge_width_ratio

    def getAgentEdgeWidthRatio(self):
        return self._agent_edge_width_ratio

    def getStones(self):
        return self._stones

    def getAgentRadius(self):
        return self._agent_radius

    def getAgentColor(self):
        return self._agent_color

    def getAgentEdgeColor(self):
        return self._agent_edge_color

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
            kinesthetic = agent.moveBy(agent.getCurrentAction().move(), self.getBounds())
            stoneHeld = holdings[agent.getId()]
            if stoneHeld is not None:
                stoneHeld.moveTo(agent.getCenter())
            agent.getCurrentObservation().setKinesthetic(kinesthetic)

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


    def __init__(self, size_x=config.ENVIRONMENT_SIZE_X, size_y=config.ENVIRONMENT_SIZE_Y, board_lines=4, number_of_stones=10, number_of_agents=2): # 4, 10, 2 for tic-tac-toe
        self._background_color = config.ENVIRONMENT_BACKGROUND_COLOR
        self._size = (size_x, size_y)
        self._center = center_x, center_y = 0.0, 0.0
        min_x, min_y = center_x - size_x / 2, center_y - size_y / 2
        max_x, max_y = center_x + size_x / 2, center_y + size_y / 2
        self._bounds = (min_x, min_y, max_x, max_y)
        self._board = Board(self._size, self._center, board_lines)

        board_inset_x, board_inset_y = self._board._inset
        stone_size = min(board_inset_x, board_inset_y) * config.STONE_SIZE_RATIO
        self._stones = self._init_stones(number_of_stones, stone_size)

        agent_size = stone_size * config.AGENT_SIZE_RATIO
        self._agents = self._init_agents(number_of_agents, agent_size)
        self._holdings = self._init_holdings(number_of_agents) # for now, one agent can hold at most one stone

    def _init_stones(self, number_of_stones, stone_size):
        self._stone_radius = stone_size / 2
        self._stone_color_black = config.STONE_BLACK_COLOR
        self._stone_edge_color_black = config.STONE_BLACK_EDGE_COLOR
        self._stone_black_edge_width_ratio = config.STONE_BLACK_EDGE_WIDTH_RATIO
        self._stone_color_white = config.STONE_WHITE_COLOR
        self._stone_edge_color_white = config.STONE_WHITE_EDGE_COLOR
        self._stone_white_edge_width_ratio = config.STONE_WHITE_EDGE_WIDTH_RATIO

        center_x, center_y = self._center
        size_x, size_y = self._size
        min_x, min_y, _, _ = self._bounds

        stones = []
        for index in range(number_of_stones):
            isBlack = index % 2 == 0 
            stone_color = (self._stone_color_black if isBlack else self._stone_color_white)
            stone_edge_color = (self._stone_edge_color_black if isBlack else self._stone_edge_color_white)
            stone_edge_ratio = (self._stone_black_edge_width_ratio if isBlack else self._stone_white_edge_width_ratio)
            stone_center = (
                min_x + self._stone_radius + random() * (size_x - stone_size),
                min_y + self._stone_radius + random() * (size_y - stone_size)
            )
            stone = Stone(index, isBlack, stone_color, stone_edge_color, self._stone_radius, stone_edge_ratio, stone_center)
            stones.append(stone)
        return stones

    def _init_agents(self, number_of_agents, agent_size):
        self._agent_radius = agent_size / 2
        self._agent_color = config.AGENT_COLOR
        self._agent_edge_color = config.AGENT_EDGE_COLOR
        self._agent_edge_width_ratio = config.AGENT_EDGE_WIDTH_RATIO

        center_x, center_y = self._center
        size_x, size_y = self._size
        min_x, min_y, _, _ = self._bounds

        agents = []
        for index in range(number_of_agents):
            agent_center = (
                min_x + self._agent_radius + random() * (size_x - agent_size),
                min_y + self._agent_radius + random() * (size_y - agent_size)
            )
            agent = Agent(index, self._agent_color, self._agent_edge_color, self._agent_radius, self._agent_edge_width_ratio, agent_center)
            agents.append(agent)
        return agents

    def _init_holdings(self, number_of_agents):
        return [None for n in range(number_of_agents)]

    def _pickUp(self, center, radius):
        picked = None
        for stone in self.getStones():
            x, y = center
            stone_x, stone_y = stone.getCenter()
            d = sqrt((stone_x - x) * (stone_x - x) + (stone_y - y) * (stone_y - y))
            if d < radius:
                picked = stone
                break

        if picked is not None:
            # bring picked stone to front and push everyone else over by one
            stones = self.getStones()
            index = picked.getId()
            for i in range(index, 0, -1):
                stones[i] = stones[i-1]
                stones[i].setId(i)
            picked.setId(0)
            stones[0] = picked

        return picked
            

class Board:

    def getColor(self):
        return self._color

    def getSize(self):
        return self._size

    def getRect(self):
        return self._rect

    def getLineColor(self):
        return self._line_color

    def getLineWidth(self):
        return self._line_width

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
        self._color = config.BOARD_COLOR
        self._line_color = config.BOARD_LINE_COLOR

        environment_size_x, environment_size_y = environment_size
        environment_center_x, environment_center_y = environment_center
        self._size = board_size_x, board_size_y = environment_size_x * config.BOARD_SIZE_X_RATIO, environment_size_y * config.BOARD_SIZE_Y_RATIO # allow size_x and size_y to be different
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
        self._line_width = config.BOARD_LINE_WIDTH_RATIO * board_inset_x # Differentiate x and y in version 5.0 ;-)

        x_lines = [((board_line_min_x, board_line_min_y + board_line_inc_y * n), (board_line_max_x, board_line_min_y + board_line_inc_y * n)) for n in range(board_lines)]
        y_lines = [((board_line_min_x + board_line_inc_x * n, board_line_min_y), (board_line_min_x + board_line_inc_x * n, board_line_max_y)) for n in range(board_lines)]
        self._lines = x_lines + y_lines


