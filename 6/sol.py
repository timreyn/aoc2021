lf = [0,0,0,0,0,0,0,0,0]

for line in open('input.txt'):
  for val in line.strip().split(','):
    lf[int(val)] += 1

print lf

for day in range(256):
  lf = [lf[1], lf[2], lf[3], lf[4], lf[5], lf[6], lf[7] + lf[0], lf[8], lf[0]]

print lf
print sum(lf)
