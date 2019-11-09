import numpy as np

from random import random

# Instances of this class should be immutable

class Action:

    @property
    def touch(self):
        return self._touch

    @property
    def move(self):
        return self._move

    @property
    def vector(self):
        _touch = 1 if self.touch else 0 # this seems cheating
        array = np.asarray(self._move + (_touch,))
        return array.reshape((array.size, 1))

    def __init__(self, touch, move, act_randomly=False):
        if act_randomly:
            # 20% of time
            self._touch = random() < 0.2
            # at most 1cm in one direction at a time
            self._move = 0.01 * (random() - 0.5), 0.01 * (random() - 0.5)
        else:
            self._touch = touch
            self._move = move
