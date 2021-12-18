import sys

if len(sys.argv) > 0:
  infile = sys.argv[1]
else:
  infile = 'input.txt'

caves = []

for row in open(infile):
  caves += [row.strip().split('-')]

queue = [(['start'], False)]
out = 0

def max_visits(node, has_revisited):
  if node == 'start':
    return 1
  if node.islower():
    if has_revisited:
      return 1
    else:
      return 2
  return 99999999

while queue:
  vals = queue.pop()
  path = vals[0]
  has_revisited = vals[1]
  for link in caves:
    if path[-1] not in link:
      continue
    other = link[1] if (link[0] == path[-1]) else link[0]
    if other == 'end':
      out += 1
    elif path.count(other) < max_visits(other, has_revisited):
      is_duplicate = other.islower() and other in path
      queue += [(path + [other], has_revisited or is_duplicate)]

print out
