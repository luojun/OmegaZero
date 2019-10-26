# TODO: understand conventions for __main__.py

import argparse

from world import World
import config
import oz

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

WORLD = World(configs)

#import cProfile
#cProfile.run('run_oz(WORLD, cycles=100, timing=True)')

# Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
#oz.run_oz(WORLD, cycles=5000, capture_pngs=True)

#oz.run_oz(WORLD, cycles=1000, timing=True, display_hz=ARGS.display_hz)

oz.run_oz(WORLD, display_hz=ARGS.display_hz)
