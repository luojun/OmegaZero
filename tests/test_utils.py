import unittest

class TestTimer(unittest.TestCase):

    def test_timer(self):
        from oz import config
        from oz.world import world
        from oz.world import settings
        from oz.runner import runner
        _settings = settings.Settings(config)
        _world = world.World(_settings)
        _runner = runner.Runner(_world, resolution=config.DEFAULT_DISPLAY_RESOLUTION,
                                transparent_color_key=config.DEFAULT_TRANSPARENT_COLOR_KEY)

        # [x] timing
        #     [x] check 0-cycle case: elapsed time is bigger than zero
        #     [x] check 1-cycle case: elapsed time is bigger than zero cycle case
        #     [x] check 10-cycle case: period is between one fifth and five times of 1-cycle case

        _stats = _runner.run(cycles=0, timing=True, display_hz=0)
        self.assertIsNotNone(_stats)
        self.assertIsNone(_stats["period"])
        _elapsed_0 = _stats["elapsed"]
        self.assertTrue(_elapsed_0 >= 0)

        _stats = _runner.run(cycles=1, timing=True, display_hz=0)
        self.assertIsNotNone(_stats)
        self.assertIsNotNone(_stats["period"])
        _elapsed_1 = _stats["elapsed"]
        _period_1 = _stats["period"]
        self.assertEqual(_period_1, _elapsed_1)
        self.assertTrue(_period_1 > _elapsed_0)

        _stats = _runner.run(cycles=10, timing=True, display_hz=0)
        self.assertIsNotNone(_stats)
        self.assertIsNotNone(_stats["period"])
        _period_10 = _stats["period"]
        self.assertTrue(0.2 * _period_1 < _period_10)
        self.assertTrue(5 * _period_1 > _period_10)

class TestScreenCapture(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory
        import tempfile
        self.test_dir = tempfile.TemporaryDirectory()
		
    def tearDown(self):
        # Close the file, the directory will be removed after the test
        self.test_dir.cleanup()

    def test_screen_captures(self):
        import pygame
        from os import listdir
        from os.path import isfile, join

        from oz import config
        from oz.world import world
        from oz.world import settings
        from oz.runner import runner

        _settings = settings.Settings(config)
        _world = world.World(_settings)
        _runner = runner.Runner(_world, resolution=config.DEFAULT_DISPLAY_RESOLUTION,
                                transparent_color_key=config.DEFAULT_TRANSPARENT_COLOR_KEY)
        # [x] multiple screenshots -- test existence of a series of PNGs and their size

        _dir = self.test_dir.name
        _cycles = 50
        _every = 10
        _expected_total = _cycles // _every
        _stats = _runner.run(cycles=_cycles,
                             capture=True, capture_every=_every, capture_dir=_dir,
                             display_hz=0)
        _files = [f for f in listdir(_dir) if isfile(join(_dir, f))]
        self.assertEqual(len(_files), _expected_total)

        _expected_size = (round(config.DEFAULT_WORLD_SIZE_X * config.DEFAULT_DISPLAY_RESOLUTION),
                          round(config.DEFAULT_WORLD_SIZE_Y * config.DEFAULT_DISPLAY_RESOLUTION))
        _image = pygame.image.load(join(_dir, _files[-1]))
        self.assertEqual(_image.get_rect().size, _expected_size)
