import collections

vals = [[int(x) for x in row.strip()] for row in open('input.txt')]

total_risks = collections.defaultdict(lambda: 99999999)
total_risks[(0, 0)] = 0

# Initial risk values (only moving down and right):
for i in range(len(vals)):
  for j in range(len(vals[i])):
    if i == 0 and j == 0:
      continue
    total_risks[(i, j)] = min(total_risks[(i-1, j)], total_risks[(i, j-1)]) + vals[i][j]

# Now keep iterating until the map stops changing.
while True:
  changes = 0
  for i in range(len(vals)):
    for j in range(len(vals[i])):
      if i == 0 and j == 0:
        continue
      new_min = min(total_risks[(i-1,j)],
                    total_risks[(i+1,j)],
                    total_risks[(i,j-1)],
                    total_risks[(i,j+1)]) + vals[i][j]
      if new_min < total_risks[(i, j)]:
        changes += 1
        total_risks[(i, j)] = new_min
  print changes
  if changes == 0:
    break

for i in range(len(vals)):
  out = ''
  for j in range(len(vals[i])):
    out += '%03d ' % total_risks[(i, j)]
  print out
