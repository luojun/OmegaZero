# Tests:
#
# - world construction
#   - check existence of surfaces and sizes
#   - check number of stones, number of lines, and number of agents
# - sensorimotor loop
#   - check dimension of rendered image
#   - single agent world
#     - move agent to corner of environment, check tactile feedback
#     - move agent to cneter of board, check tactile feedback
#   - single agent + single stone world
#     - create stone black at a corner of the environment, check existence of stone at corner
#     - move agent to that corner of the environment, check agent is at corner
#     - pick up stone, check holding and tactile feedback
#     - move to center of board, check stone location and agent location
#     - release stone
#       - check tactile feedback
#       - check color of center of rendered image -- agent color
#     - pick up stone again, check tactile feedback
#       - check color of center of rendered image -- stone black
# - timing
#   - check the zero cycle case
#   - check greater than zero cycles: elapsed time bigger than zero
#   - check double cycles make time longer
# - capture
#   - single screenshot -- test existence and size of PNG
#   - multiple screenshots -- test existence of a series of PNGs and their size
# - headless
#   - check zero cycle case
#   - check 30 hz case

import argparse

import config
from world import world
from world import settings
from runner import runner

def main():

    _parser = argparse.ArgumentParser()
    _parser.add_argument('-l', '--lines', nargs='?',
                         default=config.DEFAULT_BOARD_NUMBER_OF_LINES, type=int)
    _parser.add_argument('-s', '--stones', nargs='?',
                         default=config.DEFAULT_NUMBER_OF_STONES, type=int)
    _parser.add_argument('-a', '--agents', nargs='?',
                         default=config.DEFAULT_NUMBER_OF_AGENTS, type=int)
    _parser.add_argument('-hz', '--display_hz', nargs='?',
                         default=config.DEFAULT_DISPLAY_HZ, type=float)
    _args = _parser.parse_args()

    _world_settings = settings.WorldSettings(_args.lines, _args.stones, _args.agents)
    _world = world.World(_world_settings)
    _runner = runner.Runner(_world, resolution=config.DEFAULT_DISPLAY_RESOLUTION,
                               transparent_color_key=config.DEFAULT_TRANSPARENT_COLOR_KEY)

    #import cProfile
    #cProfile.run('_runner.run(cycles=100, timing=True)')

    # Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
    #_runner.run(cycles=5000, capture_pngs=True)

    #_runner.run(cycles=1000, timing=True, display_hz=args.display_hz)

    _runner.run(display_hz=_args.display_hz)

if __name__ == '__main__':
    main()
