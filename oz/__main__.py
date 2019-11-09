# TODO: separate out affordance0 experiment

def main():
    import argparse
    _parser = argparse.ArgumentParser()

    from . import config
    _parser.add_argument('-l', '--lines', nargs='?',
                         default=config.DEFAULT_BOARD_NUMBER_OF_LINES, type=int)
    _parser.add_argument('-s', '--stones', nargs='?',
                         default=config.DEFAULT_NUMBER_OF_STONES, type=int)
    _parser.add_argument('-a', '--agents', nargs='?',
                         default=config.DEFAULT_NUMBER_OF_AGENTS, type=int)
    _parser.add_argument('-hz', '--display_hz', nargs='?',
                         default=config.DEFAULT_DISPLAY_HZ, type=float)
    _parser.add_argument('-e', '--experiment', nargs='?',
                         default='', type=str)
    _args = _parser.parse_args()

    from .world.world import World
    from .world.settings import Settings
    from .runner.runner import Runner
    from .agent.agent import Agent
    _settings = Settings(config, _args.lines, _args.stones, _args.agents)

    if _args.experiment == 'affordance0':
        from .affordances.agent0 import Agent0
        _world = World(_settings, [Agent, Agent0])
    else:
        _world = World(_settings)
    _runner = Runner(_world, resolution=config.DEFAULT_DISPLAY_RESOLUTION,
                             transparent_color_key=config.DEFAULT_TRANSPARENT_COLOR_KEY)

    #import cProfile
    #cProfile.run('_runner.run(cycles=100, timing=True)')

    # Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
    #_runner.run(cycles=50, capture=True)

    #_runner.run(cycles=1000, timing=True, display_hz=args.display_hz)

    _runner.run(display_hz=_args.display_hz)

if __name__ == '__main__':
    main()
