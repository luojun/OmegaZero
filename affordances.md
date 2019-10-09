# Learning Affordances as Commonsense Knowledge

If we go slow enough, Oz is more than adequate for exploring the conceptual structure underlying the "commonsense knowledge" of the domain of Go-like board games, for understanding the necessary skills the coordination of which give us the cognitive architecture needed for the ability of "learning from demonstration". The following musings suggest that issues of latency, directional alignment, localization, metric correspondence, cross-modal correspondence etc are all implicated. What is the learning architecture -- components, representation, and algorithms -- needed for a successful coordination of all these aspects through learning? That's the question we want to investigate. That, we believe, is also a core part of the question about how "commonsense knowledge" may be structured and learned.

The initial articulation below is largely from the perspective of affordances, from the perspective of building towards learning affordances. J.J.Gibson's theory of affordance, Jean Piaget's account of sensorimotor development, and the idea of General Value Functions (GVFs) from reinforcement learning research are centrally at play here. 

## 1. Visual and tactile latency -- time 0: embeddedness

For simplicity of discussion, let's assume there is no delay between motion command and kinesthetic feedback. We may then ask how kinesthetic feedback and visual feedback are correlated to enable estimation of latency of visual feedback. "Latency" may not be the right word here. What matters is the temporal regularity in terms of the relationship between when an action is taken by the agent and when the impact of the action is perceived by the agent visually. The sense of latency or rather regularity here grounds a general sense for the agent that its action does impact the environment or at least it does impact the agent's own body (i.e. cursor). Similar things can be said about the latency or regularity in tactile feedback. In this sense, the temporal regularity we are concerned about is not unlike the situation with rhythmic finger sucking in babies, wherein the coordinated rhythms of sucking and feeling of being sucked embodies the temporal regularity.

To capture the regularity here, we may use one GVF to predict *gross visual motion* based on kinesthetic feedback and another GVF to predict *gross tactile change* based on kinesthetic feedback.

