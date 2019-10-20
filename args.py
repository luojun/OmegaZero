import argparse
parser = argparse.ArgumentParser()
parser.add_argument('-a', '--agents', nargs='?', default=2, type=int)
parser.add_argument('-l', '--lines', nargs='?', default=4, type=int)
parser.add_argument('-s', '--stones', nargs='?', default=5, type=int)
args = parser.parse_args()
print(args)

print(args.agents)
