from random import random

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
