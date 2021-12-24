# sol.py was my first attempt at solving, but it was way too slow.  This solution built up a tree
# of nodes.

instructions = []

INP = 'inp'
ADD = 'add'
MUL = 'mul'
DIV = 'div'
MOD = 'mod'
EQL = 'eql'

MANY = -1

# a global for rendering if() blocks
indent = 2

'''
Nodes have the following methods:
-A constructor
-Create, a static factory method, which creates the node and simplifies it with its children.
Each of these have a bazillion simplification rules, which are commented.  These were a huge pain to
write.
-str: returns a string representation
-assertEq: propagates the information that these two nodes are equal in this branch.
-assertNeq: propagates the information that these two nodes are not equal in this branch.  e.g.

if(x == y,
  if(x == y, a, b)
  if(x == y, c, d)
)

can be simplified to if(x == y, a, d).  This is also true with deeper trees -- x == y can be
propagated all the way through the "true" branch.

-get_possible: lists all possible values, given the input variable list.  If that would be more than
about 1000, returns MANY instead.
-eq: returns if two nodes are equal.
-possible: class variable, which is initialized to get_possible with no variables.
'''

# A node just representing a constant.
class ConstNode(object):
  def __init__(self, val):
    self.val = val
    self.possible = self.get_possible([])
    self.depth = 0
    self.size = 1

  def str(self):
    return str(self.val)

  def assertEq(self, node1, node2):
    return self

  def assertNeq(self, node1, node2):
    return self

  def eq(self, node):
    return isinstance(node, ConstNode) and node.val == self.val

  def get_possible(self, vals):
    return [self.val]

# A node representing one of the 14 input variables.
class InputNode(object):
  def __init__(self, idx):
    self.idx = idx
    self.possible = self.get_possible([])
    self.depth = 0
    self.size = 1

  def str(self):
    return 'in[%d]' % self.idx

  def assertEq(self, node1, node2):
    return self

  def assertNeq(self, node1, node2):
    return self

  def eq(self, node):
    return isinstance(node, InputNode) and node.idx == self.idx

  def get_possible(self, vals):
    if len(vals) > self.idx:
      return [vals[self.idx]]
    return [1,2,3,4,5,6,7,8,9]

class AddNode(object):
  @staticmethod
  def Create(node1, node2):
    add = AddNode(node1, node2)
    possible = add.possible
    # If there's only one possibility, make a constant node.
    if possible != MANY and len(possible) == 1:
      return ConstNode(list(possible)[0])
    # a + 0 -> a
    if isinstance(node1, ConstNode) and node1.val == 0:
      return node2
    if isinstance(node2, ConstNode) and node2.val == 0:
      return node1
    # (a + 2) + 3 -> a + 5
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
    # if(a = b, c, d) + if(a = b, e, f) -> if(a = b, c+e, d+f)
    if isinstance(node1, EqlNode) and isinstance(node2, EqlNode) and node1.node1.eq(node2.node1) and node1.node2.eq(node2.node2):
      return EqlNode.Create(node1.node1, node1.node2, AddNode.Create(node1.true, node2.true), AddNode.Create(node1.false, node2.false))
    # if(a = b, c, d) + e -> if(a = b, c + e, d + e)
    if isinstance(node1, EqlNode):
      return EqlNode.Create(node1.node1, node1.node2, AddNode.Create(node1.true, node2), AddNode.Create(node1.false, node2))
    if isinstance(node2, EqlNode):
      return EqlNode.Create(node2.node1, node2.node2, AddNode.Create(node2.true, node1), AddNode.Create(node2.false, node1))
    return add

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.depth = 1 + max(node1.depth, node2.depth)
    self.size = 1 + node1.size + node2.size
    self.possible = self.get_possible([])

  def get_possible(self, vals):
    if vals:
      p1 = self.node1.get_possible(vals)
      p2 = self.node2.get_possible(vals)
    else:
      p1 = self.node1.possible
      p2 = self.node2.possible
    if p1 == MANY or p2 == MANY or len(p1) * len(p2) > 100:
      return MANY
    else:
      out = set()
      for x1 in p1:
        for x2 in p2:
          out.add(x1 + x2)
      return out

  def str(self):
    return '(%s + %s)' % (self.node1.str(), self.node2.str())

  def assertEq(self, node1, node2):
    return AddNode.Create(self.node1.assertEq(node1, node2), self.node2.assertEq(node1, node2))

  def assertNeq(self, node1, node2):
    return AddNode.Create(self.node1.assertNeq(node1, node2), self.node2.assertNeq(node1, node2))

  def eq(self, node):
    return isinstance(node, AddNode) and node.node1.eq(self.node1) and node.node2.eq(self.node2)

