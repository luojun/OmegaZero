# Omega Zero: learning to play in a virtual environment

Omega Zero, Oz for short, is an exploration of the learning of commonsense knowledge in a virtual 2D environment similar to the physical setup for the game of Go. The question we ask is how an agent may learn enough commonsense knowledge in the Oz environment so that it can learn to play new games in Oz from simple demonstrations of these new games.

We call our exploration "Omega Zero" because the goal here is not to win a game as it was for AlphaGo, thus "Omega", but rather learning to play the game without being given specific representations about the game, thus "Zero". Our position is that learning to play a game in a physical environment *de novo* is qualitatively different from and significantly harder than learning to win a game after the agent already knows how to play the game.

<p align="center">
<img src="demo.gif" align="center" height="400" width="400" alt="Demo of Tic-Tac-Toe with 4 random agents and 1 human player">
<br/>
<b>Oz in a Tic-Tac-Toe setup with 4 random agents and 1 human player</b>
</p>


## <a name="challenge"></a> Challenge: learn commonsense for learning to play

We use a 2D digital version of Go stones and Go boards of various sizes (such as 19x19, 15x15 and 4x4) as the setup where an agent can play three well known games:

1. Go
2. Gomoku
3. Tic-Tac-Toe

and potentially many more games we could introduce or invent.

It is trivial to code up each of these games according to their proper abstractions so that an AI agent can "play" it by generating the next move from any game state towards an eventual win. AlphaGo depends on such a code-up and wins brilliantly. But that is not what Oz is after.

<a name="idealistically"></a>*Idealistically*, an Oz agent will not be given any prior knowledge and will have to learn all the knowledge needed. This is indeed quite idealistically, but it is not completely crazy and the gut feeling is that we are getting close (50 to 100 years away?) to being able to pull it off.

Note that we are *not* assuming that the Oz agent will not be learning from other agents or that it will not benefit from symbolic communication implementable in Oz. To get rid of all social and communicative dependencies of learning would mean to tell a full evolutionary as well as epigentic story. But we are here mainly interested in the epigenetic story.

<a name="ideally"></a>If the idealistic approach is too futuristic, then *ideally* an Oz agent may be given only generic or commonsense knowledge about the Oz environment, such as how a placed stone may not be picked up again, how the intersections on the board should be treated specially, how two agents should take turn to make moves, etc. Then on the basis of such generic knowledge the Oz agent is expected to learn all these specific games through learning from demonstration. This way with things is labeled "ideally", because while the agent is given some necessary knowledge, it still needs to, in its own interaction in Oz, abide by the ideals that both are represented by the knowledge and govern how game interactions should unfold in the actual physical setting of Oz. While it is standard for current computer board games to restrict the physics to directly honor the ideals, Oz does not enforce such ideals in its physics but instead relies on the agent's ability to do so. By setting up the Oz challenge this way, we are forced to investigate the commonsense knowledge underwriting all these games without abstracting away the relevant lower level physical interactions. Simply coding up a set of symbolic rules will not do. The commonsense knowledge has to bridge physical interactions, where anything goes, to the governing ideals of the specific games. We do not know how to do this yet, but the gut feeling is that we can pull this one off in the next 5 to 30 years.

## <a name="environment"></a> Environment: an interactive flatland under the bird's eye view

The Oz environment is a flatland with layers. One layer for the background, one layer for the board, and one layer for the stones. Multiple stones may overlap in the same layer. Both board and stones are of their regular physical size. The environment extends beyond the board by about half of the board's dimension in each of the four directions. The board may rotate and move against the background. The stones are of their regular colors: black and white. Individual stones may or may not vary in the specific shades and patterns of their color. Stones could be at anywhere in the environment. They could all be piled up at a single location or be scattered around.

The physics of Oz is simple: continuous 2D space, continuous time, asynchronous interaction, no gravity, no friction, no force, and no inertia.

