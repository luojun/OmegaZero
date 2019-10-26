# TODO: understand conventions for __main__.py

import argparse

import oz
import env

PARSER = argparse.ArgumentParser()

# default to five-agent tic-tac-toe
PARSER.add_argument('-l', '--lines', nargs='?', default=4, type=int)
PARSER.add_argument('-s', '--stones', nargs='?', default=10, type=int)
PARSER.add_argument('-a', '--agents', nargs='?', default=5, type=int)
PARSER.add_argument('-hz', '--display_hz', nargs='?', default=30, type=float)

ARGS = PARSER.parse_args()

ENVIRONMENT = env.Environment(1.0, 1.0, ARGS.lines, ARGS.stones, ARGS.agents)

# WITHOUT array3d
# Before optimization --
# Cycles:  1000   Time elasped:  2.808263063430786   Time per cycle:  0.0028082630634307863
# After optimization --
# Cycles:  1000   Time elasped:  2.2032926082611084   Time per cycle:  0.0022032926082611085
#ENVIRONMENT = env.Environment(1.0, 1.0, 19, 360, 5)

# WITHOUT array3d
# Before optimization --
# Cycles:  1000   Time elasped:  1.3584859371185303   Time per cycle:  0.0013584859371185303
# After optimization --
# Cycles:  1000   Time elasped:  1.215559720993042   Time per cycle:  0.001215559720993042
#ENVIRONMENT = env.Environment(1.0, 1.0, 4, 10, 6) # five-agent tic-tac-toe

#ENVIRONMENT = env.Environment()

#import cProfile
#cProfile.run('run_oz(ENVIRONMENT, cycles=100, timing=True)')

#oz.run_oz(e, cycles=1000, timing=True)

# Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif
#oz.run_oz(ENVIRONMENT, cycles=5000, capture_pngs=True)

#oz.run_oz(ENVIRONMENT, cycles=1000, timing=True, display_hz=ARGS.display_hz)

oz.run_oz(ENVIRONMENT, display_hz=ARGS.display_hz)