class MulNode(object):
  @staticmethod
  def Create(node1, node2):
    mul = MulNode(node1, node2)
    possible = mul.possible
    if possible != MANY and len(possible) == 1:
      return ConstNode(list(possible)[0])
    # a * 1 -> a
    if isinstance(node1, ConstNode) and node1.val == 1:
      return node2
    if isinstance(node2, ConstNode) and node2.val == 1:
      return node1
    # if(a = b, c, d) * e -> if(a = b, c * e, d * e)
    if isinstance(node1, EqlNode):
      return EqlNode.Create(node1.node1, node1.node2, MulNode.Create(node1.true, node2), MulNode.Create(node1.false, node2))
    if isinstance(node2, EqlNode):
      return EqlNode.Create(node2.node1, node2.node2, MulNode.Create(node2.true, node1), MulNode.Create(node2.false, node1))
    return mul

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.depth = 1 + max(node1.depth, node2.depth)
    self.size = 1 + node1.size + node2.size
    self.possible = self.get_possible([])

  def get_possible(self, vals):
    if vals:
      p1 = self.node1.get_possible(vals)
      p2 = self.node2.get_possible(vals)
    else:
      p1 = self.node1.possible
      p2 = self.node2.possible
    if p1 == MANY or p2 == MANY or len(p1) * len(p2) > 100:
      return MANY
    else:
      out = set()
      for x1 in p1:
        for x2 in p2:
          out.add(x1 * x2)
      return out

  def str(self):
    return '[%s * %s]' % (self.node1.str(), self.node2.str())

  def assertEq(self, node1, node2):
    return MulNode.Create(self.node1.assertEq(node1, node2), self.node2.assertEq(node1, node2))

  def assertNeq(self, node1, node2):
    return MulNode.Create(self.node1.assertNeq(node1, node2), self.node2.assertNeq(node1, node2))

  def eq(self, node):
    return isinstance(node, MulNode) and node.node1.eq(self.node1) and node.node2.eq(self.node2)


class DivNode(object):
  @staticmethod
  def Create(node1, node2):
    div = DivNode(node1, node2)
    possible = div.possible
    if possible != MANY and len(possible) == 1:
      return ConstNode(list(possible)[0])
    # a / 1 -> a
    if isinstance(node2, ConstNode) and node2.val == 1:
      return node1
    # In some cases, (a + b) / c -> a / c + b / c.
    # This is only the case if a or b is divisible by c.
    if isinstance(node1, AddNode):
      can_split_1 = True
      if node1.node1.possible != MANY:
        for poss1 in node1.node1.possible:
          for poss2 in node2.possible:
            if poss1 % poss2 != 0:
              can_split_1 = False
      can_split_2 = True
      if node1.node2.possible != MANY:
        for poss1 in node1.node2.possible:
          for poss2 in node2.possible:
            if poss1 % poss2 != 0:
              can_split_2 = False
      if can_split_1 or can_split_2:
        return AddNode.Create(DivNode.Create(node1.node1, node2), DivNode.Create(node1.node2, node2))
    # kA / c -> (k/c) * A if k/c is an integer.
    if isinstance(node1, MulNode) and isinstance(node2, ConstNode):
      if isinstance(node1.node1, ConstNode) and node1.node1.val % node2.val == 0:
        return MulNode.Create(node1.node2, ConstNode(node1.node1.val / node2.val))
      if isinstance(node1.node2, ConstNode) and node1.node2.val % node2.val == 0:
        return MulNode.Create(node1.node1, ConstNode(node1.node2.val / node2.val))
    # if(a = b, c, d) / e -> if(a = b, c / e, d / e)
    if isinstance(node1, EqlNode):
      return EqlNode.Create(node1.node1, node1.node2, DivNode.Create(node1.true, node2), DivNode.Create(node1.false, node2))
    if isinstance(node2, EqlNode):
      return EqlNode.Create(node2.node1, node2.node2, DivNode.Create(node2.true, node1), DivNode.Create(node2.false, node1))
    return div

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.depth = 1 + max(node1.depth, node2.depth)
    self.size = 1 + node1.size + node2.size
    self.possible = self.get_possible([])


  def get_possible(self, vals):
    if vals:
      p1 = self.node1.get_possible(vals)
      p2 = self.node2.get_possible(vals)
    else:
      p1 = self.node1.possible
      p2 = self.node2.possible
    if p1 == MANY or p2 == MANY or len(p1) * len(p2) > 100:
      return MANY
    else:
      out = set()
      for x1 in p1:
        for x2 in p2:
          out.add(x1 / x2)
      return out

  def str(self):
    return '<%s / %s>' % (self.node1.str(), self.node2.str())

  def assertEq(self, node1, node2):
    return DivNode.Create(self.node1.assertEq(node1, node2), self.node2.assertEq(node1, node2))

  def assertNeq(self, node1, node2):
    return DivNode.Create(self.node1.assertNeq(node1, node2), self.node2.assertNeq(node1, node2))

  def eq(self, node):
    return isinstance(node, DivNode) and node.node1.eq(self.node1) and node.node2.eq(self.node2)


