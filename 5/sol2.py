import collections

out = collections.defaultdict(int)

for line in open('input.txt'):
  l = line.strip().split(' ')
  first = [int(x) for x in l[0].split(',')]
  second = [int(y) for y in l[2].split(',')]

  x = first[0]
  y = first[1]
  while x != second[0] or y != second[1]:
    out[(x, y)] += 1
    if x > second[0]:
      x -= 1
    elif x < second[0]:
      x += 1
    if y > second[1]:
      y -= 1
    elif y < second[1]:
      y += 1
  out[(x, y)] += 1

total = 0

for pt in out:
  if out[pt] > 1:
    total += 1

print total
