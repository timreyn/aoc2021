positions = []
for line in open('input.txt'):
  positions += [int(line.strip().split(' ')[-1])]

next_roll = 1
current_player = 0
total_rolls = 0
scores = [0, 0]

while max(scores) < 1000:
  for i in range(3):
    positions[current_player] += next_roll
    next_roll += 1
    total_rolls += 1
  while positions[current_player] > 10:
    positions[current_player] -= 10
  scores[current_player] += positions[current_player]
  current_player = 1 - current_player

print total_rolls * min(scores)
