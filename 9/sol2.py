heights = [[int(x) for x in line.strip()] for line in open('input.txt')]

def get(heights, i, j):
  if i >= len(heights) or i < 0 or j >= len(heights[i]) or j < 0:
    return None
  return heights[i][j]

def neighbors(heights, i, j):
  out = []
  if i > 0:
    out += [(i-1, j)]
  if i < len(heights) - 1:
    out += [(i+1, j)]
  if j > 0:
    out += [(i, j-1)]
  if j < len(heights[i]) - 1:
    out += [(i, j+1)]
  return out

sizes = []

for i in range(len(heights)):
  for j in range(len(heights)):
    adj = [get(heights, x[0], x[1]) for x in neighbors(heights, i, j)]
    alt = get(heights,i,j)
    if alt < min(adj):
      # This is a low point.  Explore it to find all neighbors in basin.
      queue = [(i, j)]
      explored = set()
      explored.add((i, j))
      min_i = i
      max_i = i
      min_j = j
      max_j = j
      while queue:
        point = queue.pop()
        pval = get(heights, point[0], point[1])
        for neighbor in neighbors(heights, point[0], point[1]):
          nval = get(heights, neighbor[0], neighbor[1])
          if neighbor not in explored and nval < 9 and nval > pval:
            explored.add(neighbor)
            queue += [neighbor]
            min_i = min(neighbor[0], min_i)
            min_j = min(neighbor[1], min_j)
            max_i = max(neighbor[0], max_i)
            max_j = max(neighbor[1], max_j)
      sizes += [(len(explored), explored, min_i, max_i, min_j, max_j, i, j)]

out = sorted(sizes, reverse=True, key=lambda x: x[0])

for n in range(3):
  print out[n]
  
  min_i = out[n][2]
  max_i = out[n][3]
  min_j = out[n][4]
  max_j = out[n][5]
  center_i = out[n][6]
  center_j = out[n][7]
  
  i = min_i - 1
  while i <= max_i + 1:
    to_print = str(i) + ': '
    j = min_j - 1
    while j <= max_j + 1:
      if (i, j) in out[n][1]:
        to_print += '(' + str(get(heights, i, j)) + ')'
      else:
        to_print += ' ' + str(get(heights, i, j)) + ' '
      j += 1
    i += 1
    print to_print

print out[0][0] * out[1][0] * out[2][0]
