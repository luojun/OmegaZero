import sys
import time

import pygame

import oz_config
from oz_runner import renderer
from oz_runner import transform
from oz_agent import action

def _update_mouse(event, mouse_down, mouse_x, mouse_y):
    if event.type == pygame.MOUSEBUTTONDOWN:
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
    return mouse_down, mouse_x, mouse_y

class Runner:
    def __init__(self, world, resolution):
        self._world = world
        self._transform = transform.Transform(world.settings.size, resolution)
        self._renderer = renderer.Renderer(self._world, self._transform)

    def _make_gui_agent_action(self, mouse_down, mouse_x, mouse_y):
        agent_new_x, agent_new_y = self._transform.view2world2d((mouse_x, mouse_y))
        agent_x, agent_y = self._world.gui_agent.center
        agent_move = agent_new_x - agent_x, agent_new_y - agent_y
        return action.Action(mouse_down, agent_move)

    def run(self, cycles=-1, timing=False, capture_pngs=False, display_hz=50):
        mouse_down = False
        gui_agent = self._world.gui_agent
        mouse_x, mouse_y = self._transform.world2view2d(gui_agent.center)

        # manage cycles
        cycles_remain = cycles

        # prepare for timing
        if timing:
            start = time.time()

        # prepare for screen capture
        cycles_done = 0

        # manage display frame rate
        if display_hz > 0: # 0 for headless mode
            cycle_length = 1.0 / display_hz
            cycle_start = time.time()

        terminate_now = False

        # run cycles
        while cycles < 0 or cycles_remain > 0:
            if cycles_remain > 0:
                cycles_remain -= 1

            # handle interaction
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    terminate_now = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        capture_screen(self.surface, "screenshot.png", self._view_size)
                else:
                    mouse_down, mouse_x, mouse_y = _update_mouse(
                        event, mouse_down, mouse_x, mouse_y
                    )
            if terminate_now:
                break

            gui_agent_action = self._make_gui_agent_action(mouse_down, mouse_x, mouse_y)

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
            print("Cycles: ", cycles, "  Time elasped: ", time_elapsed,
                  "  Time per cycle: ", time_per_cycle)
