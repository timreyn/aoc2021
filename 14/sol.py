import collections

poly = ''
rules = {}

for line in open('input.txt'):
  if ' -> ' in line:
    rules[line[0:2]] = line[6]
  elif line.strip():
    poly = line.strip()

for i in range(10):
  new_poly = ''
  for x in range(len(poly)):
    new_poly += poly[x]
    chars = poly[x:x+2]
    if chars in rules:
      new_poly += rules[chars]
  poly = new_poly

count = collections.defaultdict(lambda: 0)
for c in poly:
  count[c] += 1

most = 0
least = 99999999

for c in count:
  most = max(most, count[c])
  least = min(least, count[c])

print len(poly)
print most
print least
