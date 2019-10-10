# Learning Affordances for Commonsense Knowledge

If we go slow enough, Oz is more than adequate for exploring the conceptual structure underlying the "commonsense knowledge" of the domain of Go-like board games, for understanding the necessary skills the coordination of which give us the cognitive architecture needed for the capacity for "learning from demonstration".

The following musings are just to get the exploration going at the lowest relevant level. It suggests that issues of latency, directional alignment, ego localization, metric correspondence, cross-modal correspondence etc are all implicated, if we are to arrive at sensorimotor abilities of generality. What is the learning architecture -- components, representations, and algorithms -- needed for a successful coordination of all these aspects of general sensorimotor abilities through learning? That is the question we are trying to tackle here. That question, we believe, is also a fundamental part of the broader question about how "commonsense knowledge" may be structured and learned.

The initial articulation below is largely from the perspective of low-level affordances, from the perspective of building from sensorimotor coordination towards the ability to learn more affordances through play. J.J.Gibson's theory of affordance, Jean Piaget's account of sensorimotor development, the idea of General Value Functions (GVFs) from reinforcement learning research, and general robotics and systems considerations are the main perspectives informing our musings here.

## 1. Visual and tactile latency -- time 0: embeddedness

For simplicity of discussion, let's assume there is no delay between motion command and kinesthetic feedback. We may then ask how kinesthetic feedback and visual feedback are correlated to enable estimation of latency of visual feedback. "Latency" may not be the right word here. What matters is the temporal regularity in terms of the relationship between when an action is taken by the agent and when the impact of the action is perceived by the agent visually. The sense of latency or rather regularity here grounds a general sense for the agent that its action does impact the environment or at least it does impact the agent's own body (i.e. its cursor). Similar things can be said about the latency or regularity in tactile feedback. In this sense, the temporal regularity we are concerned about is not unlike the situation with rhythmic finger sucking in babies, wherein the coordinated rhythm of sucking and feeling of being sucked embodies the temporal regularity.

To capture the regularity here, we may use one GVF to predict *gross visual motion* based on kinesthetic feedback and use another GVF to predict *gross tactile change* based on kinesthetic feedback.

Now, if the action command is also accessible as such, i.e. independent of and prior to the availability of the kinesthetic feedback, we can use GVFs to make similar predictions from action commands. (NB: it is very likely that higher level or cortical action commands, i.e. intentions, could be accessible as such, but not lower-level or spinal commands, i.e. reactions.)

Naturally, we could expect these GVFs to predict the arrival of visual or tactile feedback. But predicting visual and tactile feedback according to the actual *rhythm* in the *ego-action* is probably more important. This is because rhythmic changes in the environment or body under the agent's impact is the best indication that the agent is in control of that part of the environment or its own body.

Here, we can also see how such predictions embody a kind of perceived *invariance*, which is the invariance of the general effectiveness of action regardless of where and how the action is taken. Such GVF predictions and the "nexting" based on such predictions are probably at the core of the agent's sense that it's a little creature appropriately embedded in the Oz world in a way such that it can do something to the Oz world, including its own body.

From such a perspective, we can also see how such GVF predictions may be useful. They are super useful for system self-check: (1) if predictions from action command to gross visual motion (moving the cursor at all if not also the stone held) or gross tactile change (from not touching anything to touching something) fails, it means the agent's control has come apart from its body or environment; (2) if predictions from kinesthetic feedback to environmentally rooted feedback fails, it means the agent's body has come apart from its environment (e.g. the agent may be skidding or in total darkness); (3) in the less dramatic cases, if the latency between action and gross visual motion increases, the agent is in a position to suspect some sort of computational lag or extra mechanical play was somehow introduced in the overall system. Super useful things for real world robotics!

Finally, it should be noted that one place where the predictions will necessarily be irregular or different is when the agent tries to move against the boundaries of Oz. While this counts as an instance of (2) above and thus the agent's sense that it's at the boundaries will benefit from the GVF predictions here, a proper treatment of perception at the boundaries of Oz will require understanding more capacities to be unpacked below.

## 2. Visual action orientation -- space 1: action-vision directional alignment

With the temporal regularity capturing the fundamental embeddedness of the agent in Oz, we can move on to consider the specifically spatial aspects of the agent-environment relationship. A first challenge we face here is establishing the *directional* coordination between visual feedback and action.

Let's assume motion command is in robot-base coordinateas, as in a SCARA or Cartesian robot, but the camera axis may undergo rotations relative to the robot-base. To cope with such a change, the agent will need to learn to correlate kinesthetic feedback *direction* and visual feedback *direction*.

To establish the coordination, we could use a GVF that predicts the visual "direction" from the kinesthetic "direction". Such "directions" could be represented with normalized unit vectors. We put "direction" in scare quotes because, as will be illustrated below, at this level of coordination the agent does not yet have an adequate sense of space for these unit vectors to be its mental representation of spatial directions. For now what matters is that the preditive relation tied to the underlying rotational transformation is systematic and can be captured by a GVF.

