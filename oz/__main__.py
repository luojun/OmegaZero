# TODO: understand conventions for __main__.py
# TODO: test auxiliary funcationalities: timing, capture, headless

import argparse

import oz_config
from oz_world import world
from oz_world import settings
from oz_runner import runner

def main():

    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('-l', '--lines', nargs='?',
                        default=oz_config.DEFAULT_BOARD_NUMBER_OF_LINES, type=int)
    PARSER.add_argument('-s', '--stones', nargs='?',
                        default=oz_config.DEFAULT_NUMBER_OF_STONES, type=int)
    PARSER.add_argument('-a', '--agents', nargs='?',
                        default=oz_config.DEFAULT_NUMBER_OF_AGENTS, type=int)
    PARSER.add_argument('-hz', '--display_hz', nargs='?',
                        default=oz_config.DEFAULT_DISPLAY_HZ, type=float)
    ARGS = PARSER.parse_args()

    world_settings = settings.WorldSettings(ARGS.lines, ARGS.stones, ARGS.agents)
    WORLD = world.World(world_settings)
    OZ_RUNNER = runner.Runner(WORLD, resolution=oz_config.DEFAULT_DISPLAY_RESOLUTION)

    #import cProfile
    #cProfile.run('OZ_RUNNER.run(cycles=100, timing=True)')

    # Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
    #OZ_RUNNER.run(cycles=5000, capture_pngs=True)

    #OZ_RUNNER.run(cycles=1000, timing=True, display_hz=ARGS.display_hz)

    OZ_RUNNER.run(display_hz=ARGS.display_hz)

if __name__ == '__main__':
    main()
