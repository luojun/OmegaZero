# TODO: add interaction support

import sys
import pygame
import numpy
from random import random
from pygame.locals import *

import time

from movable import Action
import env

def capture_screen(surface, filepath, size, pos = (0,0)):
  image = pygame.Surface(size)  # Create image surface
  image.blit(surface, (0,0), (pos,size))  # Blit portion of the display to the image
  pygame.image.save(image, filepath)

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


class Renderer:
  def __init__(self, e, t, pg):
    self._base = self._renderBase(e, t, pg)
    self._stoneBlack, self._stoneWhite = self._renderStone(e, t, pg)
    self._agentDown, self._agentUp = self._renderAgent(e, t, pg)
    # render background and board into one surface
    # render agent unpressed into one surface
    # render agent pressed into one surface
    # render white stone into one surface
    # render black stone into one surface

  def getBaseSurface(self):
    return self._base

  def getStoneSurfaces(self):
    return self._stoneBlack, self._stoneWhite

  def getAgentSurfaces(self):
    return self._agentDown, self._agentUp

  def _renderBase(self, e, t, pg):
    background_color = e.getBackgroundColor()
    b = e.getBoard()
    board_color = b.getColor()
    board_min_x, board_min_y, board_max_x, board_max_y = t.env2gui4d(b.getRect())
    board_rect = (board_min_x, board_min_y, board_max_x - board_min_x, board_max_y - board_min_y)

    line_color = b.getLineColor()
    lines = b.getLines()

    size = t.scale2gui2d(e.getSize())
    surface = pg.Surface(size)  # Create image surface

    surface.fill(background_color)
    pg.draw.rect(surface, board_color, board_rect, 0)

    line_width = t.scale2gui(b.getLineWidth())
    for (start_pos, end_pos) in lines:
      pg.draw.line(surface, line_color, t.env2gui2d(start_pos), t.env2gui2d(end_pos), line_width)

    return surface


  def _renderStone(self, e, t, pg):
    radius = t.scale2gui(e.getStoneRadius())
    center = (radius, radius)
    size = (radius * 2, radius * 2)
    blackColor = e.getStoneColorBlack()
    whiteColor = e.getStoneColorWhite()
    edge_blackColor = e.getStoneEdgeColorBlack()
    edge_whiteColor = e.getStoneEdgeColorWhite()
    #stoneBlackSurface = pg.Surface(size, pygame.SRCALPHA)
    #stoneWhiteSurface = pg.Surface(size, pygame.SRCALPHA)
    stoneBlackSurface = pg.Surface(size)
    stoneWhiteSurface = pg.Surface(size)
    # TODO: document the fact we are using (0, 0, 0) as color key
    stoneBlackSurface.set_colorkey((0,0,0), pygame.RLEACCEL)
    stoneWhiteSurface.set_colorkey((0,0,0), pygame.RLEACCEL)
    pygame.draw.circle(stoneBlackSurface, blackColor, center, radius, 0)
    pygame.draw.circle(stoneWhiteSurface, whiteColor, center, radius, 0)

    black_edge_width = t.scale2gui(e.getStoneBlackEdgeWidthRatio() * e.getStoneRadius())
    white_edge_width = t.scale2gui(e.getStoneWhiteEdgeWidthRatio() * e.getStoneRadius())

    pygame.draw.circle(stoneBlackSurface, edge_blackColor, center, radius, black_edge_width)
    pygame.draw.circle(stoneWhiteSurface, edge_whiteColor, center, radius, white_edge_width)
    #return stoneWhiteSurface.convert_alpha(), stoneBlackSurface.convert_alpha() # seems to hurt performance
    return stoneWhiteSurface, stoneBlackSurface

  def _renderAgent(self, e, t, pg):
    radius = t.scale2gui(e.getAgentRadius())
    center = (radius, radius)
    size = (radius * 2, radius * 2)
    color = e.getAgentColor()
    #agentDownSurface = pg.Surface(size, pygame.SRCALPHA)
    #agentUpSurface = pg.Surface(size, pygame.SRCALPHA)
    agentDownSurface = pg.Surface(size)
    agentUpSurface = pg.Surface(size)
    agentDownSurface.set_colorkey((0,0,0), pygame.RLEACCEL)
    agentUpSurface.set_colorkey((0,0,0), pygame.RLEACCEL)

    edge_width = t.scale2gui(e.getAgentEdgeWidthRatio() * e.getAgentRadius())
    pygame.draw.circle(agentDownSurface, color, center, radius, edge_width)
    pygame.draw.circle(agentUpSurface, color, center, radius, 0)
    #return agentDownSurface.convert_alpha(), agentUpSurface.convert_alpha() # seems to hurt performance
    return agentDownSurface, agentUpSurface

  def update(self, env):
    pass
    # blt things together