Agents interact with the environment through their respective "cursors". There may be multiple cursors, each of which is controlled by a single agent, which could be a human interacting with the Oz envrionment through GUI. Cursors may or may not be visually differentiated. Cursors move by relative motion. Cursor motion commands are speed vectors. A speed vector must be issued continuously at every time step for the cursor to move continuously. Cursors are visible. They have the shape of a round disc. They may be of a color different from those of the stones. Their size is comparable to the size of a human fingertip. There is kinesthetic feedback as well as visual feedback for cursor movements. Cursors can move across each other without interference.

When a cursor is clicked over a stone, the stone is picked up. When the cursor moves, the stone moves along. When the cursor is clicked again the stone is dropped. Only one stone will be picked up or held at a time. When a stone is being picked up or held, one kind of tactile feedback is provided. When the board is touched, another kind of tactile feedback is provided. When the background is touched, yet another kind is provided. The point of touch is a single point. When multiple stones are at the point of touch, only one stone is picked up. When multiple cursors attempt to pick up the same stone simultaneously, the result (i.e. which cursor actually picks up the stone) is random. One cursor can also "grab" a stone held by another cursor by clicking on it.

At any point in time, the whole environment, including the board, the stones, and the cursor could be rendered into an image, from the bird's eye view. The image is given to the AI agent as its visual input along with tactile and kinesthetic feedback. (NB: We note that in the real world, the optical axis of the bird's eye camera may or may not be perpendicular to the board. But given the flatland nature of Oz, we are going to scarifice that aspect of fidelity, at least before version 2.0. We do believe that such a simplification, which still allows zooming and panning, is not trivializing the transformations that matter in the real world cases. Thus our explorations will still have adequate real-world implications.)

The image could also be presented through a GUI to one or more human agents. Humans are allowed to interact with the Oz environment through the GUI. Cursor states such as it is being pressed down and held will also be rendered per normal GUI practice. Tactile feedback could also be visualized for human interaction, but may be unnecessary. Kinesthetic feedback is not provided to human agents because they do get that for the movement of their own hand.

Three things can be noted about this setup:

1. Except for the fact that the physics of the Oz environment is an unrealistic simplification, the way in which our AI agents interact with the Oz environment is highly similar to how humans play board games through GUI on a normal computer.
2. The Oz setup allows multiple AI agents and multiple humans to simultaneously interact with the environment, giving us ample opportunity to do teaching or demonstration by either AI or human teachers.
3. The physical setup of Oz, including the vision or image rendering part, is not unlike the relationship between a [SCARA robot](https://en.wikipedia.org/wiki/SCARA) or [Cartesian robot](https://en.wikipedia.org/wiki/Cartesian_coordinate_robot) and its task environment. Thus, our learning solutions in Oz, once they are adequately figured out, could potentially enable the many robots deployed out there to adapt to new tasks very quickly.

## Illustration: from affordances to concepts through play

For one example of the sorts of exploration Oz enables, please see a separate set of notes on [(a) learning basic affordances](notes/affordances.md) as a foundation for [(b) play](notes/play.md) and for further learning of [(c) commonsense conceptual structures](notes/concepts). What is described in these notes falls largely under [the ideal approach](#ideally) to the Oz challenge. However, this specific perspective -- that of learning affordances to support play and learning further affordances and eventually conceptual structures through play -- is only one of the many possible theoretical perspectives that we can take on the [Oz envirnoment](#environment) and the [Oz challenge](#challenge). If one so chooses, one can deal with the Oz environment using traditional symbolic AI or using the conventional framework of industrial robotics. So long as Oz's commitment to "freedom from game-specific knowledge" is honored, that would be fine and that would provide a good way to compare the pros and cons of the various approaches.

# Delta One: learning to play in the real world

We take Omega Zero to be a stepping stone towards Delta One, wherein a robot learns from human demonstrations to play Go, Chess, and Chinese Chess bodily with physically real game sets and without calibration, special physical adaptation, or game-specific robotics hardward. "Delta" here marks the leap from digital to physical. "One" emphasizes the requirement that a single version of a single system is used without retraining or any other offline tweaking. It should be just like how a single person, such as a young child, can in a very short period of time learn to play Go, Chess, and Chinese Chess: we can just sit the child in front of real game sets and let the teaching, learning, and playing begin.
