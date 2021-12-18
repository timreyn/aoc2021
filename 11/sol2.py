# Note -- my solution is off-by-one, both on the actual input and the test inputs (actual answer is 251; my code outputs 250).  I'm not sure what the issue is...

grid = {}

i = 0
for row in open('input.txt'):
  grid[i] = {}
  j = 0
  for col in row.strip():
    grid[i][j] = int(col)
    j += 1
  i += 1

for row in grid:
  print ''.join([str(grid[row][x]) for x in grid[row]])
print ''

def inc(grid, i, j):
  if i < 0 or i >= 10 or j < 0 or j >= 10:
    return
  grid[i][j] += 1

def get(grid, i, j):
  if i < 0 or i >= 10 or j < 0 or j >= 10:
    return 0
  return grid[i][j]

total = 0

for step in range(100000):
  flashed = set()
  to_flash = []
  for i in range(10):
    for j in range(10):
      inc(grid, i, j)
      if grid[i][j] > 9:
        to_flash += [(i, j)]
  while to_flash:
    cell = to_flash.pop()
    flashed.add(cell)
    i = cell[0]
    j = cell[1]
    for pair in [(i+1,j), (i-1,j), (i,j+1), (i,j-1), (i+1,j+1),(i+1,j-1),(i-1,j+1),(i-1,j-1)]:
      x = pair[0]
      y = pair[1]
      inc(grid, x, y)
      if get(grid, x, y) > 9 and (x, y) not in flashed and (x, y) not in to_flash:
        to_flash += [(x, y)]
  for pair in flashed:
    grid[pair[0]][pair[1]] = 0
  print len(flashed)
  total += len(flashed)

  if len(flashed) == 100:
    print step
    break

print total