class ModNode(object):
  @staticmethod
  def Create(node1, node2):
    mod = ModNode(node1, node2)
    possible = mod.possible
    if possible != MANY and len(possible) == 1:
      return ConstNode(list(possible)[0])
    if node1.possible != MANY and node2.possible != MANY:
      all_mods_too_big = True
      all_divisible = True
      for poss1 in node1.possible:
        for poss2 in node2.possible:
          if poss2 <= poss1:
            all_mods_too_big = False
          if poss1 % poss2 != 0:
            all_divisible = False
      if all_mods_too_big:
        return node1
    # (a + b) % c -> (a % c) + (b % c)
    if isinstance(node1, AddNode):
      return AddNode.Create(ModNode.Create(node1.node1, node2), ModNode.Create(node1.node2, node2))
    # if(a = b, c, d) % e -> if(a = b, c % e, d % e)
    if isinstance(node1, EqlNode):
      return EqlNode.Create(node1.node1, node1.node2, ModNode.Create(node1.true, node2), ModNode.Create(node1.false, node2))
    if isinstance(node2, EqlNode):
      return EqlNode.Create(node2.node1, node2.node2, ModNode.Create(node2.true, node1), ModNode.Create(node2.false, node1))
    # (4 * a) % 2 -> 0
    if isinstance(node1, MulNode) and isinstance(node2, ConstNode):
      if isinstance(node1.node1, ConstNode) and node1.node1.val % node2.val == 0:
        return ConstNode(0)
      if isinstance(node1.node2, ConstNode) and node1.node2.val % node2.val == 0:
        return ConstNode(0)
    return mod

  def __init__(self, node1, node2):
    self.node1 = node1
    self.node2 = node2
    self.depth = 1 + max(node1.depth, node2.depth)
    self.size = 1 + node1.size + node2.size
    self.possible = self.get_possible([])

  def get_possible(self, vals):
    if vals:
      p1 = self.node1.get_possible(vals)
      p2 = self.node2.get_possible(vals)
    else:
      p1 = self.node1.possible
      p2 = self.node2.possible
    if p1 == MANY and p2 == MANY:
      return MANY
    elif p1 == MANY:
      return set(range(0, max(p2) + 1))
    elif p2 == MANY:
      return set(range(0, max(p1) + 1))
    else:
      out = set()
      for x1 in p1:
        for x2 in p2:
          out.add(x1 % x2)
      return out

  def str(self):
    return '{%s %% %s}' % (self.node1.str(), self.node2.str())

  def assertEq(self, node1, node2):
    return ModNode.Create(self.node1.assertEq(node1, node2), self.node2.assertEq(node1, node2))

  def assertNeq(self, node1, node2):
    return ModNode.Create(self.node1.assertNeq(node1, node2), self.node2.assertNeq(node1, node2))

  def eq(self, node):
    return isinstance(node, ModNode) and node.node1.eq(self.node1) and node.node2.eq(self.node2)


