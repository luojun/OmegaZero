class Settings:
    def __init__(self, config, number_of_lines=None,
                               number_of_stones=None,
                               number_of_agents=None):
        if number_of_lines is None:
            number_of_lines=config.DEFAULT_BOARD_NUMBER_OF_LINES
        if number_of_stones is None:
            number_of_stones=config.DEFAULT_NUMBER_OF_STONES
        if number_of_agents is None:
            number_of_agents=config.DEFAULT_NUMBER_OF_AGENTS

        size_x = config.DEFAULT_WORLD_SIZE_X
        size_y = config.DEFAULT_WORLD_SIZE_Y
        self._size = (size_x, size_y)
        center_x, center_y = 0.0, 0.0
        min_x, min_y = center_x - size_x / 2, center_y - size_y / 2
        max_x, max_y = center_x + size_x / 2, center_y + size_y / 2
        self._center = (center_x, center_y)
        self._bounds = (min_x, min_y, max_x, max_y)

        self._background_settings = BackgroundSettings(config)
        self._board_settings = BoardSettings(self, config, number_of_lines)

        self._stone_settings = StoneSettings(self.board, config)
        self._number_of_stones = number_of_stones
        self._agent_settings = AgentSettings(self.stone, config)
        self._number_of_agents = number_of_agents

    @property
    def size(self):
        return self._size

    @property
    def center(self):
        return self._center

    @property
    def bounds(self):
        return self._bounds

    @property
    def background(self):
        return self._background_settings

    @property
    def board(self):
        return self._board_settings

    @property
    def stone(self):
        return self._stone_settings

    @property
    def number_of_stones(self):
        return self._number_of_stones

    @property
    def agent(self):
        return self._agent_settings

    @property
    def number_of_agents(self):
        return self._number_of_agents

class BackgroundSettings:
    def __init__(self, config):
        self._color = config.DEFAULT_WORLD_BACKGROUND_COLOR

    @property
    def color(self):
        return self._color

class BoardSettings:
    def __init__(self, world_settings, config, number_of_lines):
        world_size_x, world_size_y = world_settings.size
        size_x = world_size_x * config.DEFAULT_BOARD_SIZE_X_RATIO
        size_y = world_size_y * config.DEFAULT_BOARD_SIZE_Y_RATIO
        self._size = (size_x, size_y)

        self._center = world_settings.center

        self._color = config.DEFAULT_BOARD_COLOR

        board_inset_x = size_x / (number_of_lines + 1)
        board_inset_y = size_y / (number_of_lines + 1)
        self._insets = (board_inset_x, board_inset_y)

        max_inset = max(board_inset_x, board_inset_y)
        self._line_width = config.DEFAULT_BOARD_LINE_WIDTH_RATIO * max_inset
        self._line_color = config.DEFAULT_BOARD_LINE_COLOR
        self._number_of_lines = number_of_lines

    @property
    def size(self):
        return self._size

    @property
    def center(self):
        return self._center

    @property
    def color(self):
        return self._color

    @property
    def insets(self):
        return self._insets

    @property
    def line_width(self):
        return self._line_width

    @property
    def line_color(self):
        return self._line_color

    @property
    def number_of_lines(self):
        return self._number_of_lines

class StoneSettings:
    def __init__(self, board_settings, config):
        stone_size = min(board_settings.insets) * config.DEFAULT_STONE_SIZE_RATIO
        self._radius = stone_size / 2
        self._color_black = config.DEFAULT_STONE_COLOR_BLACK
        self._color_white = config.DEFAULT_STONE_COLOR_WHITE
        self._edge_width = self.radius * config.DEFAULT_STONE_EDGE_WIDTH_RATIO
        self._edge_color_black = config.DEFAULT_STONE_EDGE_COLOR_BLACK
        self._edge_color_white = config.DEFAULT_STONE_EDGE_COLOR_WHITE

    @property
    def radius(self):
        return self._radius

    @property
    def color_black(self):
        return self._color_black

    @property
    def color_white(self):
        return self._color_white

    @property
    def edge_width(self):
        return self._edge_width

    @property
    def edge_color_black(self):
        return self._edge_color_black

    @property
    def edge_color_white(self):
        return self._edge_color_white

class AgentSettings:
    def __init__(self, stone_settings, config):
        self._radius = stone_settings.radius * config.DEFAULT_AGENT_SIZE_RATIO
        self._color = config.DEFAULT_AGENT_COLOR
        self._edge_width = self.radius * config.DEFAULT_AGENT_EDGE_WIDTH_RATIO
        self._edge_color = config.DEFAULT_AGENT_EDGE_COLOR

    @property
    def radius(self):
        return self._radius

    @property
    def color(self):
        return self._color

    @property
    def edge_width(self):
        return self._edge_width

    @property
    def edge_color(self):
        return self._edge_color
