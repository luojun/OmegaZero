# TODO: understand conventions for __main__.py

import argparse

import config
from world import World
from runner import Runner

PARSER = argparse.ArgumentParser()

PARSER.add_argument('-l', '--lines', nargs='?', default=config.DEFAULT_BOARD_NUMBER_OF_LINES, type=int)
PARSER.add_argument('-s', '--stones', nargs='?', default=config.DEFAULT_NUMBER_OF_STONES, type=int)
PARSER.add_argument('-a', '--agents', nargs='?', default=config.DEFAULT_NUMBER_OF_AGENTS, type=int)
PARSER.add_argument('-hz', '--display_hz', nargs='?', default=config.DEFAULT_DISPLAY_HZ, type=float)

ARGS = PARSER.parse_args()

configs = config.Config()
configs.board_number_of_lines = ARGS.lines
configs.number_of_stones = ARGS.stones
configs.number_of_agents = ARGS.agents

world = World(configs)
oz_runner = Runner(world)

#import cProfile
#cProfile.run('oz_runner.run(cycles=100, timing=True)')

# Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
#oz_runner.run(cycles=5000, capture_pngs=True)

#oz_runner.run(cycles=1000, timing=True, display_hz=ARGS.display_hz)

oz_runner.run(display_hz=ARGS.display_hz)
