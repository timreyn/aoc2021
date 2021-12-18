import sys

fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

bits = []

for row in open(fname):
  for c in row.strip():
    for bit in format(int(c, 16), '04b'):
      bits += [int(bit)]

def get(bits, n):
  out = 0
  added = 0
  while added < n and len(bits):
    out = 2 * out + bits.pop(0)
    added += 1
  if added < n and not bits:
    return None
  return out

LITERAL = 0
OPERATOR = 1

total = 0

def consume_packet(bits):
  global total
  version = get(bits, 3)
  total += version
  typeId = get(bits, 3)
  if len(bits) <= 1:
    return None
  if typeId == 4:
    # LITERAL packet.
    value = 0
    while True:
      nextBits = get(bits, 5)
      value = value * 16 + nextBits % 16
      if nextBits < 16:
        break
    return value
  # OPERATOR packet.
  lengthType = get(bits, 1)
  if lengthType == 1:
    # Number of subpackets.
    lengthInPackets = get(bits, 11)
    subpackets = []
    for i in range(lengthInPackets):
      subpackets += [consume_packet(bits)]
  # Number of bits in subpackets.
  else:
    newbits = []
    numBits = get(bits, 15)
    for i in range(numBits):
      newbits = newbits + [bits.pop(0)]
    subpackets = []
    while newbits:
      subpackets += [consume_packet(newbits)]
  if typeId == 0:
    return sum(subpackets)
  if typeId == 1:
    prod = 1
    for x in subpackets:
      prod *= x
    return prod
  if typeId == 2:
    return min(subpackets)
  if typeId == 3:
    return max(subpackets)
  if typeId == 5:
    return 1 if subpackets[0] > subpackets[1] else 0
  if typeId == 6:
    return 1 if subpackets[0] < subpackets[1] else 0
  if typeId == 7:
    return 1 if subpackets[0] == subpackets[1] else 0

print consume_packet(bits)
