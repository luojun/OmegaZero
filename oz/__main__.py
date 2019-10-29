# TODO: test auxiliary funcationalities: timing, capture, headless

import argparse

import oz_config
from oz_world import world
from oz_world import settings
from oz_runner import runner

def main():

    _parser = argparse.ArgumentParser()
    _parser.add_argument('-l', '--lines', nargs='?',
                         default=oz_config.DEFAULT_BOARD_NUMBER_OF_LINES, type=int)
    _parser.add_argument('-s', '--stones', nargs='?',
                         default=oz_config.DEFAULT_NUMBER_OF_STONES, type=int)
    _parser.add_argument('-a', '--agents', nargs='?',
                         default=oz_config.DEFAULT_NUMBER_OF_AGENTS, type=int)
    _parser.add_argument('-hz', '--display_hz', nargs='?',
                         default=oz_config.DEFAULT_DISPLAY_HZ, type=float)
    _args = _parser.parse_args()

    _world_settings = settings.WorldSettings(_args.lines, _args.stones, _args.agents)
    _world = world.World(_world_settings)
    _oz_runner = runner.Runner(_world, resolution=oz_config.DEFAULT_DISPLAY_RESOLUTION,
                               transparent_color_key=oz_config.DEFAULT_TRANSPARENT_COLOR_KEY)

    #import cProfile
    #cProfile.run('_oz_runner.run(cycles=100, timing=True)')

    # Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
    #_oz_runner.run(cycles=5000, capture_pngs=True)

    #_oz_runner.run(cycles=1000, timing=True, display_hz=args.display_hz)

    _oz_runner.run(display_hz=_args.display_hz)

if __name__ == '__main__':
    main()
