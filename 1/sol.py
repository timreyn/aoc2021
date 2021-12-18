last = 9999
out = 0

for line in open('input.txt'):
  val = int(line.strip())
  if val > last:
    out += 1
  last = val

print out