def runOzOpt(e, cycles=-1, timing=False, capture_pngs=False):
  trans = Transform(e.getSize(), 900)
  pygame.init()

  size = trans.scale2gui2d(e.getSize())
  surface = pygame.display.set_mode(size) # NB: has to set mode before instantiate Renderer

  renderer = Renderer(e, trans, pygame)
  baseSurface = renderer.getBaseSurface()
  stoneBlackSurface, stoneWhiteSurface = renderer.getStoneSurfaces()
  agentDownSurface, agentUpSurface = renderer.getAgentSurfaces()

  mouse_down = False
  picked_stone = None

  gui_agent = e.getAgents()[0]  # The 0th agent is a GUI agent
  gui_agent_x, gui_agent_y = gui_agent.getCenter()
  mouse_x, mouse_y = trans.env2gui2d((gui_agent_x, gui_agent_y))

  cycles_remain = cycles

  if timing:
    start = time.time()

  cycles_done = 0
  while cycles < 0 or cycles_remain > 0:
    if cycles_remain > 0:
      cycles_remain -= 1

    surface.blit(baseSurface, (0, 0))

    # blt the board to surface ...

    # draw stone into two separate surfaces, one for each state of the agent

    # reversed is needed to honor z-order of stones
    for stone in reversed(e.getStones()):
      x, y = stone.getCenter()
      radius = stone.getRadius()
      if stone.isBlack():
        surface.blit(stoneBlackSurface, trans.env2gui2d((x - radius, y - radius)))
      else:
        surface.blit(stoneWhiteSurface, trans.env2gui2d((x - radius, y - radius)))

    x, y = gui_agent.getCenter()
    radius = gui_agent.getRadius()
    if mouse_down:
      surface.blit(agentDownSurface, trans.env2gui2d((x - radius, y - radius)))
    else:
      surface.blit(agentUpSurface, trans.env2gui2d((x - radius, y - radius)))
    for agent in e.getAgents()[1:]: # The 0th agent is a GUI agent
      x, y = agent.getCenter()
      radius = agent.getRadius()
      if agent.getCurrentAction().press():
        surface.blit(agentDownSurface, trans.env2gui2d((x - radius, y - radius)))
      else:
        surface.blit(agentUpSurface, trans.env2gui2d((x - radius, y - radius)))

    a3d = pygame.surfarray.array3d(surface)
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_c:
          capture_screen(surface, "screenshot.png", size)
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

    cycles_done += 1
    if cycles_remain % 10 == 0:
      capture_screen(surface, "screenshot" + "{:05d}".format(cycles_done) + ".png", size)

    gui_agent_new_x, gui_agent_new_y = trans.gui2env2d((mouse_x, mouse_y))
    gui_agent_move = gui_agent_new_x - gui_agent_x, gui_agent_new_y - gui_agent_y

    gui_agent_x, gui_agent_y = gui_agent_new_x, gui_agent_new_y
    gui_agent_action = Action(mouse_down, gui_agent_move)
    e.tick(gui_agent_action, a3d)

  if timing:
    end = time.time()
    timeElapsed = end - start
    print("Cycles: ", cycles, "  Time elasped: ", timeElapsed, "  Time per cycle: ", timeElapsed / cycles)


