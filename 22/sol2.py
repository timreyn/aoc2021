import sys
fname = 'input.txt' if len(sys.argv) <= 1 else sys.argv[1]
max_val = None if len(sys.argv) <= 2 else int(sys.argv[2])

# Instructions are (cmd, (x_interval, y_interval, z_interval)).  All intervals are half-open.
instructions = []
all_x = set()

for line in open(fname):
  cmd = line.split(' ')[0]
  coords = line.strip().split(' ')[1].split(',')
  should_use = True
  c = []
  for coord in coords:
    vals = coord[2:].split('.')
    vals = [int(vals[0]), int(vals[2]) + 1]
    if max_val and (max(vals) < -1 * max_val or min(vals) > max_val):
      should_use = False
    c += [vals]
  if should_use:
    instructions += [(cmd, c)]
    all_x.add(c[0][0])
    all_x.add(c[0][1])

total = 0
all_x = sorted(list(all_x))
for xi in range(len(all_x) - 1):
  x = all_x[xi]
  nextx = all_x[xi + 1]
  all_y = set()
  instr_x = [instr for instr in instructions if instr[1][0][0] <= x and instr[1][0][1] > x]
  for instr in instr_x:
    all_y.add(instr[1][1][0])
    all_y.add(instr[1][1][1])
  all_y = sorted(list(all_y))
  for yi in range(len(all_y) - 1):
    y = all_y[yi]
    nexty = all_y[yi + 1]
    all_z = set()
    instr_y = [instr for instr in instr_x if instr[1][1][0] <= y and instr[1][1][1] > y]
    for instr in instr_y:
      all_z.add(instr[1][2][0])
      all_z.add(instr[1][2][1])
    all_z = sorted(list(all_z))
    for zi in range(len(all_z) - 1):
      z = all_z[zi]
      nextz = all_z[zi + 1]
      val = 0
      instr_z = [instr for instr in instr_y if instr[1][2][0] <= z and instr[1][2][1] > z]
      for instr in instr_z:
        val = (1 if (instr[0] == 'on') else 0)
      total += val * (nextx - x) * (nexty - y) * (nextz - z)
      #print [x, nextx, y, nexty, z, nextz, val, instr_z]

print total
