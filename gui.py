# TODO: add interaction support

import sys, pygame
from random import random
from pygame.locals import *

import env

class ToGui:

  def __init__(self, env_size, dpm=600): # 600 dpm -- dots per meter
    size_x, size_y = env_size
    self._trans_x = size_x / 2.0
    self._trans_y = size_y / 2.0
    self._scale = dpm

  def scale(self, f):
    return round(self._scale * f)

  def scale2d(self, t2):
    x, y = t2
    return (self.scale(x), self.scale(y))

  def translate2d(self, t2):
    x, y = t2
    return (x + self._trans_x, y + self._trans_y)

  def transform2d(self, t2):
    return self.scale2d(self.translate2d(t2))

  def transform4d(self, t4):
    x1, y1, x2, y2 = t4
    tx1, ty1 = self.transform2d((x1, y1))
    tx2, ty2 = self.transform2d((x2, y2))
    return (tx1, ty1, tx2, ty2)

e = env.Environment(1.0, 1.0, 19, 360, 2)
#e = env.Environment()
toGui = ToGui(e.getSize(), 1200)

background_color = e.getBackgroundColor()

b = e.getBoard()
board_color = b.getColor()
board_min_x, board_min_y, board_max_x, board_max_y = toGui.transform4d(b.getRect())
board_rect = (board_min_x, board_min_y, board_max_x - board_min_x, board_max_y - board_min_y)

line_color = b.getLineColor()
lines = b.getLines()

stones = e.getStones()

pygame.init()

#ball = pygame.image.load("intro_ball.gif")
#ballrect = ball.get_rect()

size = toGui.scale2d(e.getSize())
screen = pygame.display.set_mode(size)

mouse_x, mouse_y = 0, 0
mouse_down = False
picked_stone = None

while 1:
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      # print('Pressed button ', event.button, ' at ', event.pos) 
#      if mouse_down == False:
#        picked_stone = e.pickStone(toEnv(event.pos))
      mouse_down = True
    elif event.type == pygame.MOUSEBUTTONUP:
      # print('Released button ', event.button, ' at ', event.pos) 
      picked_stone = None
      mouse_down = False
    elif event.type == pygame.MOUSEMOTION:
      # print('Moved mouse at ', event.pos, ' by ', event.rel) 
#      if picked_stone != None:
#        e.moveStone(pickedStone, toEvn(event.rel))
      mouse_x = event.pos[0]
      mouse_y = event.pos[1]

  screen.fill(background_color)
  pygame.draw.rect(screen, board_color, board_rect, 0)

  for (start_pos, end_pos) in lines:
    pygame.draw.line(screen, line_color, toGui.transform2d(start_pos), toGui.transform2d(end_pos), 3) 

  for stone in e.getStones():
    pygame.draw.circle(screen, stone.getColor(), toGui.transform2d(stone.getCenter()), toGui.scale(stone.getRadius()), 0)

  for agent in e.getAgents():
    pygame.draw.circle(screen, agent.getColor(), toGui.transform2d(agent.getCenter()), toGui.scale(agent.getRadius()), 0)

  pygame.draw.circle(screen, Color(128, 128, 128, 64), (mouse_x, mouse_y), 30, (3 if mouse_down else 0))

#  screen.blit(ball, ballrect)
  pygame.display.flip()

  e.tick()

