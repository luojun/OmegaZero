import pygame

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
