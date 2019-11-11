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

    def test_world_construction(self):
        from oz import config
        from oz.world import settings
        from oz.world import world
        _settings = settings.Settings(config)
        _world = world.World(_settings)

        # [x] world construction
        #     [x] check size of world
        #     [x] check size of the board
        #     [x] check number of stones
        #     [x] check number of lines
        #     [x] check number of agents

        self.assertIsNotNone(_world.settings)
        self.assertEqual(_world.settings.size,
                         (config.DEFAULT_WORLD_SIZE_X, config.DEFAULT_WORLD_SIZE_Y))
        self.assertIsNotNone(_world.board)
        board_min_x, board_min_y, board_max_x, board_max_y = _world.board.rect
        _expected_size = (board_max_x - board_min_x, board_max_y - board_min_y)
        self.assertEqual(_world.settings.board.size, _expected_size)
        self.assertIsNotNone(_world.board.lines)
        self.assertEqual(len(_world.board.lines), _settings.board.number_of_lines * 2)
        self.assertIsNotNone(_world.stones)
        self.assertEqual(len(_world.stones), _settings.number_of_stones)
        self.assertIsNotNone(_world.agents)
        self.assertEqual(len(_world.agents), _settings.number_of_agents)

    def test_single_agent_world(self):
        from oz import config
        from oz.world import settings
        from oz.world import world
        from oz.runner import transform
        from oz.runner import renderer
        from oz.agent import observation
        from oz.agent import action

        # create a world with one agent and no stone
        _settings = settings.Settings(config, 2, 0, 1)
        _world = world.World(_settings)
        _transform = transform.Transform(_settings.size, config.DEFAULT_DISPLAY_RESOLUTION)
        _renderer = renderer.Renderer(_world, _transform, config.DEFAULT_TRANSPARENT_COLOR_KEY)

        # [x] single agent world
        #     [x] random action
        #         [x] check dimension of rendered image
        #         [x] check consistence between touch and feedback
        #     [x] move agent to corner of environment and touch
        #         [x] check tactile feedback -- background
        #     [x] move agent to center of board
        #         [x] check tactile feedback -- board

        # random action
        _action = action.Action(None, None, act_randomly=True)
        _world.tick(_action, _renderer)
        self.assertIsNotNone(_world.agents[0])
        self.assertIsNotNone(_world.agents[0].current_observation)
        self.assertEqual(
            _world.agents[0].current_observation.world_image.shape,
            (
                round(config.DEFAULT_WORLD_SIZE_X * config.DEFAULT_DISPLAY_RESOLUTION),
                round(config.DEFAULT_WORLD_SIZE_Y * config.DEFAULT_DISPLAY_RESOLUTION),
                3
            )
        )
        if _action.touch:
            self.assertNotEqual(_world.agents[0].current_observation.feel,
                             observation.TactileQuality.nothing)
        else:
            self.assertEqual(_world.agents[0].current_observation.feel,
                             observation.TactileQuality.nothing)

        # force move to a corner and touch
        _move = (-config.DEFAULT_WORLD_SIZE_X, config.DEFAULT_WORLD_SIZE_Y)
        _touch = True
        _action = action.Action(_touch, _move)
        _world.tick(_action, _renderer)
        self.assertEqual(_world.agents[0].current_observation.feel,
                         observation.TactileQuality.background)

        # force move to the center corner and touch
        _move = (config.DEFAULT_WORLD_SIZE_X / 2, -config.DEFAULT_WORLD_SIZE_Y / 2)
        _touch = True
        _action = action.Action(_touch, _move)
        _world.tick(_action, _renderer)
        self.assertEqual(_world.agents[0].current_observation.kinesthetic, _move)
        self.assertEqual(_world.agents[0].current_observation.feel,
                         observation.TactileQuality.board)

    def test_agent_stone_interaction(self):
        from oz import config
        from oz.world import settings
        from oz.world import world
        from oz.runner import transform
        from oz.runner import renderer
        from oz.agent import observation
        from oz.agent import action

        # create a world with two stones and one agent
        _settings = settings.Settings(config, 2, 2, 1)
        _world = world.World(_settings)
        _agent = _world.agents[0]
        _target_stone = _world.stones[1]
        _transform = transform.Transform(_settings.size, config.DEFAULT_DISPLAY_RESOLUTION)
        _renderer = renderer.Renderer(_world, _transform, config.DEFAULT_TRANSPARENT_COLOR_KEY)

        # [x] world: single agent + two stones
        #     [x] check stone color difference
        #     [x] move agent to second stone and pick up stone
        #         [x] check holdings
        #         [x] check tactile feedback
        #         [x] check order of stones
        #     [x] move to center of board along with stone
        #         [x] check holdings
        #         [x] check tactile feedback
        #         [x] check agent location
        #         [x] check stone location
        #     [x] release stone
        #         [x] check holdings
        #         [x] check tactile feedback
        #         [x] check color of center of rendered image -- agent color
        #     [x] pick up stone again
        #         [x] check holdings
        #         [x] check tactile feedback
        #         [x] check color of center of rendered image -- color of first stone

        self.assertNotEqual(_world.stones[0].is_black, _world.stones[1].is_black)

        _min_x, _min_y, _, _ = _settings.bounds
        _world.stones[0].move_to((_min_x, _min_y)) # force move stone 0 to a corner

        # move agent to second stone and pick it up
        _agent_x, _agent_y = _agent.center
        _stone_x, _stone_y = _target_stone.center
        _move = (_stone_x - _agent_x, _stone_y - _agent_y)
        _touch = True
        _action = action.Action(_touch, _move)
        _world.tick(_action, _renderer)
        self.assertEqual(_world.holdings[_agent.index], _target_stone)
        self.assertEqual(_agent.current_observation.feel, observation.TactileQuality.stone)
        self.assertEqual(_world.stones[0], _target_stone)

        # move to the center
        _agent_x, _agent_y = _agent.center
        _move = (-_agent_x, -_agent_y)
        _touch = True
        _action = action.Action(_touch, _move)
        _world.tick(_action, _renderer)
        self.assertEqual(_world.holdings[_agent.index], _target_stone)
        self.assertEqual(_agent.current_observation.feel, observation.TactileQuality.stone)
        self.assertEqual(_agent.center, (0, 0))
        self.assertEqual(_target_stone.center, (0, 0)) # stone moved along with agent

        # release stone
        _move = (0, 0)
        _touch = False
        _action = action.Action(_touch, _move)
        _world.tick(_action, _renderer)
        self.assertIsNone(_world.holdings[_agent.index])
        self.assertEqual(_agent.current_observation.feel, observation.TactileQuality.nothing)
        _size_x, _size_y, _ = _agent.current_observation.world_image.shape
        _pixel_x, _pixel_y = round(_size_x / 2), round(_size_y / 2)
        _observed_color = tuple(_agent.current_observation.world_image[_pixel_x][_pixel_y])
        _expected_color = _world.settings.agent.color[:3]
        self.assertEqual(_observed_color, _expected_color)

        # pick up stone
        _move = (0, 0)
        _touch = True
        _action = action.Action(_touch, _move)
        _world.tick(_action, _renderer)
        self.assertEqual(_world.holdings[_agent.index], _target_stone)
        self.assertEqual(_agent.current_observation.feel, observation.TactileQuality.stone)
        _size_x, _size_y, _ = _agent.current_observation.world_image.shape
        _pixel_x, _pixel_y = round(_size_x / 2), round(_size_y / 2)
        _observed_color = tuple(_agent.current_observation.world_image[_pixel_x][_pixel_y])
        if _target_stone.is_black:
            _expected_color = _world.settings.stone.color_black[:3]
        else:
            _expected_color = _world.settings.stone.color_white[:3]
        self.assertEqual(_observed_color, _expected_color)

if __name__ == '__main__':
    unittest.main()
