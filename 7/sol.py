positions = []

for line in open('input.txt'):
  for x in line.split(','):
    positions += [int(x)]

best_pos = 0
best_sum = 99999999

for pos in range(max(positions)):
  s = sum(abs(x-pos) for x in positions)
  if s < best_sum:
    best_pos = pos
    best_sum = s

print best_pos
print best_sum
