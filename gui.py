# TODO: add interaction support

import sys
import pygame
import numpy
from random import random
from pygame.locals import *

import env

class Transform:

  def __init__(self, env_size, dpm=600.0): # 600 dpm -- dots per meter
    size_x, size_y = env_size
    self._trans_x = size_x / 2.0
    self._trans_y = size_y / 2.0
    self._scale = dpm

  def scale2gui(self, f):
    return round(self._scale * f)

  def scale2gui2d(self, t2):
    x, y = t2
    return (self.scale2gui(x), self.scale2gui(y))

  def translate2gui2d(self, t2):
    x, y = t2
    return (x + self._trans_x, y + self._trans_y)

  def env2gui2d(self, t2):
    return self.scale2gui2d(self.translate2gui2d(t2))

  def env2gui4d(self, t4):
    x1, y1, x2, y2 = t4
    tx1, ty1 = self.env2gui2d((x1, y1))
    tx2, ty2 = self.env2gui2d((x2, y2))
    return (tx1, ty1, tx2, ty2)

  def scale2env(self, f):
    return f / self._scale

  def scale2env2d(self, t2):
    x, y = t2
    return (self.scale2env(x), self.scale2env(y))

  def translate2env2d(self, t2):
    x, y = t2
    return (x - self._trans_x, y - self._trans_y)

  def gui2env2d(self, t2):
    return self.translate2env2d(self.scale2env2d(t2))


# e = env.Environment(1.0, 1.0, 19, 360, 5)
e = env.Environment(1.0, 1.0, 4, 10, 3) # three-agent tic-tac-toe
# e = env.Environment()
trans = Transform(e.getSize(), 1200)

background_color = e.getBackgroundColor()

b = e.getBoard()
board_color = b.getColor()
board_min_x, board_min_y, board_max_x, board_max_y = trans.env2gui4d(b.getRect())
board_rect = (board_min_x, board_min_y, board_max_x - board_min_x, board_max_y - board_min_y)

line_color = b.getLineColor()
lines = b.getLines()

stones = e.getStones()

pygame.init()

#ball = pygame.image.load("intro_ball.gif")
#ballrect = ball.get_rect()

size = trans.scale2gui2d(e.getSize())
surface = pygame.display.set_mode(size)

mouse_down = False
picked_stone = None

gui_agent = e.getAgents()[0]  # The 0th agent is a GUI agent
gui_agent_x, gui_agent_y = gui_agent.getCenter()
mouse_x, mouse_y = trans.env2gui2d((gui_agent_x, gui_agent_y))

while 1:
  surface.fill(background_color)
  pygame.draw.rect(surface, board_color, board_rect, 0)

  for (start_pos, end_pos) in lines:
    pygame.draw.line(surface, line_color, trans.env2gui2d(start_pos), trans.env2gui2d(end_pos), 3)

  for stone in e.getStones():
    pygame.draw.circle(surface, stone.getColor(), trans.env2gui2d(stone.getCenter()), trans.scale2gui(stone.getRadius()), 0)

  pygame.draw.circle(surface, gui_agent.getColor(), trans.env2gui2d(gui_agent.getCenter()), trans.scale2gui(gui_agent.getRadius()), (3 if mouse_down else 0))
  for agent in e.getAgents()[1:]: # The 0th agent is a GUI agent
    pygame.draw.circle(surface, agent.getColor(), trans.env2gui2d(agent.getCenter()), trans.scale2gui(agent.getRadius()), 0)

#  surface.blit(ball, ballrect)
  a3d = pygame.surfarray.array3d(surface)
  pygame.display.flip()

  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
      mouse_down = True
      mouse_x = event.pos[0]
      mouse_y = event.pos[1]
    elif event.type == pygame.MOUSEBUTTONUP:
      mouse_down = False
      mouse_x = event.pos[0]
      mouse_y = event.pos[1]
    elif event.type == pygame.MOUSEMOTION:
      mouse_x = event.pos[0]
      mouse_y = event.pos[1]

  gui_agent_new_x, gui_agent_new_y = trans.gui2env2d((mouse_x, mouse_y))
  gui_agent_move = gui_agent_new_x - gui_agent_x, gui_agent_new_y - gui_agent_y

  gui_agent_x, gui_agent_y = gui_agent_new_x, gui_agent_new_y
  gui_agent_action = env.Action(mouse_down, gui_agent_move)
  e.tick(gui_agent_action, a3d)
