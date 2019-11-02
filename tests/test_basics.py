import unittest

class TestBasics(unittest.TestCase):
    def test_config(self):
        from oz import config
        self.assertIsNotNone(config.DEFAULT_WORLD_SIZE_X)
        self.assertIsNotNone(config.DEFAULT_WORLD_SIZE_Y)
        self.assertIsNotNone(config.DEFAULT_WORLD_BACKGROUND_COLOR)
        self.assertIsNotNone(config.DEFAULT_NUMBER_OF_AGENTS)
        self.assertIsNotNone(config.DEFAULT_NUMBER_OF_STONES)
        self.assertIsNotNone(config.DEFAULT_BOARD_NUMBER_OF_LINES)
        self.assertIsNotNone(config.DEFAULT_BOARD_SIZE_X_RATIO)
        self.assertIsNotNone(config.DEFAULT_BOARD_SIZE_Y_RATIO)
        self.assertIsNotNone(config.DEFAULT_BOARD_COLOR)
        self.assertIsNotNone(config.DEFAULT_BOARD_LINE_COLOR)
        self.assertIsNotNone(config.DEFAULT_BOARD_LINE_WIDTH_RATIO)
        self.assertIsNotNone(config.DEFAULT_STONE_SIZE_RATIO)
        self.assertIsNotNone(config.DEFAULT_STONE_COLOR_BLACK)
        self.assertIsNotNone(config.DEFAULT_STONE_COLOR_WHITE)
        self.assertIsNotNone(config.DEFAULT_STONE_EDGE_WIDTH_RATIO)
        self.assertIsNotNone(config.DEFAULT_STONE_EDGE_COLOR_BLACK)
        self.assertIsNotNone(config.DEFAULT_STONE_EDGE_COLOR_WHITE)
        self.assertIsNotNone(config.DEFAULT_AGENT_SIZE_RATIO)
        self.assertIsNotNone(config.DEFAULT_AGENT_COLOR)
        self.assertIsNotNone(config.DEFAULT_AGENT_EDGE_WIDTH_RATIO)
        self.assertIsNotNone(config.DEFAULT_AGENT_EDGE_COLOR)
        self.assertIsNotNone(config.DEFAULT_DISPLAY_HZ)
        self.assertIsNotNone(config.DEFAULT_DISPLAY_RESOLUTION,)
        self.assertIsNotNone(config.DEFAULT_TRANSPARENT_COLOR_KEY)

if __name__ == '__main__':
    unittest.main()
