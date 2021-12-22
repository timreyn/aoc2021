import collections
import sys

fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

positions = []
for line in open(fname):
  positions += [int(line.strip().split(' ')[-1])]

possible_turns = collections.defaultdict(int)

for i in range(1, 4):
  for j in range(1, 4):
    for k in range(1, 4):
      possible_turns[i + j + k] += 1

current_player = 0
scores = [0, 0]
universes = {(positions[0], positions[1], scores[0], scores[1], current_player): 1}

wins = [0, 0]

while universes:
  print '%d states; %s wins' % (len(universes), str(wins))
  new_universes = collections.defaultdict(int)
  for key in universes:
    current_player = key[4]
    copies = universes[key]
    for turn in possible_turns:
      times = possible_turns[turn]
      positions = [key[0], key[1]]
      scores = [key[2], key[3]]
      positions[current_player] += turn
      while positions[current_player] > 10:
        positions[current_player] -= 10
      scores[current_player] += positions[current_player]
      if scores[current_player] >= 21:
        wins[current_player] += copies * times
      else:
        new_universes[(positions[0], positions[1], scores[0], scores[1], 1 - current_player)] += copies * times
  universes = new_universes

print wins
print max(wins)
