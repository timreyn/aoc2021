import collections
import sys
iterations = int(sys.argv[1])
fname = sys.argv[2] if len(sys.argv) > 2 else 'input.txt'
debug = len(sys.argv) > 3 and sys.argv[3] == 'd'

key = ''

rows_added = 0
lights = collections.defaultdict(lambda: 0)

for row in open(fname):
  row = row.strip()
  if len(row) == 512:
    key = row
  elif row:
    for i, value in enumerate(row):
      if value == '#':
        lights[(rows_added, i)] = 1
    rows_added += 1

def display(lights):
  global debug
  if not debug:
    return
  min_x = min([pt[0] for pt in lights])-1
  min_y = min([pt[1] for pt in lights])-1
  max_x = max([pt[0] for pt in lights])+1
  max_y = max([pt[1] for pt in lights])+1
  for x in range(min_x, max_x + 1):
    out = ''
    for y in range(min_y, max_y + 1):
      if lights[(x, y)] == 1:
        out += '#'
      else:
        out += '.'
    print out
  print ''


def advance(lights, key):
  min_x = min([pt[0] for pt in lights])-1
  min_y = min([pt[1] for pt in lights])-1
  max_x = max([pt[0] for pt in lights])+1
  max_y = max([pt[1] for pt in lights])+1
  old_default = lights.default_factory()
  new_default = 1 if key[old_default * 511] == '#' else 0
  out = collections.defaultdict(lambda: new_default)

  for x in range(min_x, max_x + 1):
    for y in range(min_y, max_y + 1):
      valstr = ''
      for pt in ((x-1, y-1), (x-1, y), (x-1, y+1),
                 (x,   y-1), (x,   y), (x,   y+1),
                 (x+1, y-1), (x+1, y), (x+1, y+1)):
        valstr += str(lights[pt])
      out[(x, y)] = 1 if key[int(valstr, 2)] == '#' else 0
  return out

display(lights)

for i in range(iterations):
  lights = advance(lights, key)
  display(lights)

print sum(lights.values())
