import sys

fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

dots = []

for row in open(fname):
  if not row.strip():
    continue
  if 'fold' in row:
    print len(dots)
    directions = row.split(' ')[2]
    d = 0 if directions[0] == 'x' else 1
    val = int(directions[2:])
    new_dots = []
    for dot in dots:
      new_dot = dot
      if new_dot[d] > val:
        new_dot[d] = (2 * val - new_dot[d])
      if new_dot not in new_dots:
        new_dots += [new_dot]
    dots = new_dots
  else:
    dots += [[int(x) for x in row.strip().split(',')]]

print len(dots)

max_x = max([x[0] for x in dots])
max_y = max([x[1] for y in dots])

for y in range(max_y + 2):
  out = ''
  for x in range(max_x + 2):
    if [x, y] in dots:
      out += '#'
    else:
      out += '.'
  print out