# This is represented a "if(a = b, c, d)".  The instructions always have c = 1, d = 0.
class EqlNode(object):
  @staticmethod
  def Create(node1, node2, true, false):
    true = true.assertEq(node1, node2)
    false = false.assertNeq(node1, node2)
    eq = EqlNode(node1, node2, true, false)
    possible = eq.possible
    if possible != MANY and len(possible) == 1:
      return ConstNode(list(possible)[0])
    if true.eq(false):
      return true

    # Possibilities are possibilities of `true` and `false`, depending on whether
    # a == b and a != b are possible.
    possible_truths = set()
    if node1.possible == MANY or node2.possible == MANY:
      possible_truths = [True, False]
    else:
      for x1 in node1.possible:
        for x2 in node2.possible:
          possible_truths.add(x1 == x2)
          if len(possible_truths) == 2:
            break
        if len(possible_truths) == 2:
          break
    if len(possible_truths) == 1:
      if True in possible_truths:
        return true
      if False in possible_truths:
        return false

    # if(if(a=b, c, d) = c, e, f) -> if(a=b, e, f)
    if isinstance(node1, EqlNode) and isinstance(node2, ConstNode):
      if isinstance(node1.true, ConstNode) and node1.true.val == node2.val:
        return node1
      if isinstance(node1.false, ConstNode) and node1.false.val == node2.val:
        return EqlNode.Create(node1.node1, node1.node2, node1.false, node1.true)
    # if(a=b, if(a=b, c, d), e) -> if(a=b, c, e)
    # (this is a specific case of assertEq, and probably can be deleted)
    if isinstance(true, EqlNode) and true.node1 == node1 and true.node2 == node2:
      return EqlNode.Create(node1, node2, true.true, false)
    if isinstance(false, EqlNode) and false.node1 == node1 and false.node2 == node2:
      return EqlNode.Create(node1, node2, true, false.false)

    return eq

  def __init__(self, node1, node2, true, false):
    self.node1 = node1
    self.node2 = node2
    self.true = true
    self.false = false
    self.depth = 1 + max(node1.depth, node2.depth, true.depth, false.depth)
    self.size = 1 + node1.size + node2.size + true.size + false.size
    self.possible = self.get_possible([])

  def get_possible(self, vals):
    if vals:
      p1 = self.node1.get_possible(vals)
      p2 = self.node2.get_possible(vals)
      pt = self.true.get_possible(vals)
      pf = self.false.get_possible(vals)
    else:
      p1 = self.node1.possible
      p2 = self.node2.possible
      pt = self.true.possible
      pf = self.false.possible

    out = set()
    possible_truths = set()
    if p1 == MANY or p2 == MANY:
      possible_truths = [True, False]
    else:
      for x1 in p1:
        for x2 in p2:
          possible_truths.add(x1 == x2)
          if len(possible_truths) == 2:
            break
        if len(possible_truths) == 2:
          break
    if True in possible_truths and pt == MANY:
      return MANY
    elif False in possible_truths and pf == MANY:
      return MANY
    else:
      if True in possible_truths:
        for poss in pt:
          out.add(poss)
      if False in possible_truths:
        for poss in pf:
          out.add(poss)
    return out

  def assertEq(self, node1, node2):
    if node1.eq(self.node1) and node2.eq(self.node2):
      return self.true
    return EqlNode.Create(self.node1.assertEq(node1, node2), self.node2.assertEq(node1, node2), self.true.assertEq(node1, node2), self.false.assertEq(node1, node2))

  def assertNeq(self, node1, node2):
    if node1.eq(self.node1) and node2.eq(self.node2):
      return self.false
    return EqlNode.Create(self.node1.assertNeq(node1, node2), self.node2.assertNeq(node1, node2), self.true.assertNeq(node1, node2), self.false.assertNeq(node1, node2))


  def str(self):
    global indent
    indent_str = ' '*indent
    indent += 2
    out = 'if(%s == %s,\n%s%s,\n%s%s,\n%s)' % (self.node1.str(), self.node2.str(), indent_str, self.true.str(), indent_str, self.false.str(),indent_str[:-2])
    indent -= 2
    return out

  def eq(self, node):
    return isinstance(node, EqlNode) and node.node1.eq(self.node1) and node.node2.eq(self.node2) and node.true.eq(self.true) and node.false.eq(self.false)

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

for i, line in enumerate(open('input.txt')):
  print i, line.strip()
  if lines_to_use == 0:
    break
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
    vals[inst[1]] = EqlNode.Create(args[0], args[1], ConstNode(1), ConstNode(0))


current_guess = []
node = vals['z']
print node.str()

'''
Okay so at this point I tried running through everything (try_all()), this time cutting off any
branches that couldn't be 0.  The problem is that too many of them are MANY, so it couldn't
prune well enough.  But it got further than sol.py.

But I printed out the final tree and noticed that exactly one branch could be zero, the first one:

if((in[2] + 7) == in[3],
  if((in[1] + 8) == in[4],
    if((in[6] + -5) == in[7],
      if((in[9] + 2) == in[10],
        if((in[8] + 1) == in[11],
          if((in[5] + -4) == in[12],
            if((in[0] + 5) == in[13],
              0,
              ...
All the other ones had too many positive numbers!  So it's just a matter of picking out numbers so
that all 7 of those evaluate to true, which I did by hand.  Neat!
'''

def try_all(node):
  while True:
    possible = node.get_possible(current_guess)
    print ''.join([str(x) for x in current_guess])
    if possible == MANY:
      print 'MANY'
    else:
      print len(possible), 0 in possible
    if possible == MANY or 0 in possible:
      if len(current_guess) == 14:
        print current_guess
        break
      current_guess += [9]
      continue
    current_guess[-1] -= 1
    while current_guess[-1] == 0:
      current_guess.pop()
      current_guess[-1] -= 1
 
#try_all(node)
