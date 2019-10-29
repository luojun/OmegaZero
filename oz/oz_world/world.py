from random import random
from math import sqrt

from oz_world import settings
from oz_world import board
from oz_world import stone
from oz_agent.observation import TactileQuality
from oz_agent.agent import Agent

class World:

    @property
    def settings(self):
        return self._settings

    @property
    def board(self):
        return self._board

    @property
    def stones(self):
        return self._stones

    @property
    def agents(self):
        return self._agents

    @property
    def gui_agent(self):
        return self._agents[0]

    @property
    def holdings(self):
        return self._holdings

    # TODO: refactor this one
    def tick(self, gui_agent_action, renderer):
        holdings = self.holdings
        agents = self.agents

        # single thread: agents are all synchronized ...

        # TODO: config for the number of gui_agents
        agents[0].current_action = gui_agent_action

        # Move agents and the stones held
        for agent in agents:
            kinesthetic = agent.move_by(agent.current_action.move, self.settings.bounds)
            stone_held = holdings[agent.index]
            if stone_held is not None:
                stone_held.move_to(agent.center)
            agent.current_observation.kinesthetic = kinesthetic

        # Apply touch and update tactile feedback.
        agent_radius = self.settings.agent.radius
        for agent in agents:
            touch = agent.current_action.touch
            stone_held = holdings[agent.index]
            if not touch:
                stone_held = None
            elif stone_held is None:
                stone_held = self._pick_up(agent.center, agent_radius)
            holdings[agent.index] = stone_held

            if not touch:
                agent.feel = TactileQuality.nothing
            elif stone_held:
                agent.feel = TactileQuality.stone
            elif self.board.is_on_board(agent.center):
                agent.feel = TactileQuality.board
            else:
                agent.feel = TactileQuality.background

        world_image = renderer.render()

        for agent in agents: # single thread: agents are all synchronized ...
            agent.current_world_image = world_image

        # TODO: config for the number of gui_agents
        for agent in agents[1:]:
            agent.decide_next_action(agent.current_observation)

    def __init__(self, world_settings):
        self._settings = world_settings
        self._board = board.Board(self.settings)
        self._stones = self._init_stones(self.settings)
        self._agents = self._init_agents(self.settings)
        self._holdings = [None] * world_settings.number_of_agents # an agent holds at most 1 stone

    def _init_stones(self, world_settings):
        stone_radius = world_settings.stone.radius
        stone_size = stone_radius * 2
        size_x, size_y = world_settings.size
        min_x, min_y, _, _ = world_settings.bounds

        stones = []
        for index in range(world_settings.number_of_stones):
            color_index = index % 2
            is_black = (color_index == 0)
            stone_center = (
                min_x + stone_radius + random() * (size_x - stone_size),
                min_y + stone_radius + random() * (size_y - stone_size)
            )
            new_stone = stone.Stone(index, stone_center, is_black)
            stones.append(new_stone)
        return stones

    def _init_agents(self, world_settings):
        agent_radius = world_settings.agent.radius
        agent_size = agent_radius * 2
        size_x, size_y = world_settings.size
        min_x, min_y, _, _ = world_settings.bounds

        agents = []
        for index in range(world_settings.number_of_agents):
            agent_center = (
                min_x + agent_radius + random() * (size_x - agent_size),
                min_y + agent_radius + random() * (size_y - agent_size)
            )
            new_agent = Agent(index, agent_center)
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
