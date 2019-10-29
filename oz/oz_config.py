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
DEFAULT_DISPLAY_RESOLUTION = CONFIGS['display']['resolution']
