import pygame

from oz_runner import transform

def _initialize_pygame(view_size):
    pygame.init()
    surface = pygame.display.set_mode(view_size)
    return surface

def render_base(world, transform):
    board_color = world.settings.board.color
    board_min_x, board_min_y, board_max_x, board_max_y = transform.world2view4d(world.board.rect)
    board_width = board_max_x - board_min_x
    board_height = board_max_y - board_min_y
    board_rect = (board_min_x, board_min_y, board_width, board_height)

    line_color = world.settings.board.line_color
    lines = world.board.lines

    size = transform.scale2view2d(world.settings.size)
    surface = pygame.Surface(size)

    surface.fill(world.settings.background.color)
    pygame.draw.rect(surface, board_color, board_rect, 0)

    line_width = transform.scale2view(world.settings.board.line_width)
    for (start_pos, end_pos) in lines:
        line_start = transform.world2view2d(start_pos)
        line_end = transform.world2view2d(end_pos)
        pygame.draw.line(surface, line_color, line_start, line_end, line_width)

    return surface

def render_stone(world, transform):
    radius = transform.scale2view(world.settings.stone.radius)
    center = (radius, radius)
    size = (radius * 2, radius * 2)
    stone_color_black = world.settings.stone.color_black
    stone_color_white = world.settings.stone.color_white
    stone_edge_color_black = world.settings.stone.edge_color_black
    stone_edge_color_white = world.settings.stone.edge_color_white
    stone_black_surface = pygame.Surface(size)
    stone_white_surface = pygame.Surface(size)

    # TODO: document the fact we are using (0, 0, 0) as color key
    stone_black_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    stone_white_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    pygame.draw.circle(stone_black_surface, stone_color_black, center, radius, 0)
    pygame.draw.circle(stone_white_surface, stone_color_white, center, radius, 0)

    edge_width = transform.scale2view(world.settings.stone.edge_width)

    pygame.draw.circle(stone_black_surface, stone_edge_color_black, center, radius, edge_width)
    pygame.draw.circle(stone_white_surface, stone_edge_color_white, center, radius, edge_width)
    return stone_black_surface, stone_white_surface

def render_agent(world, transform):
    radius = transform.scale2view(world.settings.agent.radius)
    center = (radius, radius)
    size = (radius * 2, radius * 2)
    color = world.settings.agent.color
    agent_down_surface = pygame.Surface(size)
    agent_up_surface = pygame.Surface(size)
    agent_down_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)
    agent_up_surface.set_colorkey((0, 0, 0), pygame.RLEACCEL)

    edge_width = transform.scale2view(world.settings.agent.edge_width)
    pygame.draw.circle(agent_down_surface, color, center, radius, edge_width)
    pygame.draw.circle(agent_up_surface, color, center, radius, 0)
    return agent_down_surface, agent_up_surface

class Renderer:
    def __init__(self, world, transform):
        self._world = world
        world_size = world.settings.size
        self._transform = transform
        self._view_size = self._transform.scale2view2d(world_size)
        # NB: has to set mode before instantiate Renderer
        self._surface = _initialize_pygame(self._view_size)
        self._base = render_base(self._world, self._transform)
        self._stone_black, self._stone_white = render_stone(self._world, self._transform)
        self._agent_down, self._agent_up = render_agent(self._world, self._transform)

    def _blit_all(self):
        self._surface.blit(self._base, (0, 0))

        stone_radius = self._world.settings.stone.radius
        # reversed is needed to honor z-order of stones
        for stone in reversed(self._world.stones):
            center_x, center_y = stone.center
            target = self._transform.world2view2d((center_x - stone_radius, center_y - stone_radius))
            if stone.is_black:
                self._surface.blit(self._stone_black, target)
            else:
                self._surface.blit(self._stone_white, target)

        agent_radius = self._world.settings.agent.radius
        for agent in self._world.agents:
            agent_x, agent_y = agent.center
            target = self._transform.world2view2d((agent_x - agent_radius, agent_y - agent_radius))
            if agent.current_action.touch:
                self._surface.blit(self._agent_down, target)
            else:
                self._surface.blit(self._agent_up, target)

    def render(self):
        self._blit_all()
        # generate visual feedback
        a3d = pygame.surfarray.array3d(self._surface)
        return a3d

    def capture_screen(filepath):
        image = pygame.Surface(self._view_size)
        image.blit(self.surface, (0, 0), ((0, 0), self._view_size))
        pygame.image.save(image, filepath)
