# TODO: understand conventions for __main__.py
# TODO: test auxiliary funcationalities: timing, capture, headless

import argparse

import config
from world import world
from runner import runner

def main():

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-l', '--lines', nargs='?',
                        default=config.DEFAULT_BOARD_NUMBER_OF_LINES, type=int)
    PARSER.add_argument('-s', '--stones', nargs='?',
                        default=config.DEFAULT_NUMBER_OF_STONES, type=int)
    PARSER.add_argument('-a', '--agents', nargs='?',
                        default=config.DEFAULT_NUMBER_OF_AGENTS, type=int)
    PARSER.add_argument('-hz', '--display_hz', nargs='?',
                        default=config.DEFAULT_DISPLAY_HZ, type=float)
    ARGS = PARSER.parse_args()

    CONFIGS = config.Config()
    CONFIGS.board.number_of_lines = ARGS.lines
    CONFIGS.world.number_of_stones = ARGS.stones
    CONFIGS.world.number_of_agents = ARGS.agents

    WORLD = world.World(CONFIGS)

    OZ_RUNNER = runner.Runner(WORLD)

    #import cProfile
    #cProfile.run('OZ_RUNNER.run(cycles=100, timing=True)')

    # Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
    #OZ_RUNNER.run(cycles=5000, capture_pngs=True)

    #OZ_RUNNER.run(cycles=1000, timing=True, display_hz=ARGS.display_hz)

    OZ_RUNNER.run(display_hz=ARGS.display_hz)

if __name__ == '__main__':
    main()
