import numpy as np

from ..agent.agent import Agent
from ..agent.action import Action

# change env code to use updateObservation as a synchronized update of observation for the agent
#
# affordance0 -- learn to predict arrival of effect of self action
#   - take action randomly
#     - action commands are accessible ... is this reasonable ...
#     - in the future: rhythmically take action ... faster and slower; may need action pattern generator
#   - constantly measure rhythm and amount of change
#     - amount: integration over space and time
#       - parameter: temporal scale (temporal horizon)
#       - no spatial differentiation at the beginning, thus integrate the whole 2D space
#       - modality specific
#     - NB: on and off is about thresholding of amount ...
#     - NB: rhythm is cyclic change of amount
#   - constantly predict amount of change
#     - do cross-modality prediction rather than predicting from action command, at least in the beginning
#   - if predicted change diverges from observed change, then raise level of novelty
#
#   - trouble: there is no natural time scale ... unlike if there is inertia and friction ... all effect is instantaneous
#   - however: actions and sensory feedback are different "channels", thus prediction is cross channel.
#   - however: memory decay will allow a horizon ... the time scale is not natural, due to physics, but is there.

class Agent0(Agent):

    def decide_next_action(self, observation):
        self._actuals = self._actual_change(observation)
        self._all_actuals.append(self._actuals)

        if self._predictions is not None and self._last_action is not None:
            self._learn(self._predictions, self._actuals, self._last_action)

        self.current_action = Action(None, None, True) # random policy

        self._last_action = self.current_action.vector
        self._last_action[0] /= 0.01
        self._last_action[1] /= 0.01
        self._predictions = self._predict(observation, self._last_action)
        self._all_predictions.append(self._predictions)

    @property
    def all_predictions(self):
        return self._all_predictions

    @property
    def all_actuals(self):
        return self._all_actuals

    @property
    def weights(self):
        return self._weights

    def __init__(self, index, center):
        super().__init__(index, center)
        self._weights = np.zeros((4, 3))
        self._learning_rate = 0.01
        self._last_image = None
        self._last_feel = None
        self._predictions = None
        self._last_action = None
        self._all_predictions = []
        self._all_actuals = []

    def _actual_change(self, observation):
        if self._last_image is not None:
            diff = observation.world_image - self._last_image
        else:
            diff = observation.world_image - observation.world_image
        visual_change = np.sum(diff) / diff.size # should be between 0 and 255

        if self._last_feel is not None:
            tactile_change = 0 if self._last_feel is observation.feel else 1
        else:
            tactile_change = 0

        kx, ky = observation.kinesthetic
        kinesthetic = (kx / 0.01, ky / 0.01) # normalization ...

        self._last_image = observation.world_image
        self._last_feel = observation.feel

        return np.asarray((visual_change,) + (tactile_change,) + kinesthetic).reshape(-1, 1)

    def _predict(self, observation, action_vector):
        predictions = np.matmul(self._weights, action_vector)
        return predictions

    def _learn(self, predicted, actuals, action_vector):
        errors = actuals - predicted
        self._weights += self._learning_rate * np.matmul(errors,  action_vector.transpose())
