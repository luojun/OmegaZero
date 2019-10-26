# TODO: understand namespace
# TODO: understand how to do constants
# TODO: understand how to do private utility method
# TODO: revise accordingly

import yaml

with open("config.yaml") as f:
    CONFIGS = yaml.full_load(f)

def _color_dict2tuple(dictionary):
    return (dictionary['r'], dictionary['g'], dictionary['b'], dictionary['a'])

ENVIRONMENT_SIZE_X = CONFIGS['environment']['size']['x']
ENVIRONMENT_SIZE_Y = CONFIGS['environment']['size']['y']
ENVIRONMENT_BACKGROUND_COLOR = _color_dict2tuple(CONFIGS['environment']['background']['color'])

BOARD_SIZE_X_RATIO = CONFIGS['board']['size']['x']['ratio']
BOARD_SIZE_Y_RATIO = CONFIGS['board']['size']['y']['ratio']
BOARD_COLOR = _color_dict2tuple(CONFIGS['board']['color'])
BOARD_LINE_COLOR = _color_dict2tuple(CONFIGS['board']['line']['color'])
BOARD_LINE_WIDTH_RATIO = CONFIGS['board']['line']['width']['ratio']

STONE_SIZE_RATIO = CONFIGS['stone']['size']['ratio']
STONE_BLACK_COLOR = _color_dict2tuple(CONFIGS['stone']['black']['color'])
STONE_BLACK_EDGE_COLOR = _color_dict2tuple(CONFIGS['stone']['black']['edge']['color'])
STONE_BLACK_EDGE_WIDTH_RATIO = CONFIGS['stone']['black']['edge']['width']['ratio']
STONE_WHITE_COLOR = _color_dict2tuple(CONFIGS['stone']['white']['color'])
STONE_WHITE_EDGE_COLOR = _color_dict2tuple(CONFIGS['stone']['white']['edge']['color'])
STONE_WHITE_EDGE_WIDTH_RATIO = CONFIGS['stone']['white']['edge']['width']['ratio']

AGENT_COLOR = _color_dict2tuple(CONFIGS['agent']['color'])
AGENT_SIZE_RATIO = CONFIGS['agent']['size']['ratio']
AGENT_EDGE_COLOR = _color_dict2tuple(CONFIGS['agent']['edge']['color'])
AGENT_EDGE_WIDTH_RATIO = CONFIGS['agent']['edge']['width']['ratio']
