# TODO: factorize this into oz_runner.py, oz_renderer.py and oz_gui.py:
# TODO: make oz_runner.py the code that binds oz_world, oz_renderer and oz_gui
# TODO: structure oz_runner.py such that it could support a web-based remote oz_agent
# TODO: make oz_gui.py responsible solely for gui interaction and
# TODO: make oz_renderer.py responsible for rendering
# TODO: make oz_gui and oz_renderer independent, with shared Pygame dependency a convenient implementation detail
# TODO: make code compliant with Python style 

import sys
import pygame
import numpy
from random import random
from pygame.locals import *

import time

from movable import Action
import env

def capture_screen(surface, filepath, size, pos = (0, 0)):
    image = pygame.Surface(size)    # Create image surface
    image.blit(surface, (0, 0), (pos,size))    # Blit portion of the display to the image
    pygame.image.save(image, filepath)

class Transform:

    def __init__(self, env_size, dpm=600.0): # 600 dpm -- dots per meter
        size_x, size_y = env_size
        self._trans_x = size_x / 2.0
        self._trans_y = size_y / 2.0
        self._scale = dpm

    def scale2gui(self, value):
        return round(self._scale * value)

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

    def scale2env(self, value):
        return value / self._scale

    def scale2env2d(self, t2):
        x, y = t2
        return (self.scale2env(x), self.scale2env(y))

    def translate2env2d(self, t2):
        x, y = t2
        return (x - self._trans_x, y - self._trans_y)

    def gui2env2d(self, t2):
        return self.translate2env2d(self.scale2env2d(t2))


class Renderer:
    def __init__(self, environment, transform):
        self._base = self._renderBase(environment, transform)
        self._stone_black, self._stone_white = self._render_stone(environment, transform)
        self._agent_down, self._agent_up = self._render_agent(environment, transform)

    @property
    def base_surface(self):
        return self._base

    @property
    def stone_surfaces(self):
        return self._stone_black, self._stone_white

    @property
    def agent_surfaces(self):
        return self._agent_down, self._agent_up

    def _renderBase(self, environment, transform):
        board = environment.board
        board_color = board.color
        board_min_x, board_min_y, board_max_x, board_max_y = transform.env2gui4d(board.rect)
        board_rect = (board_min_x, board_min_y, board_max_x - board_min_x, board_max_y - board_min_y)

        line_color = board.line_color
        lines = board.lines

        size = transform.scale2gui2d(environment.size)
        surface = pygame.Surface(size)    # Create image surface

        surface.fill(environment.background_color)
        pygame.draw.rect(surface, board_color, board_rect, 0)

        line_width = transform.scale2gui(board.line_width)
        for (start_pos, end_pos) in lines:
            pygame.draw.line(surface, line_color, transform.env2gui2d(start_pos), transform.env2gui2d(end_pos), line_width)

        return surface


    def _render_stone(self, environment, transform):
        radius = transform.scale2gui(environment.stone_radius)
        center = (radius, radius)
        size = (radius * 2, radius * 2)
        stone_color_black, stone_color_white = environment.stone_colors
        stone_edge_color_black, stone_edge_color_white = environment.stone_edge_colors
        stone_black_surface = pygame.Surface(size)
        stone_white_surface = pygame.Surface(size)

        # TODO: document the fact we are using (0, 0, 0) as color key
        stone_black_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        stone_white_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        pygame.draw.circle(stone_black_surface, stone_color_black, center, radius, 0)
        pygame.draw.circle(stone_white_surface, stone_color_white, center, radius, 0)

        edge_width = transform.scale2gui(environment.stone_edge_width)

        pygame.draw.circle(stone_black_surface, stone_edge_color_black, center, radius, edge_width)
        pygame.draw.circle(stone_white_surface, stone_edge_color_white, center, radius, edge_width)
        return stone_black_surface, stone_white_surface

    def _render_agent(self, environment, transform):
        radius = transform.scale2gui(environment.agent_radius)
        center = (radius, radius)
        size = (radius * 2, radius * 2)
        color = environment.agent_color
        agent_down_surface = pygame.Surface(size)
        agent_up_surface = pygame.Surface(size)
        agent_down_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)
        agent_up_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)

        edge_width = transform.scale2gui(environment.agent_edge_width)
        pygame.draw.circle(agent_down_surface, color, center, radius, edge_width)
        pygame.draw.circle(agent_up_surface, color, center, radius, 0)
        return agent_down_surface, agent_up_surface

    def update(self, environment):
        pass
        # blt things together

