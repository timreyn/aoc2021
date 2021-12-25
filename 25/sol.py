import sys
fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

state = {}

EAST = '>'
SOUTH = 'v'
EMPTY = '.'

max_i = 0
max_j = 0

for i, row in enumerate(open(fname)):
  max_i = i + 1
  max_j = len(row) - 1
  for j, val in enumerate(row.strip()):
    if val != EMPTY:
      state[(i, j)] = val

def p(state):
  for i in range(max_i):
    out = ''
    for j in range(max_j):
      if (i, j) in state:
        out += state[(i, j)]
      else:
        out += EMPTY
    print out

p(state)
print ""

changes = 1
turns = 0

while changes:
  turns += 1
  new_changes = []
  for cucumber, d in state.iteritems():
    i = cucumber[0]
    j = cucumber[1]
    if d != EAST:
      continue
    if (i, (j + 1) % max_j) not in state:
      new_changes += [(i, j)]
  for change in new_changes:
    i = change[0]
    j = change[1]
    state[(i, (j + 1) % max_j)] = state[(i, j)]
    del state[(i, j)]
  changes = len(new_changes)

  new_changes = []
  for cucumber, d in state.iteritems():
    i = cucumber[0]
    j = cucumber[1]
    if d != SOUTH:
      continue
    if ((i + 1) % max_i, j) not in state:
      new_changes += [(i, j)]
  for change in new_changes:
    i = change[0]
    j = change[1]
    state[((i + 1) % max_i, j)] = state[(i, j)]
    del state[(i, j)]
  changes += len(new_changes)
  print changes

print turns
