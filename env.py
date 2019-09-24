from random import random

# TODO: OO
# TODO: write tests
# TODO: add YAML configuration

environment_size = environment_size_x, environment_size_y = 0.6, 0.6 # meters
environment_center = environment_center_x, environment_center_y = 0.0, 0.0
environment_min_x, environment_min_y = environment_center_x - environment_size_x / 2, environment_center_y - environment_size_y / 2
background_color = (64, 128, 0, 255) # RGBA

board_size = board_size_x, board_size_y = environment_size_x / 3.0 * 2.0, environment_size_y / 3.0 * 2.0 # allow size_x and size_y to be different
board_center = board_center_x, board_center_y = environment_center_x, environment_center_y # center of board
board_min_x, board_min_y = board_center_x - board_size_x / 2, board_center_y - board_size_y / 2
board_color = (128, 64, 32, 255) # RGBA
board_lines = 4 # 4 for tic-tac-toe; 19 for Go
board_inset_x = board_size_x / (board_lines + 1)
board_inset_y = board_size_y / (board_lines + 1)
board_line_min_x = board_min_x + board_inset_x
board_line_min_y = board_min_y + board_inset_y
board_line_max_x = board_min_x + board_size_x - board_inset_x
board_line_max_y = board_min_y + board_size_y - board_inset_y
board_line_inc_x = board_inset_x
board_line_inc_y = board_inset_y
board_x_line_endpoints = [((board_line_min_x, board_line_min_y + board_line_inc_y * n), (board_line_max_x, board_line_min_y + board_line_inc_y * n)) for n in range(board_lines)]
board_y_line_endpoints = [((board_line_min_x + board_line_inc_x * n, board_line_min_y), (board_line_min_x + board_line_inc_x * n, board_line_max_y)) for n in range(board_lines)]
board_line_color = (32, 32, 32, 255) # RGBA

number_of_stones = 10 # 10 for tic-tac-toe; 360 for Go
stone_size = min(board_inset_x, board_inset_y) / 5 * 4
stone_radius = stone_size / 2
stone_color_white = (224, 224, 224, 255)
stone_color_black = (32, 32, 32, 255)

# scale [0, 1] to [stone_radius, size_x - stone_radius]
stones = [((stone_color_white if (n % 2) == 0 else stone_color_black), (environment_min_x + stone_radius + random() * (environment_size_x - stone_size), stone_radius + random() * (environment_min_y + environment_size_y - stone_size)), stone_radius) for n in range(number_of_stones)]

origin = environment_center # origin is at center of environment

for (start_pos, end_pos) in board_x_line_endpoints:
    print(board_line_color, start_pos, end_pos)
for (start_pos, end_pos) in board_y_line_endpoints:
    print(board_line_color, start_pos, end_pos)

for (color, center, radius) in stones:
    print(color, center, radius)

