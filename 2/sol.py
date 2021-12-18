x = 0
y = 0

for line in open('input.txt'):
  vals = line.split(' ')
  d = vals[0]
  amt = int(vals[1])
  if d=='forward':
    x += amt
  elif d=='up':
    y -= amt
  elif d=='down':
    y += amt

print x
print y
