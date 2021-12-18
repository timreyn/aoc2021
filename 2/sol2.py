x = 0
y = 0

aim = 0

for line in open('input.txt'):
  vals = line.split(' ')
  d = vals[0]
  amt = int(vals[1])
  if d=='forward':
    x += amt
    y += aim * amt
  elif d=='up':
    aim -= amt
  elif d=='down':
    aim += amt

print x
print y
