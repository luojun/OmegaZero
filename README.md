# Omega Zero

Exploration in a virtual 2D environment, focused on learning from demonstration on the way towards Delta One.

## Goal

Sketch out a design for "Omega Zero", which uses Go board and Go stones to play at least three games:

1. Go
2. Gomoku
3. Tic-Tac-Toe

Moreover, Omega Zero, Oz for short, must not be given the knowledge to play all three games. Instead, it will be given the "knowledge" to play only up to two of these three games and must learn the third game based on explanation and demonstration suitable for a normal human.

Ideally, Oz will be given only enough knowledge to learn the three games through learning from demonstration.

## Environment as 2D GUI

Pixel flatland with layers. One layer for board and one layer for stones. Multiple stones may overlap in the same layer. The environment extends beyond the board by half of the board's dimension in each of the four directions. Continuous time. Asynchronous interaction.

A 2D GUI, with regular sized Go board and regular sized Go stones. No gravity. No force. No inertia. With layers -- stones are placed on top of board. Continuous position variation. Purely relative position based control similar to normal 2D GUI.

Humans interact with the environment through the GUI. Actions available: click on a stone to pick it up, move mouse to move stone, click again to place stone, move the mouse cursor around. When a stone is being touched or held, one tactile bit is set. When the board is touched, another bit is set. When the background is touched, yet another bit is set. The touching point is a single pixel. AI gets 2D rendering of the environment as input. AI interacts with the environment in the same way, by issuing click and move commands.

If a click is issued above a stone (or a stack of stones), that stone (or the top stone of the stack) is picked up and a tactile bit is set. If the cursor moves, the stone moves along with the cursor. If a click is issued again, the stone is dropped and the tactile bit is unset.

Cursors move by relative motion. There may be multiple cursors, each of which is controlled by an agent, which could be a human user. The cursors may or may not be visually differentiated. Cursor motion commands are speed vectors. The speed vector must be issued continuously at every time step for the cursor to move continuously.



# Delta One

Learn from human demonstration to play Go, Chess, and Chinese Chess bodily with real game sets and without calibration, special adaptation, or special hardward.


