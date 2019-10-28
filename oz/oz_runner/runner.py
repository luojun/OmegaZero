import sys
import time

import pygame

from oz_runner import renderer
from oz_runner import transform
from oz_agent import action

class Runner:
    def __init__(self, world):
        self._world = world
        self._transform = transform.Transform(world.settings.size, 900) # TODO: config
        self._renderer = renderer.Renderer(self._world, self._transform)

    def _create_gui_agent_action(self, mouse_down, mouse_x, mouse_y):
        gui_agent_new_x, gui_agent_new_y = self._transform.view2world2d((mouse_x, mouse_y))
        gui_agent_x, gui_agent_y = self._world.agents[0].center # The 0th agent is a GUI agent
        gui_agent_move = gui_agent_new_x - gui_agent_x, gui_agent_new_y - gui_agent_y
        return action.Action(mouse_down, gui_agent_move)

    # TODO: refactor this into its proper parts
    def run(self, cycles=-1, timing=False, capture_pngs=False, display_hz=50):
        mouse_down = False
        gui_agent = self._world.agents[0]    # The 0th agent is a GUI agent
        mouse_x, mouse_y = self._transform.world2view2d(gui_agent.center)

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

            # handle interaction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit() # TODO: exit appropriately
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        capture_screen(self.surface, "screenshot.png", self._view_size)
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

            gui_agent_action = self._create_gui_agent_action(mouse_down, mouse_x, mouse_y)

            # tick the world
            self._world.tick(gui_agent_action, self._renderer)

            # handle display frame rate
            if display_hz > 0: # 0 for headless mode
                cycle_now = time.time()
                if cycle_now - cycle_start >= cycle_length:
                    pygame.display.flip()
                    cycle_start = cycle_now

            # screen recording
            cycles_done += 1
            if capture_pngs and cycles_remain % 10 == 0:
                png_path = "screenshot" + "{:05d}".format(cycles_done) + ".png"
                self.renderer.capture_screen(png_path)

        # finish running
        if timing:
            end = time.time()
            time_elapsed = end - start
            time_per_cycle = time_elapsed / cycles
            print("Cycles: ", cycles, "  Time elasped: ", time_elapsed, "  Time per cycle: ", time_per_cycle)
