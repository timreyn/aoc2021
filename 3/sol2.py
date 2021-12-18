import collections

freqs = collections.defaultdict(lambda: collections.defaultdict(lambda: 0))

nums = [line.strip() for line in open('input.txt')]
bits = len(nums[0])

def mcb(nums, i):
  ones = len([x for x in nums if x[i] == '1'])
  zeros = len([x for x in nums if x[i] == '0'])
  if ones >= zeros:
    return '1'
  else:
    return '0'

ogr = nums
cosr = nums

for i in range(bits):
  if len(ogr) > 1:
    mcb_ogr = mcb(ogr, i)
    ogr = [x for x in ogr if x[i] == mcb_ogr]
  if len(cosr) > 1:
    mcb_cosr = mcb(cosr, i)
    cosr = [x for x in cosr if x[i] != mcb_cosr]

print ogr
print cosr
print int(ogr[0], 2)
print int(cosr[0], 2)
print int(ogr[0], 2) * int(cosr[0], 2)
