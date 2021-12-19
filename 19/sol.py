import collections
import sys

fname = sys.argv[1] if len(sys.argv) > 1 else 'input.txt'

scanners = []
current_scanner = None

for line in open(fname):
  if '---' in line:
    if current_scanner:
      scanners += [current_scanner]
    current_scanner = []
  elif line.strip():
    current_scanner += [[int(x) for x in line.strip().split(',')]]

scanners += [current_scanner]

# For scanners we've figured out the position and orientation, map their points to the absolute grid.
mapping_fns = {0: []}

unmatched = set(range(len(scanners)))
unmatched.remove(0)

def overlap(s, t):
  vals = {}
  for si, p1 in enumerate(s):
    for sj, p2 in enumerate(s):
      if si <= sj:
        continue
      key = str(sorted([abs(a - b) for a, b in zip(p1, p2)]))
      vals[key] = (si, sj)

  potential_matches = collections.defaultdict(list)
  matches = {}
  for ti, p1 in enumerate(t):
    for tj, p2 in enumerate(t):
      if ti <= tj:
        continue
      key = str(sorted([abs(a - b) for a, b in zip(p1, p2)]))
      if key in vals:
        si = vals[key][0]
        sj = vals[key][1]
        for pair in ((si, ti), (si, tj), (sj, ti), (sj, tj)):
          ss = pair[0]
          tt = pair[1]
          if tt in potential_matches[ss]:
            matches[ss] = tt
          else:
            potential_matches[ss] += [tt]
  return matches

def orient(s, t, matches):
  # Returns a function that maps s[i] to t[matches[i]].
  sa = min(matches.keys())
  sb = max(matches.keys())
  ta = matches[sa]
  tb = matches[sb]
  sdiff = [aa - bb for aa, bb in zip(s[sa], s[sb])]
  tdiff = [aa - bb for aa, bb in zip(t[ta], t[tb])]

  # S coordinate -> T coordinate
  mapping = {}
  for i in range(len(sdiff)):
    for j in range(len(tdiff)):
      if sdiff[i] == tdiff[j]:
        mapping[i] = (j, 1)
      elif sdiff[i] == tdiff[j] * -1:
        mapping[i] = (j, -1)
  return [mapping, s[sa], t[ta]]

def applyorientation(pt, inputs):
  for val in inputs:
    mapping = val[0]
    s = val[1]
    t = val[2]
    out = [0] * len(pt)
    for i in range(len(pt)):
      j, sign = mapping[i]
      out[j] = sign * (pt[i] - s[i] + sign * t[j])
    pt = out
  return pt

while unmatched:
  for s in unmatched:
    deleted = False
    for t in mapping_fns:
      matches = overlap(scanners[s], scanners[t])
      if len(matches) >= 12:
        #print '%d and %d overlap!' % (s, t)
        orientation = orient(scanners[s], scanners[t], matches)
        mapping_fns[s] = [orientation] + mapping_fns[t]
        #for num, pt in enumerate(scanners[s]):
          #if num in matches:
            #print pt, applyorientation(pt, mapping_fns[s])
        unmatched.remove(s)
        deleted = True
        break
    if deleted:
      break

all_beacons = set()

for s in mapping_fns:
  for pt in scanners[s]:
    beacon = applyorientation(pt, mapping_fns[s])
    all_beacons.add(str(beacon))

print len(all_beacons)

max_distance = 0

for s in mapping_fns:
  for t in mapping_fns:
    pt_s = applyorientation([0,0,0], mapping_fns[s])
    pt_t = applyorientation([0,0,0], mapping_fns[t])
    manhattan_distance = sum([x-y for x, y in zip(pt_s, pt_t)])
    max_distance = max(manhattan_distance, max_distance)
print max_distance
