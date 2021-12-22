import sys
fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

instructions = []

for line in open(fname):
  cmd = line.split(' ')[0]
  coords = line.strip().split(' ')[1].split(',')
  should_use = True
  c = []
  for coord in coords:
    vals = coord[2:].split('.')
    vals = [int(vals[0]), int(vals[2])]
    if max(vals) < -50 or min(vals) > 50:
      should_use = False
    c += [vals]
  if should_use:
    instructions += [(cmd, c)]

total = 0

for x in range(-50, 51):
  for y in range(-50, 51):
    for z in range(-50, 51):
      val = 0
      for instruction in instructions:
        cmd = instruction[0]
        xs = instruction[1][0]
        ys = instruction[1][1]
        zs = instruction[1][2]
        if x >= xs[0] and x <= xs[1] and y >= ys[0] and y <= ys[1] and z >= zs[0] and z <= zs[1]:
          val = 1 if (cmd == 'on') else 0
      total += val
      if (val == 1):
        print x, y, z

print total
