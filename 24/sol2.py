instructions = []

INP = 'inp'
ADD = 'add'
MUL = 'mul'
DIV = 'div'
MOD = 'mod'
EQL = 'eql'

class ConstNode(object):
  def __init__(self, val):
    self.val = val
    self.possible = [self.val]

  def str(self):
    return str(self.val)

class InputNode(object):
  def __init__(self, idx):
    self.idx = idx
    self.possible = [1,2,3,4,5,6,7,8,9]

  def str(self):
    return 'in[%d]' % self.idx

class AddNode(object):
  @staticmethod
  def Create(node1, node2):
    add = AddNode(node1, node2)
    possible = add.possible
    if len(possible) == 1:
      return ConstNode(list(possible)[0])
    if isinstance(node1, ConstNode) and node1.val == 0:
      return node2
    if isinstance(node2, ConstNode) and node2.val == 0:
      return node1
    if isinstance(node1, AddNode) and isinstance(node2, ConstNode):
      if isinstance(node1.node1, ConstNode):
        return AddNode.Create(node1.node2, ConstNode(node2.val + node1.node1.val))
      if isinstance(node1.node2, ConstNode):
        return AddNode.Create(node1.node1, ConstNode(node2.val + node1.node2.val))
    if isinstance(node2, AddNode) and isinstance(node1, ConstNode):
      if isinstance(node2.node1, ConstNode):
        return AddNode.Create(node2.node2, ConstNode(node1.val + node2.node1.val))
      if isinstance(node2.node2, ConstNode):
        return AddNode.Create(node2.node1, ConstNode(node1.val + node2.node2.val))
        
    return add

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.possible = set()
    for x1 in self.node1.possible:
      for x2 in self.node2.possible:
        self.possible.add(x1 + x2)

  def str(self):
    return '(%s + %s)' % (self.node1.str(), self.node2.str())

class MulNode(object):
  @staticmethod
  def Create(node1, node2):
    mul = MulNode(node1, node2)
    possible = mul.possible
    if len(possible) == 1:
      return ConstNode(list(possible)[0])
    if isinstance(node1, ConstNode) and node1.val == 1:
      return node2
    if isinstance(node2, ConstNode) and node2.val == 1:
      return node1
    return mul

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.possible = set()
    for x1 in self.node1.possible:
      for x2 in self.node2.possible:
        self.possible.add(x1 * x2)

  def str(self):
    return '[%s * %s]' % (self.node1.str(), self.node2.str())

class DivNode(object):
  @staticmethod
  def Create(node1, node2):
    div = DivNode(node1, node2)
    possible = div.possible
    if len(possible) == 1:
      return ConstNode(list(possible)[0])
    if isinstance(node2, ConstNode) and node2.val == 1:
      return node1
    if isinstance(node1, AddNode):
      can_split_1 = True
      for poss1 in node1.node1.possible:
        for poss2 in node2.possible:
          if poss1 % poss2 != 0:
            can_split_1 = False
      can_split_2 = True
      for poss1 in node1.node2.possible:
        for poss2 in node2.possible:
          if poss1 % poss2 != 0:
            can_split_2 = False
      if can_split_1 or can_split_2:
        return AddNode.Create(DivNode.Create(node1.node1, node2), DivNode.Create(node1.node2, node2))
    if isinstance(node1, MulNode) and isinstance(node2, ConstNode):
      if isinstance(node1.node1, ConstNode) and node1.node1.val % node2.val == 0:
        return MulNode.Create(node1.node2, ConstNode(node1.node1.val / node2.val))
      if isinstance(node1.node2, ConstNode) and node1.node2.val % node2.val == 0:
        return MulNode.Create(node1.node1, ConstNode(node1.node2.val / node2.val))
    return div

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.possible = set()
    for x1 in self.node1.possible:
      for x2 in self.node2.possible:
        self.possible.add(x1 / x2)

  def str(self):
    return '<%s / %s>' % (self.node1.str(), self.node2.str())

class ModNode(object):
  @staticmethod
  def Create(node1, node2):
    mod = ModNode(node1, node2)
    possible = mod.possible
    if len(possible) == 1:
      return ConstNode(list(possible)[0])
    all_mods_too_big = True
    for poss1 in node1.possible:
      for poss2 in node2.possible:
        if poss2 <= poss1:
          all_mods_too_big = False
    if all_mods_too_big:
      return node1
    if isinstance(node1, AddNode):
      return AddNode.Create(ModNode.Create(node1.node1, node2), ModNode.Create(node1.node2, node2))
    return mod

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.possible = set()
    for x1 in self.node1.possible:
      for x2 in self.node2.possible:
        self.possible.add(x1 % x2)

  def str(self):
    return '{%s %% %s}' % (self.node1.str(), self.node2.str())

class NeqlNode(object):
  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.possible = set()
    for x1 in self.node1.possible:
      for x2 in self.node2.possible:
        self.possible.add(1 if x1 != x2 else 0)

  def str(self):
    return '(%s != %s)' % (self.node1.str(), self.node2.str())

class EqlNode(object):
  @staticmethod
  def Create(node1, node2):
    eq = EqlNode(node1, node2)
    possible = eq.possible
    if len(possible) == 1:
      return ConstNode(list(possible)[0])

    if isinstance(node1, EqlNode) and isinstance(node2, ConstNode):
      if node2.val == 0:
        return NeqlNode(node1.node1, node1.node2)
      if node2.val == 1:
        return node1
      return ConstNode(0)
    if isinstance(node2, EqlNode) and isinstance(node1, ConstNode):
      if node1.val == 0:
        return NeqlNode(node2.node1, node2.node2)
      if node1.val == 1:
        return node2
      return ConstNode(0)
    return eq

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.possible = set()
    for x1 in self.node1.possible:
      for x2 in self.node2.possible:
        self.possible.add(1 if x1 == x2 else 0)

  def str(self):
    return '(%s == %s)' % (self.node1.str(), self.node2.str())

vals = {'w': ConstNode(0), 'x': ConstNode(0), 'y': ConstNode(0), 'z': ConstNode(0)}

def get_args(instruction, vals):
  out = []
  for val in instruction[1:]:
    if val in vals:
      out += [vals[val]]
    else:
      out += [ConstNode(int(val))]
  return out

inputs_used = 0

import sys
lines_to_use = int(sys.argv[1]) if len(sys.argv) > 1 else -1

for line in open('input.txt'):
  if lines_to_use == 0:
    break
  if lines_to_use == 1:
    print line.strip()
  lines_to_use -= 1
  inst = line.strip().split(' ')
  args = get_args(inst, vals)
  if inst[0] == INP:
    vals[inst[1]] = InputNode(inputs_used)
    inputs_used += 1
  elif inst[0] == ADD:
    vals[inst[1]] = AddNode.Create(args[0], args[1])
  elif inst[0] == MUL:
    vals[inst[1]] = MulNode.Create(args[0], args[1])
  elif inst[0] == DIV:
    vals[inst[1]] = DivNode.Create(args[0], args[1])
  elif inst[0] == MOD:
    vals[inst[1]] = ModNode.Create(args[0], args[1])
  elif inst[0] == EQL:
    vals[inst[1]] = EqlNode.Create(args[0], args[1])

for k, v in vals.iteritems():
  print k, v.str()
