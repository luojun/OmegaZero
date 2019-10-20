from movable import Agent

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

  def decideNextAction(self, observation):
    self._action = Action(None, None, True)

  def __init__(self, index, color, radius, center):
    super.__init__(self, index, color, radius, center)

