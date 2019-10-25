# TODO: consider combining these classes with "env.py" into a "oz_world.py"

from random import random

class Movable:

    def getId(self):
        return self._id

    def setId(self, new_id):
        self._id = new_id

    def getColor(self):
        return self._color

    def getEdgeColor(self):
        return self._edge_color

    def getRadius(self):
        return self._radius

    def getEdgeWidth(self):
        return self._edge_width

    def getCenter(self):
        return self._center

    def moveBy(self, translation, bounds): # could use insets instead of bounds
        current_x, current_y = self._center
        tx, ty = translation
        x, y = current_x + tx, current_y + ty
        min_x, min_y, max_x, max_y = bounds
        if x < min_x:
            x = min_x
        if y < min_y:
            y = min_y
        if x > max_x:
            x = max_x
        if y > max_y:
            y = max_y

        kx, ky = x - current_x, y - current_y
        self._center = x, y
        return kx, ky # return the actual change

    def moveTo(self, target):
        self._center = target

    def __init__(self, index, color, edge_color, radius, edge_ratio, center):
        self._id = index
        self._color = color
        self._edge_color = edge_color
        self._radius = radius
        self._edge_width = radius * edge_ratio
        self._center = center


class Stone(Movable):
    def __init__(self, index, isBlack, color, edge_color, radius, edge_ratio, center):
        super().__init__(index, color, edge_color, radius, edge_ratio, center)
        self._isBlack = isBlack

    def isBlack(self):
        return self._isBlack


class Agent(Movable): # Note how stones are equivalent to super of agents, evolutionarily speaking ;-)

    def getCurrentObservation(self):
        return self._observation

    def setCurrentFeel(self,feel):
        self._observation.setFeel(feel)

    def setCurrentEnvImage(self, env_image):
        self._observation.setEnvImage(env_image)

    def getCurrentAction(self):
        return self._action

    def setCurrentAction(self, action):
        self._action = action

    def updateObservation(self, observation):
        self._observation = observation

    def decideNextAction(self, observation):
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
        if act_randomly:
            self._press = random() < 0.2 # 20% of time
            self._move = 0.01 * (random() - 0.5), 0.01 * (random() - 0.5) # at most 1cm in one direction at a time
        else:
            self._press = press
            self._move = move


class Observation:

    FEELS_NOTHING = 0
    FEELS_BACKGROUND = 1
    FEELS_BOARD = 2
    FEELS_STONE = 3

    def getFeel(self):
        return self._feel

    def setFeel(self, feel):
        self._feel = feel

    def getKinesthetic(self):
        return self._kinesthetic

    def setKinesthetic(self, kinesthetic):
        self._kinesthetic = kinesthetic

    def getEnvImage():
        return self._env_image

    def setEnvImage(self, env_image):
        self._env_image = env_image

    def __init__(self, feel=None, env_image=None, kinesthetic=None):
        self._feel = feel
        self._env_image = env_image
        self._kinesthetic = kinesthetic

