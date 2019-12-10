import math
import functools

def parseRocks(fn):
    result = []
    with open(fn, "r") as fh:
        for (y, line) in enumerate(fh):
            line = line.strip()
            for (x, ch) in enumerate(line):
                if ch == '#':
                    result.append((x,y))
    return result

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0

def normalizeDirection(d):
    (x, y) = d
    if x == 0:
        return (0, sign(y))
    if y == 0:
        return (sign(x), 0)
    divisor = math.gcd(abs(x), abs(y))
    return (x // divisor, y // divisor)

def pspmap(rocks):
    result = {}
    for a in rocks:
        sp = {}
        result[a] = sp
        for b in rocks:
            if a != b:
                slope = normalizeDirection((b[0] - a[0], b[1]-a[1]))
                if not (slope in sp):
                    sp[slope] = []
                sp[slope].append(b)
    return result

def distanceFrom(p):
    def d(p2):
        return abs(p2[0] -p[0]) + abs(p2[1] - p[1])
    return d        

def neighbormap(psp):
    result = {}
    for a in psp.keys():    
        result[a] = []
        sp = psp[a]
        for s in sp.keys():
            nextNeighbor = min(sp[s], key=distanceFrom(a))
            result[a].append(nextNeighbor)
    return result

def main10():
    rocks = parseRocks("input.txt")
    print(len(rocks))
    psp = pspmap(rocks)
    neighbors = neighbormap(psp)
    neighborcounts = [len(z) for z in neighbors.values()]
    m = max(neighborcounts)
    print(m)

def manhattan(p, q):
    return abs(p[0] - q[0]) + abs(p[1]-q[1])

            
def main10b():
    rocks = parseRocks("input.txt")
    print(len(rocks))
    psp = pspmap(rocks)
    neighbors = neighbormap(psp)
    neighborcounts = [len(z) for z in neighbors.values()]
    m = max(neighborcounts)
    base = [rock for rock in rocks if len(neighbors[rock]) == m][0]
    directions = list(psp[base].keys())
    directions.sort(key=lambda p: -math.atan2(p[0], p[1]))
    sp = psp[base] 
    spcopy = {}
    for (d, line) in sp.items():
        line2 = list(line)
        line2.sort(reverse=True, key=functools.partial(manhattan, base))
        spcopy[d] = line2
    sp = spcopy
    count = 0
    vaporized = []
    while len(vaporized) < 200:
        for d in directions:
            line = sp[d]
            if len(line) > 0:
                vaporized.append(line.pop())
    print(vaporized[199])


main10b()
    
    

