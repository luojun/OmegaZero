## Varieties of Affordance Fields

If we go slow enough, Oz is more than adequate for exploring the conceptual structure underlying the "commonsense knowledge" of a domain of Go-like board games, for understanding the construction of the various skills the coordination of which give us the cognitive architecture needed for the eventual ability of "learning from demonstration".

As should be clear below, the Oz environment is also a "site" for many cross-cutting concerns and cross-cutting registrations. While the shared base-level "I/O" and base-level "physics" are quite simple and stable, what make things interesting is how all the relevant aspects converge on the same "site": time, directional alignment, localization, metric correspondence, cross-modal correspondence etc. What is the learning architecture -- components, representation, and algorithms -- needed for a successful coordination of all these aspects? That's the question we want to investigate.

### 1. Visual latency -- time

- Assume there is no delay between motion command and kinesthetic feedback.
- Correlate kinesthetic feedback and visual feedback to estimate latency of visual feedback.
- Very much like rhythmic finger sucking in babies.
- This could be a field where different places in the visual scene has different latency.
- This could be related to visual orientation and visual localization below.
- ... How visual change at all is expected given motion -- overall timing ... learn the fact that there is no latency (or systematic reliable latency) between my action and visual feedback on my action
- ... Similarly with tactile feedback
- ... Boundary is special
- Maybe we need a field of latency? Or maybe not? Maybe the latency should just be an aspect of the overall field of visual feedback? No, that doesn't seem to be right.
- Latency could be object-specific. It's one aspect of the concerns. It's a concern. We can attach the concern to the object or the sujbect, the ego. Maybe using a cumulant.

- What kind of invariance is this? Visual latency regardless of action. Also regardless of location? Is this invariance a property of the vision channel?
- What sort of flexibility does this enable? Anywhere latency estimates?
- How is this useful? Control of timing? No necessarily directly useful in the current Oz setup.

- Estimate temporal correlation of *gross motion* and *ego-action*. Rhythm if possible.
- GVF of gross motion. Impulse repnose ...

### 2. Visual orientation -- space 1: action-vision alignment

- Assume motion command is in robot-base coordinateas, as in a SCARA robot.
- Correlate kinesthetic feedback *direction* and visual feedback *direction* to estimate orientation.
- Visual orientation here is part of the transformation between motion command coordinates and visual feedback coordinates.
- But this one could also be a field if the transformations differ at different parts of the visual scene.
- This is related to visual localization below.
- This is important for dealing with board rotation, or rotation of the board relative to the SCARA robot's base.
- ... How motion direction correlates with visual change direction.
- ... Boundary is special
- "Direction": again, a concern or an aspect about things in the Oz world. Could be represented with a normalized vector, a unit vector.
- But the point is that the agent moves in a certain direction correlated with the visual transformation of the agent's visible "body".
- Think about coherence in terms of waving hand and seeing hand waved.
- Why a new pair of glasses make things look weird.
- Relative amount / ratio ...

- What kind of invariance is this? Orientation regardless of location?
- How is this useful? So as to have goal orientedness. For example, suppose a direction is specified in terms of where I am and where target is, an action can be derived accordingly. 
- Flexibility? When getting a new pair of glasses? When getting a new pair of motors?

- This is a transformation between visual plane and action vector. About transformation that makes the action vector parallel to the visual plane. These may not be parallel to each other.
- GVFs predicting in the visual plane the direction of change, given some change, given the action/kinesthetic vector and the visual input.

### 3. Visual localization -- space 2, where am I?

- A visual field of where I am, a field with a single or possibly multiple activation peaks for where I could possibly be in the visual field.
- This one settles the locus of action in the visual scene.
- ... How motion correlates with localized visual changes
- ... Boundary is special

- What kind of invariance? Regardless of where I am actually. Always able to localize.
- Needs spatial differentiation ... Here ... and there ... Local motion.
- GVFs predicting where the activity will be next given current activity.
- The fundamental limitation with the GVFs is that they assume that the relevant dimensions are given.
- Play does not assume that.

- GVFs predicting center location
- GVFs predicting feeling and predicting color ...

### 4. Where to travel and when to arrive -- space 3, metric correspondence

- This one settles the mapping of motion command to visual scene globally.
- This one requires integration of visual orientation and visual localization.
- It further requires metric correspondence for the two independently controllable action/motion dimensions with visible changes of ego location.
- This will be important for dealing with differential scaling.
- If the agent is to wear a new pair of glasses, the adaptation here is relevant.
- Yet another field, centered around where the agent is, and spreads out according to how much time it takes to arrive where.
- ... GVFs in space ...
- ... Boundary is special

- Device a set of representations and learning algorithms.
- Calibration free, data labeling free.

- This one is the scaling transformation.
- GVFs predicting where the agent will be when.

### 5. How do I feel?

- Another "sensory" modality: tactile feedback.
- Tactile latency is a factor: learn to trigger a tactile change through a "press" or "touch" action.
- No tactile orientation.

- Nexting?
- GVF to predict how I feel given my action, past feeling, motion, and visual input ...

### 6. Where will I feel what?

- Field of possible tactile feedback.
- Could be based solely on map built from dead reckoning.

- The same for feeling ... similar to vision ...
- GVF field ... or feeling as a GVF of color ... from color to feeling: esp. white and black.

### 7. The looks of how things feel -- cross modality

- Alignment of tactile field and visual field
- Multi-feature field

- Join these two fields ... cross-modality GVF field ...
- Two inputs, one output

### 8. Where are the stones?

- Cross-modality feature placing of stoneness.
- So far no goal-oriented actions, all through correlations ...
- Learn all of the above through unsupervised predictive learning ...

- GVFs of stone color???

### 9. Moving stones

- Sequential decision making now ...
- Learn to differentiate individual stones ...

- Now we can specify the task of moving stones arounds ... in a goal oriented way ... with enough resilience and flexibility.

### ... and so on ...

