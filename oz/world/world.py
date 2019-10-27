# TODO: understand how to do modules
# TODO: understand the convention for random and sqrt
# TODO: understand convention for relationship between Python classes and Python files vs. Java
# TODO: Python's way with setters and getters

from random import random
from math import sqrt

from world import board
from world import stone
from agent import agent
from agent import observation

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

    # TODO: refactor this one
    def tick(self, gui_agent_action=None, world_image=None):
        holdings = self.holdings
        agents = self.agents

        # single thread: agents are all synchronized ...

        # receive the rendered world image here because we defer that to the GUI/Pygame
        for a in agents: # single thread: agents are all synchronized ...
            a.current_world_image = world_image

        # TODO: config for the number of gui_agents
        agents[0].current_action = gui_agent_action

        # Move agents and the stones held then apply touch action.
        for a in agents:
            kinesthetic = a.move_by(a.current_action.move, self.bounds)
            stone_held = holdings[a.index]
            if stone_held is not None:
                stone_held.move_to(a.center)
            a.current_observation.kinesthetic = kinesthetic

        # Apply touch and update tactile feedback.
        for a in agents:
            touch = a.current_action.touch
            stone_held = holdings[a.index]
            if not touch:
                stone_held = None
            elif stone_held is None:
                stone_held = self._pick_up(a.center, a.radius)
            holdings[a.index] = stone_held

            if not touch:
                a.feel = observation.FEELS_NOTHING
            elif stone_held:
                a.feel = observation.FEELS_STONE
            elif self.board.is_on_board(a.center):
                a.feel = observation.FEELS_BOARD
            else:
                a.feel = observation.FEELS_BACKGROUND

        # TODO: config for the number of gui_agents
        for a in agents[1:]:
            a.decide_next_action(a.current_observation)


    def __init__(self, configs):
        size_x = configs.world.size_x
        size_y = configs.world.size_y
        self._background_color = configs.world.background_color

        self._size = (size_x, size_y)
        self._center = center_x, center_y = 0.0, 0.0
        min_x, min_y = center_x - size_x / 2, center_y - size_y / 2
        max_x, max_y = center_x + size_x / 2, center_y + size_y / 2
        self._bounds = (min_x, min_y, max_x, max_y)

        self._board = board.Board(configs.board, self._size, self._center)

        self._stone_colors = (configs.stone.color_black, configs.stone.color_white)
        self._stone_edge_colors = (configs.stone.edge_color_black, configs.stone.edge_color_white)
        self._stone_edge_width_ratio = configs.stone.edge_width_ratio

        board_inset_x, board_inset_y = self._board._inset
        stone_size = min(board_inset_x, board_inset_y) * configs.stone.size_ratio
        self._stones = self._init_stones(configs.stone, configs.world.number_of_stones,
                                         stone_size)

        agent_size = stone_size * configs.agent.size_ratio
        self._agent_color = configs.agent.color
        self._agent_edge_width_ratio = configs.agent.edge_width_ratio
        self._agents = self._init_agents(configs.agent, configs.world.number_of_agents,
                                         agent_size)

        # an agent can hold at most 1 stone
        self._holdings = [None for n in range(configs.number_of_agents)]

    def _init_stones(self, configs, number_of_stones, stone_size):
        self._stone_radius = stone_size / 2

        size_x, size_y = self._size
        min_x, min_y, _, _ = self._bounds

        stones = []
        for index in range(number_of_stones):
            color_index = index % 2
            is_black = (color_index == 0)
            stone_center = (
                min_x + self._stone_radius + random() * (size_x - stone_size),
                min_y + self._stone_radius + random() * (size_y - stone_size)
            )
            new_stone = stone.Stone(index, is_black, configs, self._stone_radius, stone_center)
            stones.append(new_stone)
        return stones

    def _init_agents(self, configs, number_of_agents, agent_size):
        self._agent_radius = agent_size / 2

        size_x, size_y = self._size
        min_x, min_y, _, _ = self._bounds

        agents = []
        for index in range(number_of_agents):
            agent_center = (
                min_x + self._agent_radius + random() * (size_x - agent_size),
                min_y + self._agent_radius + random() * (size_y - agent_size)
            )
            new_agent = agent.Agent(index, configs, self._agent_radius, agent_center)
            agents.append(new_agent)
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
