expected = {
  '[': ']',
  '(': ')',
  '<': '>',
  '{': '}',
}

scores = {
  ')': 1,
  ']': 2,
  '}': 3,
  '>': 4,
}

out = []

for line in open('input.txt'):
  chars = []
  corrupted = False
  for c in line.strip():
    if c in expected.keys():
      chars += [c]
    else:
      last = chars.pop()
      if c != expected[last]:
        corrupted = True
        break
  if not corrupted:
    score = 0
    while chars:
      score = 5 * score + scores[expected[chars.pop()]]
    out += [score]

print sorted(out)[(len(out) - 1)/2]
