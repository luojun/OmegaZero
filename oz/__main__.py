# TODO: understand conventions for __main__.py

import oz
import env
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-l', '--lines', nargs='?', default=4, type=int)
parser.add_argument('-s', '--stones', nargs='?', default=10, type=int)
parser.add_argument('-a', '--agents', nargs='?', default=5, type=int)
parser.add_argument('-hz', '--display_hz', nargs='?', default=30, type=float)
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

#runOzOpt(e, cycles=1000, timing=True)

#runOzOpt(e, cycles=5000, capture_pngs=True) # Use: convert -delay 20 -loop 0 screenshot0*.png demo.gif

#runOzOpt(e, cycles=1000, timing=True, display_hz=args.display_hz)

oz.runOzOpt(e, display_hz=args.display_hz)

