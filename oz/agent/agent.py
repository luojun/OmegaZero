from world import movable
from agent import observation
from agent import action

class Agent(movable.Movable):

    @property
    def current_observation(self):
        return self._observation

    @current_observation.setter
    def current_observation(self, observation):
        self._observation = observation

    @property
    def current_feel(self):
        return self._observation.feel

    @current_feel.setter
    def current_feel(self, feel):
        self._observation.feel = feel

    @property
    def current_word_image(self):
        return self._observation.word_image

    @current_word_image.setter
    def current_word_image(self, word_image):
        self._observation.word_image = word_image

    @property
    def current_action(self):
        return self._action

    @current_action.setter
    def current_action(self, action):
        self._action = action

    def decide_next_action(self, observation):
        self._action = action.Action(None, None, True)

    # TODO: simplify this through config
    def __init__(self, index, color, edge_color, radius, edge_ratio, center):
        super().__init__(index, color, edge_color, radius, edge_ratio, center)
        self._observation = observation.Observation()
        self._action = action.Action(None, None, True)
