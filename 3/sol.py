import collections

freqs = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))

for line in open('input.txt'):
  for i in range(len(line.strip())):
    freqs[i][int(line[i])] += 1

gamma = 0
epsilon = 0

for i in freqs.keys():
  fr = freqs[i]
  if fr[1] > fr[0]:
    gamma += 2 ** (len(freqs) - i - 1)
  else:
    epsilon += 2 ** (len(freqs) - i - 1)

print gamma
print epsilon
