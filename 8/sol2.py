import itertools

digits = ['123567', '36', '13457', '13467', '2346', '12467', '124567', '136', '1234567', '123467']

out = 0

for line in open('input.txt'):
  line_spl = line.strip().split(' ')
  outputs = line_spl[11:]
  signals = line_spl[0:10]

  num_valid = 0

  for perm in itertools.permutations('abcdefg'):
    perm = ''.join(perm)
    valid = True
    for char in outputs + signals:
      rendered = ''.join(sorted([str(perm.find(x) + 1) for x in char]))
      if rendered not in digits:
        valid = False
        break
    if valid:
      # Repeat to compute the output
      val = 0
      for char in outputs:
        rendered = ''.join(sorted([str(perm.find(x) + 1) for x in char]))
        val = 10 * val + digits.index(rendered)
      num_valid += 1
      out += val
  if num_valid != 1:
    print 'ERROR: failed to find exactly one solution to ' + line.strip()

print out