While the kinesthetic unit vector is easy to obtain from the kinesthetic feedback, which could simply take the form of a two-dimensional vector. The visual unit vector will require a bit of summarizing over the gross visual motion -- practically motion of that cursor under "my" control -- to surface the overall visual motion's direction. The "summarizing" here could be easily engineered by using for example an optical flow estimator. The predicted timing of gross visual motion from the first aspect (temporal regularity) treated above could be used to filter in the precise temporal segment of the optic flow that matters. But the GVF could also be simply implemented by a neural network that predict how "my cursor" will move in the visual field given the kinesthetic feedback and given how it has been moving in the visual field. If we adopt a "field" representation rather than a "vector" representation, the GVF could be implicitly realized as the directionally-specific spread of the cursor-based activation in the field. We'll return to the potential importance of "field" representation of GVFs again later.

From a first person perspective, the situation we are dealing with is like our waving our own hand in a particular direction leading us to expect our seeing that hand to visually move in a specific direction. That we have such expectation is why a new pair of glasses make things look weird. That we are able to quickly adapt to a new pair of glasses means that we have the right kind of plasticity for coping with the underlying shifts that disrupt the normal coordination and normal prediction. This kind of plasticity is also what allows humans to cope with the more [dramatic case of inverting lens](https://en.wikipedia.org/wiki/George_M._Stratton#Wundt's_lab_and_the_inverted-glasses_experiments).

The kind of invariance that is achieved through the coordinated prediction is invariance over shifts between eye/camera (or rather the optical path, to be precise) and body base. The plasticity or flexibility that we can build into the GVF predictor will allow us to handle rotational changes *without explicit calibration*.

As with other aspects of coordination, the boundaries of the Oz world are special. But that prediction does not work normally, at least along some dimension is actually the signature event that tells the agent that it's at the boundary.

Another point worth noting is that we are assuming that we could use some hand-crafted cumulants (the unit vectors) to build the GVF predictor. This is an example of the kind of "generic or commonsense knowledge" that we are for now building into the agent, because, for now, we are doing our exploration [ideally](README.md#ideally) rather than [idealistically](README.md#idealistically). The fundamental limitation with the GVFs is that they assume that the relevant dimensions of interest, or "cumulants", are given. But full-blown play does not assume that. For now, we will be playing ideally rather than idealistically.

## 3. Visual ego localization -- space 2: where am I, visually speaking?

In addition to directional correspondence, we also need to be concerned about locational correspondence: *where* in the visual field the impact of "my" current activity will be. However, the sense of "where" here requires a bit of analysis. While it may be obvious that the "where" could be represented by a pair of coordinate values, that will require choosing an origin in addition to the dimensions of the direction, essentially forcing an explicit coordinate system as a precondition for representation. While we are used to utilizing explicit coordinate systems in conventional robotics, the reliance on them implies precise measurement and calibration, which are typically taken care of through engineering practice beyond the agent's own control. That in turn makes the solution brittle and hard to generalize. For this reason, while conceptually we may still think of the "where am I" ego-localization in terms of GVF style prediction over coordinates, we probably should choose a field sort of representation, a field with a single or possibly multiple activation peaks for where I could possibly be with respect to the visual field. This choice avoids the question of the specific choice of coordinates systems. Insofar as the field coincides with the visual field, it is implicitly relying on the camera-centered coordinates.

Now, the point of "where am I" in the visual field is so that the agent could know or predict the specific locus of its action in the visual scene, i.e. where in the visual field is "my" motion causing localized visual changes. The sort of invariance achieved here is that regardless of where I am actually, I am always able to localize myself through where my action is in the ego-centric or "camera-centered" coordinates. This gives the agent a certain degree of spatial differentiation between here and eleswhere. The basis of this here vs. elsewhere differentiation is the predictions about where ego-centrically "my cursor" will be or could be next. With this sort of localization, "my" actions will now have an ego anchor. They will be now from somewhere. (NB: the situation with Oz is somewhat different from the case of a human person because our eyes -- the "cameras" in question -- are where the ego-body is, specifically in our head, thus the visual world for us is centered around our heads, which is where the "ego" arguably is. But the locus of the Oz agent is arguably where its cursor is, with the all-seeing camera being in a bird's eye position outside of the Oz flatland.)

Note that this sort of visual ego localization could be supported by the directional alignment discussed above. The directional alignment will help us to tell which moving cursor is me, based on the predicted and the actual direction of the movements of the cursors. Thus, localization could be helped by attaching direction to a visually disturbed area as well as with the help of timing of the disturbance (temporal regularity). In the reverse direction, the visual ego localization could also support directional alignment through localizing the visual direction change to where I am. Insofar as this sort of mutual support is future-oriented, insofar as it is about predictions, we do not have a vicious dependency here. Instead, it is more like ongoing fusion of multiple constraints or sources of information.

It might be suggested that the ego localization should be considered with respect to the boundaries of the Oz flatland. In other words, it may be suggested that the agent could use the boundaries of the Oz flatland to define the reference frame it relies on rather than implicitly depends on the camera coordinates. But relationship to the boundary is indeed both different from and unnecessary for the visual ego localization: even in a boundless field in the wild, we humans still have no problem localizing ourselves at where we are at the time, and localize our actions and their effects *ego-centrically* to where we are. The here vs. elsewhere differentiation is spatial differentiation without absolute coordinates or boundary references. The boundaries will be more relevant when we consider metric correspondence and distance next.

## 4. How far to travel and when to arrive where -- space 3: metric correspondence

Should this be secondary to ego localization + visual direction. Allows visual sense of where to and how far to travel ...

This one settles the mapping of motion command to visual scene globally. This one requires integration of visual orientation and visual localization. It further requires metric correspondence for the two independently controllable action/motion dimensions with visible changes of ego location. Yet another field, centered around where the agent is, and spreads out according to how much time it takes to arrive where.

The invariance is with respect to differential scaling. This one is the scaling transformation, understood as how far the ego camera is from the Oz flatland. The distance metric correspondence between locomotion and visual change will allow estimation of how far to travel regardless of the scaling. Considering time, likely based on the rhythmic regularity or at least number of incremental ego motion, will allow the agent to have a sense of how much time it is going to take to arrive at a specific point in the visual field.

With these, the boundary, coupled with the special cursor behavior there, also becomes boundary, and arrive at it in a particular direction requires specific amount of travel or time. The boundary may then serve as landmarks.

Now, presumably also visual edges such as where the board ends and the background starts. Such as occluding lines on the board. This is something that Gibson has given elaborate analysis, it is something that the agent could learn to be sensitive to. But for now, we are not explicitly treating these aspects of vision yet. We will comment on this when we deal with "stoneness" about spatial distribution of visual or visible features.

## 5. What do I feel now? -- tactile feedback

So far, other than the tactile latency discussed earlier, we have only considered visual feedback. Obviously, we also need to consider the other very important "sensory" modality: tactile feedback. Tactile latency is a factor: learn to trigger a tactile change through a "press" or "touch" action. Here we also need to be concerned about the content of the tactile feedback.

Note that since tactile feedback under Oz, unlike in the real human case, takes a single point form and thus it makes no sense to talk about tactile orientation. Thus, in the simplest case, a gentle touch will just give us a point feedback. In this purest form, this point is not located with respect to anything, rather than the immediate ego. As the ego gets located in the visual field, and more over the visual quality gets correlated with the tacticle quality, which we will discuss later, the tactile feedback could become spatially located.

For now, it is the temporal version that matters more. In the simplest and most basic form, the prediction here would just be if I press, I will feel something and if I continue to press, I will continue to feel something. This is the form we discussed at the beginning when we talk about temporal regularity between touch action and tactile feedback. In the more elaborate version, we can and should consider the prediction as a function of not only my immediate press action, but also my past feeling, my current motion and even the visual input. These considerations get us to the next two topics.

## 6. Where will I feel what? -- tactile map

- Field of possible tactile feedback.
- Could be based solely on map built from dead reckoning. Built on top of memory. 

- The same for feeling ... similar to vision ...
- GVF field. We could use convolutional filters spanning both spatial and temporal dimension or use CNN+RNN combination for GVF field implementation.

feeling as a GVF of visual input ... from color and visual texture to feeling: esp. white and black. This gets us to the next topic.

## 7. The looks of how things feel -- cross-modal visual-tactile map and the rise of space

- Alignment of tactile field and visual field
- Multi-feature field
- We could use visual field to anchor and correct tactile field and error in dead reckoning.

- Join these two fields ... cross-modality GVF field ...
- Two inputs, one output, how things feel next or if I were there now. The rise of space.

- This is important for dealing with board movement and board rotation, or rotation of the board relative to the SCARA robot's base, because the board both looks and feels different from the background.

## 8. Where are the stones? -- stoneness as a particular kind of spatially distributed affordance

- Cross-modality feature placing of stoneness.
- So far no goal-oriented actions, all through correlations ...
- Learn all of the above through unsupervised predictive learning ...

- GVFs of stone color???

## 9. Moving stones -- let the play begin

- Learn about occlusion of the board and the lines by the stones.
- The beginning of play with stones qua stones, qua what a stone can do and what the agent can do with the stone in the environment

- Learn about stone affordances.
- Learn to differentiate individual stones ...

- Now we can specify the task of moving stones arounds ... in a goal oriented way ... with enough resilience and flexibility.
- Sequential decision making now ...

## ... and so on ...

We have charted a route for building up all the way to a level of complexity where stones could be played with. The sense is that such complexity is close to be within the reach of contemporary AI techniques and computational capacity. What is needed to to walk the route and fashion the necessary new techniques along the way. However, what is *not* going to work, i.e. what is not going to allow us to succeed at learning to play, would be to trivialize any crucial part of the complexity so that our AI ideas, agents, or robots will just "work". Indeed, they may work and win Go games and drive cars, but they won't be able to [play in Oz](play.md).
