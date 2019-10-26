import sys
import time

import pygame

import renderer
from action import Action

def capture_screen(surface, filepath, size, pos=(0, 0)):
    image = pygame.Surface(size)    # Create image surface
    image.blit(surface, (0, 0), (pos, size))    # Blit portion of the display to the image
    pygame.image.save(image, filepath)

class Transform:

    def __init__(self, world_size, dpm=600.0): # 600 dpm -- dots per meter
        size_x, size_y = world_size
        self._trans_x = size_x / 2.0
        self._trans_y = size_y / 2.0
        self._scale = dpm

    def scale2gui(self, value):
        return round(self._scale * value)

    def scale2gui2d(self, pair):
        first_value, second_value = pair
        return (self.scale2gui(first_value), self.scale2gui(second_value))

    def translate2gui2d(self, pair):
        current_x, current_y = pair
        return (current_x + self._trans_x, current_y + self._trans_y)

    def world2gui2d(self, pair):
        return self.scale2gui2d(self.translate2gui2d(pair))

    def world2gui4d(self, quad):
        current_x1, current_y1, current_x2, current_y2 = quad
        new_x1, new_y1 = self.world2gui2d((current_x1, current_y1))
        new_x2, new_y2 = self.world2gui2d((current_x2, current_y2))
        return (new_x1, new_y1, new_x2, new_y2)

    def scale2world(self, value):
        return value / self._scale

    def scale2world2d(self, pair):
        current_x, current_y = pair
        return (self.scale2world(current_x), self.scale2world(current_y))

    def translate2world2d(self, pair):
        current_x, current_y = pair
        return (current_x - self._trans_x, current_y - self._trans_y)

    def gui2world2d(self, pair):
        return self.translate2world2d(self.scale2world2d(pair))

def run_oz(world, cycles=-1, timing=False, capture_pngs=False, display_hz=50):

    # prepare transformation
    transform = Transform(world.size, 900)

    # initialize pygame
    pygame.init()
    size = transform.scale2gui2d(world.size)
    surface = pygame.display.set_mode(size) # NB: has to set mode before instantiate Renderer

    # prerender surfaces
    base_surface = renderer.render_base(world, transform)
    stone_black_surface, stone_white_surface = renderer.render_stone(world, transform)
    agent_down_surface, agent_up_surface = renderer.render_agent(world, transform)

    # initialize for interaction
    mouse_down = False
    gui_agent = world.agents[0]    # The 0th agent is a GUI agent
    gui_agent_x, gui_agent_y = gui_agent.center
    mouse_x, mouse_y = transform.world2gui2d((gui_agent_x, gui_agent_y))

    # manage cycles
    cycles_remain = cycles
    if timing:
        start = time.time()
    cycles_done = 0

    # manage display frame rate
    if display_hz > 0: # 0 for headless mode
        cycle_length = 1.0 / display_hz
        cycle_start = time.time()

    # run cycles
    while cycles < 0 or cycles_remain > 0:
        if cycles_remain > 0:
            cycles_remain -= 1

        # blit surfaces together
        surface.blit(base_surface, (0, 0))

        # reversed is needed to honor z-order of stones
        for stone in reversed(world.stones):
            center_x, center_y = stone.center
            radius = stone.radius
            target = transform.world2gui2d((center_x - radius, center_y - radius))
            if stone.is_black:
                surface.blit(stone_black_surface, target)
            else:
                surface.blit(stone_white_surface, target)

        gui_agent_x, gui_agent_y = gui_agent.center
        radius = gui_agent.radius
        target = transform.world2gui2d((gui_agent_x - radius, gui_agent_y - radius))
        if mouse_down:
            surface.blit(agent_down_surface, target)
        else:
            surface.blit(agent_up_surface, target)
        for agent in world.agents[1:]: # The 0th agent is a GUI agent
            agent_x, agent_y = agent.center
            target = transform.world2gui2d((agent_x - radius, agent_y - radius))
            radius = agent.radius
            if agent.current_action.press():
                surface.blit(agent_down_surface, target)
            else:
                surface.blit(agent_up_surface, target)

        # generate visual feedback
        a3d = pygame.surfarray.array3d(surface)

        # handle display frame rate
        if display_hz > 0: # 0 for headless mode
            cycle_now = time.time()
            if cycle_now - cycle_start >= cycle_length:
                pygame.display.flip()
                cycle_start = cycle_now

        # handle interaction
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

        # handle screen recording
        cycles_done += 1
        if capture_pngs and cycles_remain % 10 == 0:
            capture_screen(surface, "screenshot" + "{:05d}".format(cycles_done) + ".png", size)

        # handle interaction
        gui_agent_new_x, gui_agent_new_y = transform.gui2world2d((mouse_x, mouse_y))
        gui_agent_move = gui_agent_new_x - gui_agent_x, gui_agent_new_y - gui_agent_y
        gui_agent_x, gui_agent_y = gui_agent_new_x, gui_agent_new_y
        gui_agent_action = Action(mouse_down, gui_agent_move)

        # tick the world
        world.tick(gui_agent_action, a3d)

    # finish running
    if timing:
        end = time.time()
        time_elapsed = end - start
        time_per_cycle = time_elapsed / cycles
        print("Cycles: ", cycles, "  Time elasped: ", time_elapsed, "  Time per cycle: ", time_per_cycle)
