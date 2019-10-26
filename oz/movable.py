# TODO: consider combining these classes with "env.py" into a "oz_world.py"

from random import random

class Movable:

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, new_index):
        self._index = new_index

    @property
    def color(self):
        return self._color

    @property
    def edge_color(self):
        return self._edge_color

    @property
    def radius(self):
        return self._radius

    @property
    def edge_width(self):
        return self._edge_width

    @property
    def center(self):
        return self._center

    def move_by(self, translation, bounds): # could use insets instead of bounds
        current_x, current_y = self._center
        delta_x, delta_y = translation
        new_x, new_y = current_x + delta_x, current_y + delta_y
        min_x, min_y, max_x, max_y = bounds
        if new_x < min_x:
            new_x = min_x
        if new_y < min_y:
            new_y = min_y
        if new_x > max_x:
            new_x = max_x
        if new_y > max_y:
            new_y = max_y

        actual_delta_x, actual_delta_y = new_x - current_x, new_y - current_y
        self._center = new_x, new_y
        return actual_delta_x, actual_delta_y # return the actual change

    def move_to(self, target):
        self._center = target

    def __init__(self, index, color, edge_color, radius, edge_ratio, center):
        self._index = index
        self._color = color
        self._edge_color = edge_color
        self._radius = radius
        self._edge_width = radius * edge_ratio
        self._center = center


class Stone(Movable):
    def __init__(self, index, is_black, color, edge_color, radius, edge_ratio, center):
        super().__init__(index, color, edge_color, radius, edge_ratio, center)
        self._is_black = is_black

    @property
    def is_black(self):
        return self._is_black


class Agent(Movable):

    @property
    def current_observation(self):
        return self._observation

    # TODO: figure what's the appropriate way here
    @property
    def current_feel(self):
        return self._observation.feel

    @current_feel.setter
    def current_feel(self, feel):
        self._observation.feel = feel

    @property
    def current_env_image(self):
        return self._observation.env_image

    @current_env_image.setter
    def current_env_image(self, env_image):
        self._observation.env_image = env_image

    @property
    def current_action(self):
        return self._action

    @current_action.setter
    def current_action(self, action):
        self._action = action

    def update_observation(self, observation):
        self._observation = observation

    def decide_next_action(self, observation):
        self._action = Action(None, None, True)

    def __init__(self, index, color, edge_color, radius, edge_ratio, center):
        super().__init__(index, color, edge_color, radius, edge_ratio, center)
        self._observation = Observation()
        self._action = Action(None, None, True)


class Action:

    def press(self):
        return self._press

    def move(self):
        return self._move

    def __init__(self, press, move, act_randomly=False):
        # TODO: move to defaut agent
        if act_randomly:
            # 20% of time
            self._press = random() < 0.2
            # at most 1cm in one direction at a time
            self._move = 0.01 * (random() - 0.5), 0.01 * (random() - 0.5)
        else:
            self._press = press
            self._move = move


class Observation:

    FEELS_NOTHING = 0
    FEELS_BACKGROUND = 1
    FEELS_BOARD = 2
    FEELS_STONE = 3

    @property
    def feel(self):
        return self._feel

    @feel.setter
    def set_feel(self, feel):
        self._feel = feel

    @property
    def kinesthetic(self):
        return self._kinesthetic

    @kinesthetic.setter
    def kinesthetic(self, kinesthetic):
        self._kinesthetic = kinesthetic

    @property
    def env_image(self):
        return self._env_image

    @env_image.setter
    def env_image(self, image):
        self._env_image = image

    def __init__(self, feel=None, image=None, kinesthetic=None):
        self._feel = feel
        self._env_image = image
        self._kinesthetic = kinesthetic
