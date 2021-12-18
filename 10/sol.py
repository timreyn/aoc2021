expected = {
  '[': ']',
  '(': ')',
  '<': '>',
  '{': '}',
}

scores = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
}

out = 0

for line in open('input.txt'):
  chars = []
  for c in line.strip():
    if c in expected.keys():
      chars += [c]
    else:
      last = chars.pop()
      if c != expected[last]:
        out += scores[c]
        break
print out
