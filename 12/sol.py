import sys

if len(sys.argv) > 0:
  infile = sys.argv[1]
else:
  infile = 'input.txt'

caves = []

for row in open(infile):
  caves += [row.strip().split('-')]

queue = [['start']]
out = 0

while queue:
  path = queue.pop()
  for link in caves:
    if path[-1] not in link:
      continue
    other = link[1] if (link[0] == path[-1]) else link[0]
    if other == 'end':
      out += 1
    elif other.isupper() or other not in path:
      queue += [path + [other]]

print out
