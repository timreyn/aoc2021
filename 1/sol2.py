last = 9999
out = 0

vals = [int(x.strip()) for x in open('input.txt')]
for i in range(len(vals)):
  if i > 2 and vals[i] > vals[i-3]:
    out += 1
print out
