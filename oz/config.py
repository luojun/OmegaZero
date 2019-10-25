# TODO: understand namespace
# TODO: understand how to do constants
# TODO: understand how to do private utility method
# TODO: revise accordingly

import yaml

with open("config.yaml") as f:
    configs = yaml.full_load(f)

def _color_dict2tuple(d):
    return (d['r'], d['g'], d['b'], d['a'])

ENVIRONMENT_SIZE_X = configs['environment']['size']['x']
ENVIRONMENT_SIZE_Y = configs['environment']['size']['y']
ENVIRONMENT_BACKGROUND_COLOR = _color_dict2tuple(configs['environment']['background']['color'])

BOARD_SIZE_X_RATIO = configs['board']['size']['x']['ratio']
BOARD_SIZE_Y_RATIO = configs['board']['size']['y']['ratio']
BOARD_COLOR = _color_dict2tuple(configs['board']['color'])
BOARD_LINE_COLOR = _color_dict2tuple(configs['board']['line']['color'])
BOARD_LINE_WIDTH_RATIO = configs['board']['line']['width']['ratio']

STONE_SIZE_RATIO = configs['stone']['size']['ratio']
STONE_BLACK_COLOR = _color_dict2tuple(configs['stone']['black']['color'])
STONE_BLACK_EDGE_COLOR = _color_dict2tuple(configs['stone']['black']['edge']['color'])
STONE_BLACK_EDGE_WIDTH_RATIO = configs['stone']['black']['edge']['width']['ratio']
STONE_WHITE_COLOR = _color_dict2tuple(configs['stone']['white']['color'])
STONE_WHITE_EDGE_COLOR = _color_dict2tuple(configs['stone']['white']['edge']['color'])
STONE_WHITE_EDGE_WIDTH_RATIO = configs['stone']['white']['edge']['width']['ratio']

AGENT_COLOR = _color_dict2tuple(configs['agent']['color'])
AGENT_SIZE_RATIO = configs['agent']['size']['ratio']
AGENT_EDGE_COLOR = _color_dict2tuple(configs['agent']['edge']['color'])
AGENT_EDGE_WIDTH_RATIO = configs['agent']['edge']['width']['ratio']
