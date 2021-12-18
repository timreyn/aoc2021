import sys
fname = sys.argv[1] if len(sys.argv) > 1 else "input.txt"
isdebug = len(sys.argv) > 2 and sys.argv[2] == 'd'

def p(x):
  global isdebug
  if isdebug:
    print x

LEFT = 0
RIGHT = 1

def letter(d):
  if d == LEFT:
    return 'l'
  if d == RIGHT:
    return 'r'
  return 'n'

class IntNode(object):
  def __init__(self, parent, side, val):
    self.parent = parent
    self.side = side
    self.val = val

  def deepen(self):
    pass

  def maybe_explode(self):
    return False

  def recurse_down_and_add(self, val, direction):
    self.val += val

  def str(self):
    return str(self.val)

  def magnitude(self):
    return self.val

class Node(object):
  def __init__(self, parent, side, vals, depth=0):
    self.children = []
    self.parent = parent
    self.depth = depth
    self.side = side
    side = LEFT
    for val in vals:
      if isinstance(val, int):
        self.children += [IntNode(self, side, val)]
      else:
        self.children += [Node(self, side, val, depth + 1)]
      side += 1

  def deepen(self):
    self.depth += 1
    for child in self.children:
      child.deepen()

  # Returns whether it exploded.
  def maybe_explode(self):
    p('maybe_explode ' + self.str())
    if self.depth < 4:
      for child in self.children:
        if child.maybe_explode():
          return True
      return False
    else:
      self.recurse_up_and_add(self.children[LEFT].val, LEFT)
      self.recurse_up_and_add(self.children[RIGHT].val, RIGHT)
      self.parent.children[self.side] = IntNode(self.parent.parent, self.side, 0)
      return True

  def recurse_up_and_add(self, val, direction):
    p('recursing up ' + letter(direction) + ' at ' + self.str() + ' with ' + str(val))
    if self.parent == None:
      return
    if self.side != direction:
      self.parent.children[1 - self.side].recurse_down_and_add(val, self.side)
    else:
      self.parent.recurse_up_and_add(val, direction)

  def recurse_down_and_add(self, val, direction):
    p('recursing down ' + letter(direction) + ' at ' + self.str() + ' with ' + str(val))
    self.children[direction].recurse_down_and_add(val, direction)

  # Returns whether it splits.
  def maybe_split(self):
    for i in [0, 1]:
      child = self.children[i]
      if isinstance(child, Node) and child.maybe_split():
        return True
      elif isinstance(child, IntNode) and child.val >= 10:
        val = child.val
        self.children[i] = Node(self, i, [val / 2, val - val / 2], self.depth + 1)
        return True
    return False

  def add(self, other):
    new = Node(None, -1, [], 0)
    new.children = [self, other]
    self.deepen()
    self.parent = new
    self.side = LEFT
    other.deepen()
    other.parent = new
    other.side = RIGHT
    return new

  def str(self):
    return letter(self.side) + str(self.depth) + '[' + ','.join([child.str() for child in self.children]) + ']'

  def magnitude(self):
    return 3 * self.children[0].magnitude() + 2 * self.children[1].magnitude()

inputs = []
for line in open(fname):
  inputs += [line.strip()]

max_magnitude = 0

for i in range(len(inputs)):
  for j in range(len(inputs)):
    if i == j:
      continue
    val_i = Node(None, -1, eval(inputs[i]))
    val_j = Node(None, -1, eval(inputs[j]))
    val = val_i.add(val_j)
    did_something = True
    while did_something:
      did_something = val.maybe_explode() or val.maybe_split()

    max_magnitude = max(max_magnitude, val.magnitude())
print max_magnitude
