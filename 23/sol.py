EMPTY = '.'

destinations = {
  'A': 3,
  'B': 5,
  'C': 7,
  'D': 9,
}

costs = {
  'A': 1,
  'B': 10,
  'C': 100,
  'D': 1000,
}

status = {}
for i, line in enumerate(open('input.txt')):
  for j, value in enumerate(line):
    if value != '#' and value != ' ' and value != '\n':
      status[(i, j)] = value

def path(si, sj, ti, tj):
  i = si
  j = sj
  if j != tj:
    while i > 1:
      i -= 1
      yield i, j
    while j > tj:
      j -= 1
      yield i, j
    while j < tj:
      j += 1
      yield i, j
  while i > ti:
    i -= 1
    yield i, j
  while i < ti:
    i += 1
    yield i, j

def valid_moves(status):
  out = []
  for t, val_t in status.iteritems():
    if val_t != EMPTY:
      continue
    ti = t[0]
    tj = t[1]
    if ti == 1 and tj in (3, 5, 7, 9):
      # Rule 1
      continue
    for s, val_s in status.iteritems():
      si = s[0]
      sj = s[1]
      if val_s == EMPTY:
        continue
      if ti > 1:
        # Rule 2
        if tj != destinations[val_s]:
          continue
        if ti == 2 and status[(3, tj)] != val_s:
          continue
      if ti == 1 and si == 1:
        # Rule 3
        continue
      # Don't move into the hallway if you're already in the right spot and not blocking someone in.
      if si > 1 and destinations[val_s] == sj and ti == 1:
        if si == 3:
          continue
        elif si == 2 and status[(3, sj)] != val_s:
          continue
      # Don't move within a room.
      if sj == tj:
        continue
      # Don't walk over someone else.
      cost = 0
      valid = True
      for i, j in path(si, sj, ti, tj):
        if status[(i, j)] != EMPTY:
          valid = False
          break
        cost += costs[val_s]
      if valid:
        out += [(si, sj, ti, tj, cost)]
  return out

def is_solved(state):
  for s, val in state.iteritems():
    si = s[0]
    sj = s[1]
    if si == 1 and val != EMPTY:
      return False
    if si > 1 and (val == EMPTY or destinations[val] != sj):
      return False
  return True

def pr(status):
  ret = ''
  for i in range(5):
    out = ''
    for j in range(13):
      if (i, j) not in status:
        out += '#'
      else:
        out += status[(i, j)]
    ret += out + '\n'
  return ret

def min_remaining_cost(status):
  out = 0
  for s, val in status.iteritems():
    si = s[0]
    sj = s[1]
    if val == EMPTY:
      continue
    ti = 2
    tj = destinations[val]
    if sj == tj and si == 3:
      ti = 3
    out += costs[val] * len(list(path(si, sj, ti, tj)))
  return out

done = False
final_cost = 0
queue = {pr(status): (status, 0, 0)}
visited = set()
while not done:
  queue_sorted = sorted(queue.items(), key=lambda i: i[1][2])
  print len(queue)
  val = queue_sorted[0]
  key = val[0]
  del queue[key]
  if key in visited:
    continue
  visited.add(key)
  status = val[1][0]
  cost = val[1][1]
  min_cost = val[1][2]
  print key
  print cost, min_cost
  if is_solved(status):
    done = True
    final_cost = cost
    break
  for move in valid_moves(status):
    si = move[0]
    sj = move[1]
    ti = move[2]
    tj = move[3]
    new_cost = move[4]
    new_status = status.copy()
    new_status[(ti, tj)] = status[(si, sj)]
    new_status[(si, sj)] = EMPTY
    min_cost = cost + new_cost + min_remaining_cost(new_status)
    new_key = pr(new_status)
    if new_key in queue:
      old_cost = queue[new_key][1]
      if cost + new_cost < old_cost:
        queue[new_key] = (new_status, cost + new_cost, min_cost)
    else:
      queue[new_key] = (new_status, cost + new_cost, min_cost)

print final_cost
