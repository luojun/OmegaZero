from world import movable
from agent import observation, action

class Agent(movable.Movable):

    @property
    def current_observation(self):
        return self._observation

    @current_observation.setter
    def current_observation(self, new_observation):
        self._observation = new_observation

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
    def current_action(self, new_action):
        self._action = new_action

    def decide_next_action(self, current_observation):
        self._action = action.Action(None, None, True)

    def __init__(self, index, center):
        super().__init__(index, center)
        self._observation = observation.Observation()
        self._action = action.Action(None, None, True)
