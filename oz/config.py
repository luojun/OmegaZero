# TODO: understand namespace
# TODO: understand how to do constants
# TODO: understand how to do private utility method
# TODO: do all configuration logic / size calculation here and free other code from complication?
# TODO: separate differet parts of configration: board, world, agent, stone etc.
# TODO: revise accordingly

import yaml

with open("config.yaml") as f:
    CONFIGS = yaml.full_load(f)

def _color_dict2tuple(dictionary):
    return (dictionary['r'], dictionary['g'], dictionary['b'], dictionary['a'])

DEFAULT_WORLD_SIZE_X = CONFIGS['world']['size']['x']
DEFAULT_WORLD_SIZE_Y = CONFIGS['world']['size']['y']
DEFAULT_WORLD_BACKGROUND_COLOR = _color_dict2tuple(CONFIGS['world']['background']['color'])
DEFAULT_NUMBER_OF_AGENTS = CONFIGS['world']['agents']
DEFAULT_NUMBER_OF_STONES = CONFIGS['world']['stones']

DEFAULT_BOARD_NUMBER_OF_LINES = CONFIGS['board']['lines']
DEFAULT_BOARD_SIZE_X_RATIO = CONFIGS['board']['size']['x']['ratio']
DEFAULT_BOARD_SIZE_Y_RATIO = CONFIGS['board']['size']['y']['ratio']
DEFAULT_BOARD_COLOR = _color_dict2tuple(CONFIGS['board']['color'])
DEFAULT_BOARD_LINE_COLOR = _color_dict2tuple(CONFIGS['board']['line']['color'])
DEFAULT_BOARD_LINE_WIDTH_RATIO = CONFIGS['board']['line']['width']['ratio']

DEFAULT_STONE_SIZE_RATIO = CONFIGS['stone']['size']['ratio']
DEFAULT_STONE_COLOR_BLACK = _color_dict2tuple(CONFIGS['stone']['color']['black'])
DEFAULT_STONE_COLOR_WHITE = _color_dict2tuple(CONFIGS['stone']['color']['white'])
DEFAULT_STONE_EDGE_WIDTH_RATIO = CONFIGS['stone']['edge']['width']['ratio']
DEFAULT_STONE_EDGE_COLOR_BLACK = _color_dict2tuple(CONFIGS['stone']['edge']['color']['black'])
DEFAULT_STONE_EDGE_COLOR_WHITE = _color_dict2tuple(CONFIGS['stone']['edge']['color']['white'])

DEFAULT_AGENT_COLOR = _color_dict2tuple(CONFIGS['agent']['color'])
DEFAULT_AGENT_SIZE_RATIO = CONFIGS['agent']['size']['ratio']
DEFAULT_AGENT_EDGE_COLOR = _color_dict2tuple(CONFIGS['agent']['edge']['color'])
DEFAULT_AGENT_EDGE_WIDTH_RATIO = CONFIGS['agent']['edge']['width']['ratio']

DEFAULT_DISPLAY_HZ = CONFIGS['display']['hz']

class WorldConfig:
    def __init__(self):
        self.size_x = DEFAULT_WORLD_SIZE_X
        self.size_y = DEFAULT_WORLD_SIZE_Y
        self.background_color = DEFAULT_WORLD_BACKGROUND_COLOR
        self.number_of_agents = DEFAULT_NUMBER_OF_AGENTS
        self.number_of_stones = DEFAULT_NUMBER_OF_STONES

class BoardConfig:
    def __init__(self):
        self.number_of_lines = DEFAULT_BOARD_NUMBER_OF_LINES
        self.size_x_ratio = DEFAULT_BOARD_SIZE_X_RATIO
        self.size_y_ratio = DEFAULT_BOARD_SIZE_Y_RATIO
        self.color = DEFAULT_BOARD_COLOR
        self.line_color = DEFAULT_BOARD_LINE_COLOR
        self.line_width_ratio = DEFAULT_BOARD_LINE_WIDTH_RATIO

class StoneConfig:
    def __init__(self):
        self.size_ratio = DEFAULT_STONE_SIZE_RATIO
        self.color_black = DEFAULT_STONE_COLOR_BLACK
        self.color_white = DEFAULT_STONE_COLOR_WHITE
        self.edge_width_ratio = DEFAULT_STONE_EDGE_WIDTH_RATIO
        self.edge_color_black = DEFAULT_STONE_EDGE_COLOR_BLACK
        self.edge_color_white = DEFAULT_STONE_EDGE_COLOR_WHITE

class AgentConfig:
    def __init__(self):
        self.color = DEFAULT_AGENT_COLOR
        self.size_ratio = DEFAULT_AGENT_SIZE_RATIO
        self.edge_color = DEFAULT_AGENT_EDGE_COLOR
        self.edge_width_ratio = DEFAULT_AGENT_EDGE_WIDTH_RATIO

class MovableConfig:
    def __init__(self, color, edge_color, edge_width_ratio):
        self.color = color
        self.edge_color = edge_color
        self.edge_width_ratio = edge_width_ratio

class Config:
    def __init__(self):
        self.world = WorldConfig()
        self.board = BoardConfig()
        self.stone = StoneConfig()
        self.agent = AgentConfig()

