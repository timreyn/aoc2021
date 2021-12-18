heights = [[int(x) for x in line.strip()] for line in open('input.txt')]

def get(heights, i, j):
  if i >= len(heights) or i < 0 or j >= len(heights[i]) or j < 0:
    return None
  return heights[i][j]

out = 0

for i in range(len(heights)):
  for j in range(len(heights)):
    adj = [x for x in [get(heights, i+1,j), get(heights, i-1,j), get(heights,i,j+1),get(heights,i,j-1)] if x is not None]
    alt = get(heights,i,j)
    if alt < min(adj):
      out += alt + 1

print out