def runOz(e, cycles=-1, timing=False):
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

  size = trans.scale2gui2d(e.getSize())
  surface = pygame.display.set_mode(size)

  mouse_down = False
  picked_stone = None

  gui_agent = e.getAgents()[0]  # The 0th agent is a GUI agent
  gui_agent_x, gui_agent_y = gui_agent.getCenter()
  mouse_x, mouse_y = trans.env2gui2d((gui_agent_x, gui_agent_y))

  cycles_remain = cycles

  if timing:
    start = time.time()

  while cycles < 0 or cycles_remain > 0:
    if cycles_remain > 0:
      cycles_remain -= 1

    surface.fill(background_color)

    # draw board into a separate surface out side of the loop
    pygame.draw.rect(surface, board_color, board_rect, 0)

    for (start_pos, end_pos) in lines:
      pygame.draw.line(surface, line_color, trans.env2gui2d(start_pos), trans.env2gui2d(end_pos), 3)

    # blt the board to surface ...

    # draw stone into two separate surfaces, one for each state of the agent

    # reversed is needed to honor z-order of stones
    for stone in reversed(e.getStones()):
      # blt
      pygame.draw.circle(surface, stone.getColor(), trans.env2gui2d(stone.getCenter()), trans.scale2gui(stone.getRadius()), 0)

    # draw agent into two separate surfaces, one for each state of the agent
    pygame.draw.circle(surface, gui_agent.getColor(), trans.env2gui2d(gui_agent.getCenter()), trans.scale2gui(gui_agent.getRadius()), (3 if mouse_down else 0))
    for agent in e.getAgents()[1:]: # The 0th agent is a GUI agent
      # blt
      pygame.draw.circle(surface, agent.getColor(), trans.env2gui2d(agent.getCenter()), trans.scale2gui(agent.getRadius()), 0)

    a3d = pygame.surfarray.array3d(surface)
    pygame.display.flip()

    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        sys.exit()
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_c:
          capture_screen(surface, "screenshot.png", size)
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
    gui_agent_action = Action(mouse_down, gui_agent_move)
    e.tick(gui_agent_action, a3d)

  if timing:
    end = time.time()
    timeElapsed = end - start
    print("Cycles: ", cycles, "  Time elasped: ", timeElapsed, "  Time per cycle: ", timeElapsed / cycles)



import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lines', nargs='?', default=4, type=int)
parser.add_argument('-s', '--stones', nargs='?', default=10, type=int)
parser.add_argument('-a', '--agents', nargs='?', default=2, type=int)
parser.add_argument('-x', '--width', nargs='?', default=1.0, type=float)
parser.add_argument('-y', '--height', nargs='?', default=1.0, type=float)
args = parser.parse_args()

e = env.Environment(1.0, 1.0, args.lines, args.stones, args.agents) # five-agent tic-tac-toe

# WITHOUT array3d
# Before optimization --
# Cycles:  1000   Time elasped:  2.808263063430786   Time per cycle:  0.0028082630634307863
# After optimization --
# Cycles:  1000   Time elasped:  2.2032926082611084   Time per cycle:  0.0022032926082611085
#e = env.Environment(1.0, 1.0, 19, 360, 5)

# WITHOUT array3d
# Before optimization --
# Cycles:  1000   Time elasped:  1.3584859371185303   Time per cycle:  0.0013584859371185303
# After optimization --
# Cycles:  1000   Time elasped:  1.215559720993042   Time per cycle:  0.001215559720993042
#e = env.Environment(1.0, 1.0, 4, 10, 6) # five-agent tic-tac-toe

# e = env.Environment()

#import cProfile
#cProfile.run('runOzOpt(e, cycles=100, timing=True)')

#runOz(e, cycles=1000, timing=True)

#runOzOpt(e, cycles=1000, timing=True)

#runOzOpt(e, cycles=5000, capture_pngs=True) # Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif

runOz(e)