Now, if the action command is also accessible as such, i.e. independent of and prior to the availability of the kinesthetic feedback, we can use GVFs to make similar predictions from action commands. (NB: it's my sense that higher level or cortical action commands, i.e. intentions, could be accessible as such, but not so much lower-level or spinal commands, i.e. reactions.)

Naturally, we could expect these GVFs to capture the actual *rhythm* as reflected in the feedbacks of the *ego-action*. This is important because the rhythmic regularity under the agent's control is the best indication that the agent is in control.

Here, we can also see how such predictions as embody a kind of perceived *invariance*, which is the invariance of the general effectiveness of action regardless of where and how the action is taken. Such GVFs and the "nexting" based on them are probably at the core of the agent's sense that it's a little creature appropriately embedded in Oz.

From such a perspective, we can also see how this may be useful? It is super useful for system self-check: (1) if predictions from action command to gross visual motion (moving the cursor at all if not also the stone held) or gross tactile change (from not touching anything to touching something) fails, it means the agent's control has come apart from its body or environment; (2) if predictions from kinesthetic feedback to environmentally rooted feedback fails, it means the agent's body has come apart from its environment (e.g. the agent may be skidding or in total darkness); (3) in the less dramatic cases, if the latency between action and gross visual motion increases, the agent is in a position to suspect some sort of computational lag or extra mechanical play was somehow introduced in the overall system. Super useful things for real world robotics!

Finally, it should be noted that one place where the predictions will necessarily be irregular is when the agent tries to move against the bounds of Oz. While this counts as an instance of (2) above and thus the agent's sense that it's at the bounds will benefit from the GVF predictions here, the full proper treatment of perception at the bounds of Oz will require more capacities unpacked below.

## 2. Visual action orientation -- space 1: action-vision directional alignment

With the temporal regularity capturing the fundamental embeddedness of the agent in Oz, we can move on to consider the specifically spatial aspects of the agent-environment relationship. A first challenge we face here is establishing the *directional* coordination between visual feedback and action.

Assume motion command is in robot-base coordinateas, as in a SCARA or Cartesian robot, but the camera axis may rotate relative to the robot-base. To cope with such a change, the agent will need to learn to correlate kinesthetic feedback *direction* and visual feedback *direction*.

To establish the coordination, we could use a GVF that predicts the visual "direction" from the kinesthetic "direction". Such "directions" could be represented with normalized unit vectors. We put "direction" in scare quotes because, as will be illustrated below, at this level of coordination the agent does not yet have an adequate sense of space for these unit vectors to be its mental representation of spatial directions. For now what matters is that the preditive relation is systematic and can be captured by a GVF.

From a first person perspective, the situation we are dealing with is like our waving our own hand in a particular direction leads us to expect our seeing that hand to visually move in a specific direction. That we have such expectation is why a new pair of glasses make things look weird. That we are able to quickly adapt to a new pair of glasses mean we have the right kind of plasticity for coping with the underlying shifts that disrupt the normal coordination. This kind of plasticity also allow humans to cope with the more [dramatic case of inverting lens](https://en.wikipedia.org/wiki/George_M._Stratton#Wundt's_lab_and_the_inverted-glasses_experiments).

The kind of invariance that is needed through the coordinated prediction is invariance over shifts between eye/camera (or rather the optical path, to be precise) and body base. The plasticity or flexibility that we can build into the GVF predictor will allow us to handle rotational changes without explicit calibration.

As with other aspects of coordination, the bounds of the Oz world are always special. But that prediction does not work normally, at least along some dimension is actually the signature event that tells the agent that it's at the boundary. Going forward, we'll neglect to comment on the specialness of the bounds.

Another point worth noting is that we are assuming that we use some hand-crafted cumulants (the unit vectors) to build the GVF predictor. This is an example of the kind of "generic or commonsense knowledge" that we are for now building into the agent, because, for now, we are doing our exploration [ideally](README.md#ideally) rather than [idealistically](README.md#idealistically).

## 3. Visual ego localization -- space 2: where am I?

This should be secondary to the directional alignment ...

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

## 4. Where to travel and when to arrive -- space 3: metric correspondence

Should this be secondary to ego localization?

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

## 5. What do I feel?

- Another "sensory" modality: tactile feedback.
- Tactile latency is a factor: learn to trigger a tactile change through a "press" or "touch" action.
- No tactile orientation.

- Nexting?
- GVF to predict how I feel given my action, past feeling, motion, and visual input ...

## 6. Where will I feel what? -- tactile map

- Field of possible tactile feedback.
- Could be based solely on map built from dead reckoning.

- The same for feeling ... similar to vision ...
- GVF field ... or feeling as a GVF of color ... from color to feeling: esp. white and black.

## 7. The looks of how things feel -- cross-modal visual-tactile map and the rise of space

- Alignment of tactile field and visual field
- Multi-feature field

- Join these two fields ... cross-modality GVF field ...
- Two inputs, one output. The rise of space.

- This is important for dealing with board rotation, or rotation of the board relative to the SCARA robot's base.

## 8. Where are the stones? -- stoneness as a particular kind of spatially distributed affordance

- Cross-modality feature placing of stoneness.
- So far no goal-oriented actions, all through correlations ...
- Learn all of the above through unsupervised predictive learning ...

- GVFs of stone color???

## 9. Moving stones -- let the play begin

- Sequential decision making now ...
- Learn to differentiate individual stones ...

- Now we can specify the task of moving stones arounds ... in a goal oriented way ... with enough resilience and flexibility.

## ... and so on ...

We have charted a route for building up all the way to a level of complexity where stones could be played with. The sense is that such complexity is close to be within the reach of contemporary AI techniques and computational capacity. What is needed to to walk the route and fashion the necessary new techniques along the way. However, what is *not* going to work, i.e. what is not going to allow us to succeed at learning to play, would be to trivialize any crucial part of the complexity so that our AI ideas, agents, or robots will just "work". Indeed, they may work and win Go games and drive cars, but they won't be able to play in Oz.
