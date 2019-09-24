import sys, pygame
from random import random

pygame.init()

environment_size = width, height = 600, 600
background_color = pygame.Color(64, 128, 0)

board_size = board_width, board_height = width / 3 * 2, height / 3 * 2
board_origin = board_x, board_y = (width - board_width) / 2, (height - board_height) / 2
board_rect = pygame.Rect(board_origin, board_size)
board_color = pygame.Color(128, 64, 32)

board_lines = 4 # 4 for tic-tac-toe; 19 for Go
board_inset = board_width / (board_lines + 1)
board_w_line_endpoints = [((board_x + board_inset, board_y + board_inset * (n + 1)), (board_x + board_width - board_inset, board_y + board_inset * (n + 1))) for n in range(board_lines)]
board_h_line_endpoints = [((board_x + board_inset * (n + 1), board_y + board_inset), (board_x + board_inset * (n + 1), board_y + board_width - board_inset)) for n in range(board_lines)]
line_color = pygame.Color(32, 32, 32)

number_of_stones = 10 # 10 for tic-tac-toe; 360 for Go
stone_size = board_inset / 5 * 4
stone_radius = round(stone_size / 2)
stone_color_white = pygame.Color(224, 224, 224)
stone_color_black = pygame.Color(32, 32, 32)

# scale [0, 1] to [stone_radius, width - stone_radius]
stones = [((stone_color_white if (n % 2) == 0 else stone_color_black), (round(random() * (width - stone_size) + stone_radius), round(random() * (height - stone_size) + stone_radius)), stone_radius) for n in range(number_of_stones)]

screen = pygame.display.set_mode(environment_size)
#ball = pygame.image.load("intro_ball.gif")
#ballrect = ball.get_rect()

while 1:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(background_color)
    pygame.draw.rect(screen, board_color, board_rect, 0)

    for (start_pos, end_pos) in board_w_line_endpoints:
        pygame.draw.line(screen, line_color, start_pos, end_pos, 3) 
    for (start_pos, end_pos) in board_h_line_endpoints:
        pygame.draw.line(screen, line_color, start_pos, end_pos, 3) 

    for (color, center, radius) in stones:
        pygame.draw.circle(screen, color, center, radius, 0)

#    screen.blit(ball, ballrect)
    pygame.display.flip()
