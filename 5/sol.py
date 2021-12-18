import collections

out = collections.defaultdict(int)

for line in open('input.txt'):
  l = line.strip().split(' ')
  first = [int(x) for x in l[0].split(',')]
  second = [int(y) for y in l[2].split(',')]

  if first[0] == second[0]:
    y = min(first[1], second[1])
    while y <= max(first[1], second[1]):
      out[(first[0], y)] += 1
      y += 1
  elif first[1] == second[1]:
    y = min(first[0], second[0])
    while y <= max(first[0], second[0]):
      out[(y, first[1])] += 1
      y += 1

total = 0

for pt in out:
  if out[pt] > 1:
    total += 1

print total
