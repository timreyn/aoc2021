# This was my first pass.  Running through 10^14 numbers is, uh, not a good idea.
# It proved useful for validating sol2.py, though, since it's plenty fast for running through a few
# hundred examples and comparing the outputs.

import sys

instructions = []

INP = 'inp'
ADD = 'add'
MUL = 'mul'
DIV = 'div'
MOD = 'mod'
EQL = 'eql'

num = int(sys.argv[1]) if len(sys.argv) > 1 else 0

for line in open('input.txt'):
  instruction = line.strip().split(' ')
  instructions += [line.strip().split(' ')]

def get_args(instruction, vals):
  out = []
  for val in instruction[1:]:
    if val in vals:
      out += [vals[val]]
    else:
      out += [int(val)]
  return out

def run(model, num):
  inputs = 0
  vals = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
  last = None
  for inst in instructions[:num + 1]:
    args = get_args(inst, vals)
    if inst[0] == INP:
      res = int(model[inputs])
      inputs += 1
    elif inst[0] == ADD:
      res = args[0] + args[1]
    elif inst[0] == MUL:
      res = args[0] * args[1]
    elif inst[0] == DIV:
      res = args[0] / args[1]
    elif inst[0] == MOD:
      res = args[0] % args[1]
    elif inst[0] == EQL:
      res = 1 if args[0] == args[1] else 0
    vals[inst[1]] = res
    last = inst[1]
  return vals[last]

for i in range(len(instructions)):
  print i, ' '.join(instructions[i])
  print i, run('99999999999999', i)
