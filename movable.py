from random import random

class Movable:

  def getId(self):
    return self._id

  def getColor(self):
    return self._color

  def getRadius(self):
    return self._radius

  def getCenter(self):
    return self._center

  def moveBy(self, translation, bounds): # could use insets instead of bounds
    x, y = self._center
    tx, ty = translation
    x, y = x + tx, y + ty
    min_x, min_y, max_x, max_y = bounds
    radius = self.getRadius()
    if x < min_x + radius:
      x = min_x + radius
    if y < min_y + radius:
      y = min_y + radius
    if x > max_x - radius:
      x = max_x - radius
    if y > max_y - radius:
      y = max_y - radius
    self._center = x, y

  def moveTo(self, target):
    self._center = target

  def __init__(self, index, color, radius, center):
    self._id = index
    self._color = color
    self._radius = radius
    self._center = center


class Stone(Movable):
  pass

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

  def __init__(self, index, color, radius, center):
    super().__init__(index, color, radius, center)
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

  def getEnvImage():
    return self._env_image

  def setEnvImage(self, env_image):
    self._env_image = env_image

  def __init__(self, feel=None, env_image=None):
    self._feel = feel
    self._env_image = env_image