def runOzOpt(environment, cycles=-1, timing=False, capture_pngs=False, display_hz=50):
    transform = Transform(environment.size, 900)
    pygame.init()

    size = transform.scale2gui2d(environment.size)
    surface = pygame.display.set_mode(size) # NB: has to set mode before instantiate Renderer

    renderer = Renderer(environment, transform)
    base_surface = renderer.base_surface
    stone_black_surface, stone_white_surface = renderer.stone_surfaces
    agent_down_surface, agent_up_surface = renderer.agent_surfaces

    mouse_down = False
    picked_stone = None

    gui_agent = environment.agents[0]    # The 0th agent is a GUI agent
    gui_agent_x, gui_agent_y = gui_agent.center
    mouse_x, mouse_y = transform.env2gui2d((gui_agent_x, gui_agent_y))

    cycles_remain = cycles

    if timing:
        start = time.time()

    cycles_done = 0

    if display_hz > 0: # 0 for headless mode
        cycle_length = 1.0 / display_hz
        cycle_start = time.time()

    while cycles < 0 or cycles_remain > 0:
        if cycles_remain > 0:
            cycles_remain -= 1

        surface.blit(base_surface, (0, 0))

        # reversed is needed to honor z-order of stones
        for stone in reversed(environment.stones):
            x, y = stone.center
            radius = stone.radius
            if stone.is_black:
                surface.blit(stone_black_surface, transform.env2gui2d((x - radius, y - radius)))
            else:
                surface.blit(stone_white_surface, transform.env2gui2d((x - radius, y - radius)))

        x, y = gui_agent.center
        radius = gui_agent.radius
        if mouse_down:
            surface.blit(agent_down_surface, transform.env2gui2d((x - radius, y - radius)))
        else:
            surface.blit(agent_up_surface, transform.env2gui2d((x - radius, y - radius)))
        for agent in environment.agents[1:]: # The 0th agent is a GUI agent
            x, y = agent.center
            radius = agent.radius
            if agent.current_action.press():
                surface.blit(agent_down_surface, transform.env2gui2d((x - radius, y - radius)))
            else:
                surface.blit(agent_up_surface, transform.env2gui2d((x - radius, y - radius)))

        a3d = pygame.surfarray.array3d(surface)

        if display_hz > 0: # 0 for headless mode
            cycle_now = time.time()
            if cycle_now - cycle_start >= cycle_length:
                pygame.display.flip()
                cycle_start = cycle_now

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
        if capture_pngs and cycles_remain % 10 == 0:
            capture_screen(surface, "screenshot" + "{:05d}".format(cycles_done) + ".png", size)

        gui_agent_new_x, gui_agent_new_y = transform.gui2env2d((mouse_x, mouse_y))
        gui_agent_move = gui_agent_new_x - gui_agent_x, gui_agent_new_y - gui_agent_y

        gui_agent_x, gui_agent_y = gui_agent_new_x, gui_agent_new_y
        gui_agent_action = Action(mouse_down, gui_agent_move)
        environment.tick(gui_agent_action, a3d)

    if timing:
        end = time.time()
        time_elapsed = end - start
        print("Cycles: ", cycles, "    Time elasped: ", time_elapsed, "    Time per cycle: ", time_elapsed / cycles)

