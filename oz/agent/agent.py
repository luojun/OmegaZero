from ..world.movable import Movable
from .observation import Observation
from .action import Action

class Agent(Movable):

    @property
    def current_observation(self):
        return self._observation

    @current_observation.setter
    def current_observation(self, new_observation):
        self._observation = new_observation

    @property
    def current_action(self):
        return self._action

    @current_action.setter
    def current_action(self, new_action):
        self._action = new_action

    def decide_next_action(self, current_observation):
        self._action = Action(None, None, True)

    def __init__(self, index, center):
        super().__init__(index, center)
        self._observation = Observation()
        self._action = Action(None, None, True)
