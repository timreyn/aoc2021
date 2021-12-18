tx = [34, 67]
ty = [-215, -186]

def hits_area(vx, vy):
  pos = [0, 0]
  max_y = 0
  while True:
    pos[0] += vx
    pos[1] += vy
    max_y = max(max_y, pos[1])
    if vx > 0:
      vx -= 1
    elif vx < 0:
      vx += 1
    vy -= 1
    if pos[0] >= tx[0] and pos[0] <= tx[1] and pos[1] >= ty[0] and pos[1] <= ty[1]:
      return True, max_y
    if pos[0] > tx[1] or pos[1] < ty[0]:
      return False, max_y

best = 0
hits_area_count = 0
for vx in range(tx[1] + 10):
  for vy in range(ty[0] - 10, abs(ty[0]) + 10):
    hits, max_y = hits_area(vx, vy)
    if hits:
      hits_area_count += 1
    best = max(best, max_y)
print best
print hits_area_count
