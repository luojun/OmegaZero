# TODO: understand how to do modules
# TODO: understand how to do from ... import ...
# TODO: understand the convention for random and sqrt
# TODO: move test to tests/
# TODO: understand convention for relationship between Python classes and Python files vs. Java
# TODO: follow Python style guide
# TODO: Python's way with setters and getters

from random import random
from math import sqrt

from board import Board
from agent import Agent
from stone import Stone
import observation

class World:

    # TODO: implement these properties on top of Config properties

    @property
    def background_color(self):
        return self._background_color

    @property
    def size(self):
        return self._size

    @property
    def bounds(self):
        return self._bounds

    @property
    def board(self):
        return self._board

    @property
    def stone_radius(self):
        return self._stone_radius

    @property
    def stone_colors(self):
        return self._stone_colors

    @property
    def stone_edge_colors(self):
        return self._stone_edge_colors

    @property
    def stone_edge_width(self):
        return self._get_stone_edge_width()

    @property
    def stones(self):
        return self._stones

    @property
    def agent_radius(self):
        return self._agent_radius

    @property
    def agent_color(self):
        return self._agent_color

    @property
    def agent_edge_color(self):
        return self._agent_edge_color

    @property
    def agent_edge_width(self):
        return self._get_agent_edge_width()

    @property
    def agents(self):
        return self._agents

    @property
    def holdings(self):
        return self._holdings

    def _get_stone_edge_width(self):
        return self.stone_radius * self._stone_edge_width_ratio

    def _get_agent_edge_width(self):
        return self.agent_radius * self._agent_edge_width_ratio

    def tick(self, gui_agent_action=None, world_image=None):
        holdings = self.holdings
        agents = self.agents

        # single thread: agents are all synchronized ...

        # receive the rendered world image here because we defer that to the GUI/Pygame
        for agent in agents: # single thread: agents are all synchronized ...
            agent.current_world_image = world_image

        # TODO: config for the number of gui_agents
        agents[0].current_action = gui_agent_action

        # Move agents and the stones held then apply touch action.
        for agent in agents:
            kinesthetic = agent.move_by(agent.current_action.move, self.bounds)
            stone_held = holdings[agent.index]
            if stone_held is not None:
                stone_held.move_to(agent.center)
            agent.current_observation.kinesthetic = kinesthetic

        # Apply touch and update tactile feedback.
        for agent in agents:
            touch = agent.current_action.touch
            stone_held = holdings[agent.index]
            if not touch:
                stone_held = None
            elif stone_held is None:
                stone_held = self._pick_up(agent.center, agent.radius)
            holdings[agent.index] = stone_held

            if not touch:
                agent.feel = observation.FEELS_NOTHING
            elif stone_held:
                agent.feel = observation.FEELS_STONE
            elif self.board.is_on_board(agent.center):
                agent.feel = observation.FEELS_BOARD
            else:
                agent.feel = observation.FEELS_BACKGROUND

        # TODO: config for the number of gui_agents
        for agent in agents[1:]:
            agent.decide_next_action(agent.current_observation)


    def __init__(self, configs):
        size_x = configs.world_size_x
        size_y = configs.world_size_y
        board_lines = configs.board_number_of_lines
        self._background_color = configs.world_background_color
        self._size = (size_x, size_y)
        self._center = center_x, center_y = 0.0, 0.0
        min_x, min_y = center_x - size_x / 2, center_y - size_y / 2
        max_x, max_y = center_x + size_x / 2, center_y + size_y / 2
        self._bounds = (min_x, min_y, max_x, max_y)
        self._board = Board(configs, self._size, self._center, board_lines)

        board_inset_x, board_inset_y = self._board._inset
        stone_size = min(board_inset_x, board_inset_y) * configs.stone_size_ratio
        self._stones = self._init_stones(configs, stone_size)

        agent_size = stone_size * configs.agent_size_ratio
        self._agents = self._init_agents(configs, agent_size)
        # an agent can hold at most 1 stone
        self._holdings = [None for n in range(configs.number_of_agents)]

    def _init_stones(self, configs, stone_size):
        self._stone_radius = stone_size / 2
        self._stone_colors = (configs.stone_color_black, configs.stone_color_white)
        self._stone_edge_colors = (configs.stone_edge_color_black, configs.stone_edge_color_white)
        self._stone_edge_width_ratio = configs.stone_edge_width_ratio

        size_x, size_y = self._size
        min_x, min_y, _, _ = self._bounds

        stones = []
        for index in range(configs.number_of_stones):
            color_index = index % 2
            is_black = (color_index == 0)
            stone_color = self._stone_colors[color_index]
            stone_edge_color = self._stone_edge_colors[color_index]
            stone_center = (
                min_x + self._stone_radius + random() * (size_x - stone_size),
                min_y + self._stone_radius + random() * (size_y - stone_size)
            )
            stone = Stone(index, is_black, stone_color, stone_edge_color,
                          self._stone_radius, self._stone_edge_width_ratio, stone_center)
            stones.append(stone)
        return stones

    def _init_agents(self, configs, agent_size):
        self._agent_radius = agent_size / 2
        self._agent_color = configs.agent_color
        self._agent_edge_color = configs.agent_edge_color
        self._agent_edge_width_ratio = configs.agent_edge_width_ratio

        size_x, size_y = self._size
        min_x, min_y, _, _ = self._bounds

        agents = []
        for index in range(configs.number_of_agents):
            agent_center = (
                min_x + self._agent_radius + random() * (size_x - agent_size),
                min_y + self._agent_radius + random() * (size_y - agent_size)
            )
            agent = Agent(index, self._agent_color, self._agent_edge_color,
                          self._agent_radius, self._agent_edge_width_ratio, agent_center)
            agents.append(agent)
        return agents

    def _pick_up(self, center, radius):
        picked = None
        for stone in self.stones:
            center_x, center_y = center
            stone_x, stone_y = stone.center
            diff_x = stone_x - center_x
            diff_y = stone_y - center_y
            distance = sqrt(diff_x * diff_x + diff_y * diff_y)
            if distance < radius:
                picked = stone
                break

        if picked is not None:
            # bring picked stone to front and push everyone else over by one
            stones = self.stones
            for i in range(picked.index, 0, -1):
                stones[i] = stones[i - 1]
                stones[i].index = i
            picked.index = 0
            stones[0] = picked

        return picked
