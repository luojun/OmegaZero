World - composition
    Background
    Board
    List of Stones with z-order
    List of Agents without z-order?

World - constraints - configs
    World
        Shape: rectangular
        Size: given
        Background: background.size == world.size
    Board:
        Shape: rectangular
        Size: world-Board: board.size == world.size * board_size_ratio
        Grid:
            Rectangular grid: (1) even spacing; (2) parallel to board edges
            Grid line positioning: (1) number of lines; (2) inset
    Stone
        Shape: round
        Size: size of cell on the board * stone_size_ratio
    Agent
        Shape: round
        Size: size of stone * agent_size_ratio

World - behavior (tick)
    - per tick
        1. generate observations
            - render ...
        2. generate actions
        3. apply actions

Oz world, renderer, GUI agent
    - synchronized calls into renderer
        - (why does "renderering" take so much time? in contrast to the real world.
           why humans do not need rendering?)
    - asynch observation queue to each agent
        - when dequeue and empty, agent throws exception
        - when enqueue and full, environment throws exception
    - asynch action queue from each agent
        - when dequeue and empty, world does nothing for agent (no change but touching continues)
        - when enqueue and full, agent throws exception

Oz world, GUI and the real world
    - world ticking drives renderring, rather than the other way around
    - GUI agent is just another asynchronous participant
        - when there is a GUI agent the tick rate matches a pre-defined normal rate
    - time constraints on how an Oz world interfaces with the real world
        - computing has to be fast enough for GUI interaction (the normal rate)
        - computing could go arbitrarily super real time
