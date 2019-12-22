## Affordance0 -- learn to do cross-modal prediction based on effect of random self action

[ ] collect data first
    [ ] process image difference first also
[ ] do predictive learning offline ...
[ ] consider polar action ... Is this cheating?

- take action randomly
  - action commands are accessible ... is this reasonable ...
  - in the future: rhythmically take action ... faster and slower; may need action pattern generator
- constantly measure rhythm and amount of change
  - amount: integration over space and time
    - parameter: temporal scale (temporal horizon)
    - no spatial differentiation at the beginning, thus integrate the whole 2D space
    - modality specific
  - NB: on and off is about thresholding of amount ...
  - NB: rhythm is cyclic change of amount
- constantly predict amount of change
  - do cross-modality prediction rather than predicting from action command, at least in the beginning
- if predicted change diverges from observed change, then raise level of novelty

- trouble: there is no natural time scale ... unlike if there is inertia and friction ... all effect is instantaneous
- however: actions and sensory feedback are different "channels", thus prediction is cross channel.
- however: memory decay will allow a horizon ... the time scale is not natural, due to physics, but is there.

### Code

1. V: spatially sum up amount of visual change: # of pixels different between two consecutive observations
2. K: kinesthetic feedback: use vector length, because kinesthetic feedback is differential feedback
3. T: tactile feedback change (0, +1, -1): sum of absolute values: 0 -- no change, 1 -- on or off, 2 -- texture boundary

- What's the function here? f(V, K, T) -> V, K, T
- T == 2 strongly predicts V and K
- T == 1 strongly predicts V (need to change implementation such that all touching agents are rendered)
- T == 0 predicts nothing about V and K
- V low predicts K low and T low
- V high predicts K hight and T high
- K low predicts V low
- K high predicts V high, but plateaus after a threshold

- What is the temporal profile of f? Purely cross-modal would mean no time. Is this because the agents are in synch with env dynamics? Maybe. Maybe we should go asynchronous from the start?

- How to implement f?

