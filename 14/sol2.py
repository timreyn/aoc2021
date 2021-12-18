import collections

poly = collections.defaultdict(lambda: 0)
rules = {}

for line in open('input.txt'):
  if ' -> ' in line:
    rules[line[0:2]] = line[6]
  elif line.strip():
    poly_str = line.strip()
    for x in range(len(poly_str)):
      poly[poly_str[x:x+2]] += 1

for i in range(40):
  print 'step ' + str(i)
  print 'len: ' + str(len(poly))
  new_poly = collections.defaultdict(lambda: 0)
  for key in poly:
    if key in rules:
      new_poly[key[0] + rules[key]] += poly[key]
      new_poly[rules[key] + key[1]] += poly[key]
    else:
      new_poly[key] += poly[key]
  poly = new_poly

count = collections.defaultdict(lambda: 0)
for c in poly:
  count[c[0]] += poly[c]

most = 0
least = 999999999999

for c in count:
  most = max(most, count[c])
  least = min(least, count[c])

print len(poly)
print most
print least
print most - least
