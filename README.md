# Omega Zero

Exploration in a virtual 2D environment, focused on learning from demonstration on the way towards Delta One.

## Challenge: learn to play games from demonstrations

In Omega Zero, Oz for short, we use a 2D digital version of the Go board and Go stones as an experimental setup where an AI agent can play at least three games:

1. Go
2. Gomoku
3. Tic-Tac-Toe

It is trivial to code each of these games and the corresponding game play up so that an AI agent can "play" it by generating a good next move given any game state. That is not what Oz is about.

Instead, the challenge is for an AI agent to learn from demonstration how to play at least one of these three games (e.g. Go) when given only knowledge about how to play the other one or two games.

Ideally, an AI agent will be given no game-specific knowledge at all but will be given only generic knowledge about the environment on the basis of which it is expected to learn all three games through learning from demonstration.

Idealistically, Oz will not be given any prior knowledge at all.

## A pixel flatland environment

The Oz environment is going to be a pixel flatland with layers. One layer for the background, one layer for the board, one layer for the lines on the board, and one more layer for stones. Multiple stones may overlap in the same layer. Both board and stones are of their regular size. The environment extends beyond the board by half of the board's dimension in each of the four directions. The stones are of their regular colors: black and white. Individual stones may or may not vary in the specific shades and patterns of their color. Stones could be at anywhere in the environment. They could all be piled up at a single location or be scattered around completely separately.

Continuous 2D space. Continuous time. Asynchronous interaction. No gravity. No force. No inertia.

Agents interact with the environment through their respective cursors. There may be multiple cursors, each of which is controlled by an agent, which could be a human through GUI.  The cursors may or may not be visually differentiated. Cursors move by relative motion. Cursor motion commands are speed vectors. The speed vector must be issued continuously at every time step for the cursor to move continuously. No motion feedback other than visual. Cursors can move across each other without any interference.

Extra cursor actions: click on a stone to pick it up, move cursor to move stone, click again to place stone. Click: press down and release within a short time window, as with regular mouse. State feedback: cursor is being pressed down or not. Tactile feedback at cursor: When a stone is being held, one tactile bit is set. When the board is touched, another bit is set. When the background is touched, yet another bit is set. Touch: press down and hold. The touching point is a single point. Only one stone will be picked up or held at a time. When multiple stones are at a point that is clicked one of these stones are randomly picked up. When multiple cursors attempt to pick up the same stone simultaneously, the result (such as which cursor picks up the stone) is random. However, when one stone is held by a cursor, no other cursors could pick that stone up. One cursor can pick up or held only one stone at a time.

At any point in time, the whole environment, including the board, the stones, and the cursor could be rendered into an image. This image is given to the AI agent as its visual input along with the tactile bits. The image could also be presented through a GUI. Humans interact with the environment through the GUI. Cursor states such as it is being pressed down and held will also be rendered per normal GUI practice. Tactile feedback could also be visualized for human interaction, but may be unnecessary.

With this setup, AI agents interact with the environment in a way similar to how humans interact with a 2D virtual environment through GUI (normal board game playing on computer).

Note two things: (1) the setup allows multiple AI agents and multiple humans to simultaneously interact with the environment and (2) a rule-based agent with all necessary game-specific knowledge coded up could be easily integrated with the environment to serve as a teacher for learning from demonstration.

# Delta One

Learn from human demonstration to play Go, Chess, and Chinese Chess bodily with real game sets and without calibration, special adaptation, or special hardward.


