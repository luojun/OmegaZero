import sys
import time

import pygame

from runner import renderer
from runner import transform
from agent import action

def capture_screen(surface, filepath, size, pos=(0, 0)):
    image = pygame.Surface(size)    # Create image surface
    image.blit(surface, (0, 0), (pos, size))    # Blit portion of the display to the image
    pygame.image.save(image, filepath)

def _initialize_pygame(view_size):
    pygame.init()
    surface = pygame.display.set_mode(view_size)
    return surface

class Runner:
    def __init__(self, world):
        self._world = world
        self._transform = transform.Transform(world.size, 900) # TODO: turn 900 into a config
        self._view_size = self._transform.scale2view2d(self._world.size)
        # NB: has to set mode before instantiate Renderer
        self._surface = _initialize_pygame(self._view_size)
        self._base = renderer.render_base(self._world, self._transform)
        self._stone_black, self._stone_white = renderer.render_stone(self._world, self._transform)
        self._agent_down, self._agent_up = renderer.render_agent(self._world, self._transform)

    def _blit_all(self):
        self._surface.blit(self._base, (0, 0))

        # reversed is needed to honor z-order of stones
        for stone in reversed(self._world.stones):
            center_x, center_y = stone.center
            radius = stone.radius
            target = self._transform.world2view2d((center_x - radius, center_y - radius))
            if stone.is_black:
                self._surface.blit(self._stone_black, target)
            else:
                self._surface.blit(self._stone_white, target)

        for agent in self._world.agents:
            agent_x, agent_y = agent.center
            radius = agent.radius
            target = self._transform.world2view2d((agent_x - radius, agent_y - radius))
            if agent.current_action.touch:
                self._surface.blit(self._agent_down, target)
            else:
                self._surface.blit(self._agent_up, target)

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

            self._blit_all()

            # generate visual feedback
            a3d = pygame.surfarray.array3d(self._surface)

            # handle display frame rate
            if display_hz > 0: # 0 for headless mode
                cycle_now = time.time()
                if cycle_now - cycle_start >= cycle_length:
                    pygame.display.flip()
                    cycle_start = cycle_now

            # handle screen recording
            cycles_done += 1
            if capture_pngs and cycles_remain % 10 == 0:
                capture_screen(self.surface, "screenshot" + "{:05d}".format(cycles_done)
                               + ".png", self._view_size)

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
            self._world.tick(gui_agent_action, a3d)

        # finish running
        if timing:
            end = time.time()
            time_elapsed = end - start
            time_per_cycle = time_elapsed / cycles
            print("Cycles: ", cycles, "  Time elasped: ", time_elapsed, "  Time per cycle: ", time_per_cycle)
