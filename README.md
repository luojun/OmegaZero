# Omega Zero: learning to play in a virtual environment

Omega Zero, Oz for short, is an exploration of the learning of commonsense knowledge in a virtual 2D environment similar to the physical setup of the game of Go. The goal is to learn enough commonsense knowledge to enable learning from demonstration of new games that can be played in this physical setup.

We call our exploration "Omega Zero" because the goal here is not acing the game as AlphaGo did, thus "Omega", but rather learning to play it without being given either prior knowledge of the game rules or data abstractions coding up the game at the level of game states and rules, thus "Zero". Our intuition is that learning to play a game in an adequately physical environment is qualitatively different from and significantly harder than learning to win a game.

<p align="center">
<img src="screenshot-0.png" align="center" height="600" width="600" alt="Tic-Tac-Toe with 3 agents">
<br/>
<b>Oz in a Tic-Tac-Toe setup with 3 agents</b>
</p>


## <a name="challenge"></a> Challenge: learn commonsense for learning to play

We use a 2D digital version of the Go board and Go stones as an experimental setup where an AI agent can play at least three common games:

1. Go
2. Gomoku
3. Tic-Tac-Toe

and many other new games we could invent.

It is trivial to code up each of these games so that an AI agent can "play" it by generating a good next move from any game state towards an eventual "win". AlphaGo did that brilliantly. But that is not what Oz is about.

Instead, the challenge of Oz is for an AI agent to learn from demonstration how to play at least one of these three games (e.g. Go) when given only knowledge about how to play the other one or two games (e.g. Tic-Tac-Toe).

<a name="ideally"></a>Ideally, an AI agent will be given no game-specific knowledge at all but will be given only generic or commonsense knowledge about the environment on the basis of which it is expected to learn all three games through learning from demonstration. This way with things is labeled "ideally", because it means the environment will necessarily have to be engineered according to the "ideals" corresponding to the generic knowledge we build in so that the knowledge will be valid in the actual (but sufficiently engineered) environment.

<a name="idealistically"></a>Idealistically, an Oz AI agent will not be given any prior knowledge at all and will have to learn the knowledge needed. This is indeed a bit futuristic, but yep that's we are aiming at and the gut feeling is that we are getting close to being able to pull that off. (NB: we are not assuming that the agent will not be learning socially through the Oz environment from other agents or that it will not benefit from some forms of symbolic communication implementable in Oz. To fully rid of the social and communicative dependencies of learning would mean to tell a full evolutionary as well as epigentic story. We are here mainly interested in the epigenetic story.)

## <a name="environment"></a> Environment: an interactive flatland under the bird's eye view

The Oz environment is a flatland with layers. One layer for the background, one layer for the board, and one layer for the stones. Multiple stones may overlap in the same layer. Both board and stones are of their regular physical size. The environment extends beyond the board by half of the board's dimension in each of the four directions. The board may rotate against the background. The stones are of their regular colors: black and white. Individual stones may or may not vary in the specific shades and patterns of their color. Stones could be at anywhere in the environment. They could all be piled up at a single location or be scattered around.

The physics of Oz is simple: continuous 2D space, continuous time, asynchronous interaction, no gravity, no friction, no force, and no inertia.

Agents interact with the environment through their respective "cursors". There may be multiple cursors, each of which is controlled by a single agent, which could be a human interacting with the Oz envrionment through GUI. The cursors may or may not be visually differentiated. Cursors move by relative motion. Cursor motion commands are speed vectors. A speed vector must be issued continuously at every time step for the cursor to move continuously. Cursors are visible. They have the shape of a round disc. They are of a color different from those of the stones. Their size is comparable to the size of a human fingertip. There is kinesthetic feedback as well as visual feedback for cursor movements. Cursors can move across each other without any interference.

When a cursor is clicked over a stone, the stone is picked up. When the cursor moves, the stone moves along. When the cursor is clicked again the stone is dropped. Only one stone will be picked up or held at a time. When a stone is being picked up or held, one kind of tactile feedback is provided. When the board is touched, another kind of tactile feedback is provided. When the background is touched, yet another kind is provided. The point of touch is a single point. When multiple stones are at the point of touch, only one stone is picked up. When multiple cursors attempt to pick up the same stone simultaneously, the result (i.e. which cursor actually picks up the stone) is random. One cursor can also "grab" a stone held by another cursor by clicking on it.

At any point in time, the whole environment, including the board, the stones, and the cursor could be rendered into an image, from the bird's eye view. The image is given to the AI agent as its visual input along with tactile and kinesthetic feedback. (NB: We note that in the real world, the optical axis of the bird's eye camera may or may not be perpendicular to the board. But given the flatland nature of Oz, we are going to scarifice that aspect of fidelity, at least before version 2.0. We do believe that such a simplification, which still retains scaling and planar rotation, is not trivializing the transformations that matter in the real world cases. Thus our explorations will still have adequate real-world implications.)

The image could also be presented through a GUI to one or more human agents. Humans are allowed to interact with the Oz environment through the GUI. Cursor states such as it is being pressed down and held will also be rendered per normal GUI practice. Tactile feedback could also be visualized for human interaction, but may be unnecessary. Kinesthetic feedback is not provided to human agents because they do get that for the movement of their own hand.

Three things can be noted about this setup:

1. Except for the fact that the physics of the Oz environment is totally unrealistic, the way in which our AI agents interact with the Oz environment is highly similar to how humans play board games through GUI on a normal computer.
2. The Oz setup allows multiple AI agents and multiple humans to simultaneously interact with the environment, giving us ample opportunity to do teaching or demonstration by either AI or human teachers.
3. The physical setup of Oz, including the vision or image rendering part, is not unlike the relationship between a [SCARA robot](https://en.wikipedia.org/wiki/SCARA) or [Cartesian robot](https://en.wikipedia.org/wiki/Cartesian_coordinate_robot) and its task environment. Thus, our learning solutions in Oz, once they are adequately figured out, could almost directly enable the many robots out there to adapt to new tasks very quickly.

## Illustration: from affordances to conceptual structures through play

For one example of the sorts of exploration Oz enables, please see a separate set of notes on [(a) learning basic affordances](affordances.md) as a foundation for [(b) play](play.md) and for further learning [(c) commonsense conceptual structures](concepts).

Note that this specific perspective (that of learning affordances to support play and learning further affordances and eventually conceptual structures through play) is only one of the many possible theoretical perspectives that we can take on the [Oz envirnoment](#environment) and the [Oz challenge](#challenge). If one so chooses, one can deal with the Oz environment using traditional symbolic AI or using the conventional framework of industrial robotics. So long as the orientation of the Oz challenge is honored, that would be fine and that would be a good way to compare the pros and cons of the various approaches.

# Delta One: learning to play in the real world

We take Omega Zero to be a stepping stone towards Delta One, wherein a robot learns from human demonstrations to play Go, Chess, and Chinese Chess bodily with physically real game sets and without calibration, special adaptation, or special hardward. "Delta" marks the leap from digital to physical. "One" emphasizes the requirement that a single version of a single system is used without retraining or any other offline tweaking. It should be just like how one person can in a very short period of time learn to play Go, Chess, and Chinese Chess.
