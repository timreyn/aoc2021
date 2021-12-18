out = 0

for line in open('input.txt'):
  line_spl = line.strip().split(' ')
  outputs = line_spl[11:]
  signals = line[0:10]
  for output in outputs:
    if len(output) in (2, 3, 4, 7):
      out += 1

print out
