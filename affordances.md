## Varieties of Affordance Fields

If we go slow enough, Oz is more than adequate for exploring the concepctual structure underlying the "commonsense knowledge" of a domain of Go-like board games, for understanding the construction of the various skills the coordination of which give us the cognitive architecture needed for the eventual ability of "learning from demonstration".

As should be clear below, it also is a "site" for much cross-cutting concerns and cross-cutting registrations, because the shared base-level "I/O" and base-level "physics" are quite stable and what makes things interesting is the varities of interests we take in the "site".

### 1. Visual latency -- time

- Assume there is no delay between motion command and kinesthetic feedback.
- Correlate kinesthetic feedback and visual feedback to estimate latency of visual feedback.
- Very much like rhythmic finger sucking in babies.
- This could be a field where different places in the visual scene has different latency.
- This could be related to visual orientation and visual localization below.
- ... How visual change at all is expected given motion -- overall timing ... learn the fact that there is no latency (or systematic reliable latency) between my action and visual feedback on my action
- ... Similarly with tactile feedback
- ... Boundary is special

### 2. Visual orientation -- space 1: action-vision alignment

- Assume motion command is in robot-base coordinateas, as in a SCARA robot.
- Correlate kinesthetic feedback *direction* and visual feedback *direction* to estimate orientation.
- Visual orientation here is part of the transformation between motion command coordinates and visual feedback coordinates.
- But this one could also be a field if the transformations differ at different parts of the visual scene.
- This is related to visual localization below.
- This is important for dealing with board rotation, or rotation of the board relative to the SCARA robot's base.
- ... How motion direction correlates with visual change direction.
- ... Boundary is special

### 3. Visual localization -- space 2, where am I?

- A visual field of where I am, a field with a single or possibly multiple activation peaks for where I could possibly be in the visual field.
- This one settles the locus of action in the visual scene.
- ... How motion correlates with localized visual changes
- ... Boundary is special

### 4. Where to travel and when to arrive -- space 3, metric correspondence

- This one settles the mapping of motion command to visual scene globally.
- This one requires integration of visual orientation and visual localization.
- It further requires metric correspondence for the two independently controllable action/motion dimensions with visible changes of ego location.
- This will be important for dealing with differential scaling.
- If the agent is to wear a new pair of glasses, the adaptation here is relevant.
- Yet another field, centered around where the agent is, and spreads out according to how much time it takes to arrive where.
- ... GVFs in space ...
- ... Boundary is special

### 5. How do I feel?

- Another "sensory" modality: tactile feedback.
- Tactile latency is a factor: learn to trigger a tactile change through a "press" or "touch" action.
- No tactile orientation.

### 6. Where will I feel what?

- Field of possible tactile feedback.
- Could be based solely on map built from dead reckoning.

### 7. The looks of how things feel -- cross modality

- Alignment of tactile field and visual field
- Multi-feature field

### 8. Where are the stones?

- Cross-modality feature placing of stoneness.
- So far no goal-oriented actions, all through correlations ...

### 9. Moving stones

- Sequential decision making now ...
- Learn to differentiate individual stones ...


### ... and so on ...

