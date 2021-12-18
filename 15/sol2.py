import collections

import sys
fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

invals = [[int(x) for x in row.strip()] for row in open(fname)]

vals = collections.defaultdict(lambda: 0)
total_risks = collections.defaultdict(lambda: 99999999)
total_risks[(0, 0)] = 0

def mod(n):
  while n > 9:
    n -= 9
  return n


for i in range(len(invals)):
  for j in range(len(invals[i])):
    for xi in range(5):
      for xj in range(5):
        vals[(i + len(invals) * xi, j + len(invals) * xj)] = mod(xi + xj + invals[i][j])

dim = len(invals) * 5

# Initial risk values (only moving down and right):
for i in range(dim):
  for j in range(dim):
    if i == 0 and j == 0:
      continue
    total_risks[(i, j)] = min(total_risks[(i-1, j)], total_risks[(i, j-1)]) + vals[(i, j)]

# Now keep iterating until the map stops changing.
while True:
  changes = 0
  for i in range(dim):
    for j in range(dim):
      if i == 0 and j == 0:
        continue
      new_min = min(total_risks[(i-1,j)],
                    total_risks[(i+1,j)],
                    total_risks[(i,j-1)],
                    total_risks[(i,j+1)]) + vals[(i, j)]
      if new_min < total_risks[(i, j)]:
        changes += 1
        total_risks[(i, j)] = new_min
  print changes
  if changes == 0:
    break

print total_risks[(dim-1, dim-1)]
