EMPTY = '.'
import sys
fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

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
lines = list(open(fname))
lines = lines[0:3] + ['###D#C#B#A#','###D#B#A#C#'] + lines[3:]
for i, line in enumerate(lines):
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
        valid = True
        for tii in range(ti + 1, 6):
          if status[(tii, tj)] != val_s:
            valid = False
        if not valid:
          continue
      if ti == 1 and si == 1:
        # Rule 3
        continue
      # Don't move into the hallway if you're already in the right spot and not blocking someone in.
      if si > 1 and destinations[val_s] == sj and ti == 1:
        valid = False
        for sii in range(si + 1, 6):
          if status[(sii, sj)] != val_s:
            valid = True
        if not valid:
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

# Printable version of the status.  This also became my dict key.
def pr(status):
  ret = ''
  for i in range(7):
    out = ''
    for j in range(13):
      if (i, j) not in status:
        out += '#'
      else:
        out += status[(i, j)]
    ret += out + '\n'
  return ret

import collections

def min_remaining_cost(status):
  out = 0
  cells_filled = collections.defaultdict(list)
  for s, val in status.iteritems():
    si = s[0]
    sj = s[1]
    if val == EMPTY:
      continue
    ti = 2
    tj = destinations[val]
    if sj == tj and si > ti:
      ti = si
    cells_filled[tj] += [ti]
    out += costs[val] * len(list(path(si, sj, ti, tj)))
  for ti, cells in cells_filled.iteritems():
    extra = 14 - sum(cells)
    out += extra * 10 ** ((ti - 3) / 2)
  return out

#############
#A..D...D.BA#
###.#C#.#B###
###.#C#.#A###
###D#B#.#C###
###B#C#D#A###
#############
# This is invalid because the D in (2, 8) is blocking everything in column 9.
# Specifically, there are more than two to the right of it.  With two, it would
# be okay because they could go to the top right.
#
# Additionally, this case is invalid:
#############
#A..D.D.B.BA#
###.#C#.#B###
###.#C#.#A###
###.#B#.#C###
###D#C#D#A###
#############
# because the second D in the top row needs to go to the right of the first B
# in the top row.  They can't cross each others' path once they're both in the
# top row.
def is_valid(status):
  for tj in [4,6,8]:
    count = 0
    ti = 1
    val_t = status[(ti, tj)]
    if val_t == EMPTY:
      continue
    dest = destinations[val_t]
    if dest > tj:
      for s, val_s in status.iteritems():
        si = s[0]
        sj = s[1]
        if val_s == EMPTY:
          continue
        if sj < tj:
          continue
        dest_s = destinations[val_s]
        if dest_s < tj and (si == 1 or sj == dest):
          count += 1
          if si == 1 and sj == 10 and status[(1, 11)] == EMPTY:
            count += 1
        elif dest_s > tj:
          num_in_col = 0
          for sii in [2, 3, 4, 5]:
            if status[(sii, dest_s)] != EMPTY and destinations[status[(sii, dest_s)]] < tj:
              num_in_col += 1
          if num_in_col > 0:
            continue
      if count > 2:
        return False
    else:
      for s, val_s in status.iteritems():
        si = s[0]
        sj = s[1]
        if val_s == EMPTY:
          continue
        dest_s = destinations[val_s]
        if sj > tj:
          continue
        if dest_s > tj and (si == 1 or sj == dest):
          count += 1
          if si == 1 and sj == 2 and status[(1, 1)] == EMPTY:
            count += 1
        elif dest_s < tj:
          num_in_col = 0
          for sii in [2, 3, 4, 5]:
            if status[(sii, dest_s)] != EMPTY and destinations[status[(sii, dest_s)]] > tj:
              num_in_col += 1
          if num_in_col > 0:
            continue
      if count > 2:
        return False

  # This is a specific case of the above logic.  I think it's not needed anymore.
  if status[(1, 8)] == 'D':
    num = 0
    for s, val_s in status.iteritems():
      si = s[0]
      sj = s[1]
      if sj > 8 and val_s != 'D' and val_s != EMPTY:
        num += 1
    if num > 2:
      return False
      
  if status[(1, 4)] == 'A':
    num = 0
    for s, val_s in status.iteritems():
      si = s[0]
      sj = s[1]
      if sj < 4 and val_s != 'A' and val_s != EMPTY:
        num += 1
    if num > 2:
      return False

  for sj in range(1, 12):
    for tj in range(sj + 1, 12):
      val_s = status[(1, sj)]
      val_t = status[(1, tj)]
      if val_s == EMPTY or val_t == EMPTY:
        continue
      if sj > destinations[val_t] and tj < destinations[val_s]:
        return False

  return True

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
    if not is_valid(new_status):
      print '(%d, %d, %d, %d) invalid' % (si, sj, ti, tj)
      continue
    min_cost = cost + new_cost + min_remaining_cost(new_status)
    new_key = pr(new_status)
    print move, min_cost
    if new_key in queue:
      old_cost = queue[new_key][1]
      if cost + new_cost < old_cost:
        #print 'replacing with %d' % (cost + new_cost)
        queue[new_key] = (new_status, cost + new_cost, min_cost)
    else:
      #print 'newly adding with %d' % (cost + new_cost)
      queue[new_key] = (new_status, cost + new_cost, min_cost)

print final_cost
