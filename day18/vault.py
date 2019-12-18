import collections
import heapq
ROBOT = "%&/$@"

def neighbors(p):
    (x,y) = p
    return [(x-1, y), (x+1, y), (x,y-1), (x,y+1)]

class Vault:
    def __init__(me, lines):
        me.map = collections.defaultdict(lambda: '#')
        me.locations = {}
        for (y, line) in enumerate(lines):
            for (x, ch) in enumerate(line):
                me.map[(x,y)] = ch
                if ch != '.' and ch != '#':
                    me.locations[ch] = (x,y)
        me.locDistances = me.calcAllDistances()

    def solve(me):
        state = (0, '@', "")
        keyCount = len([k for k in me.locations.keys() if k.islower()])
        q = [state]
        seen = set()
        while len(q) > 0:
            (cost, loc, keys) = heapq.heappop(q)
            if (loc, keys) in seen:
                continue
            seen.add((loc, keys))
            if len(keys) == keyCount:
                return cost
            for (nextNode, d) in me.locDistances[loc].items():
                if nextNode.islower():
                    if nextNode in keys:
                        nextkeys = keys
                    else:
                        nextkeys = "".join(sorted(list(keys + nextNode)))
                    heapq.heappush(q, (cost+d, nextNode, nextkeys))
                elif nextNode == '@':
                    heapq.heappush(q, (cost+d, nextNode, keys))
                elif nextNode.isupper() and nextNode in keys.upper():
                    heapq.heappush(q, (cost+d, nextNode, keys))

    def solve2(me):
        state = (0, ('$', '%', '&', '/'), "")
        keyCount = len([k for k in me.locations.keys() if k.islower()])
        quadrants = {} 
        qpos = "$%&/"
        MX = 40
        MY = 40
        for (loc, (x, y)) in me.locations.items():
            print(loc, x, y)
            if x > MX and y > MY:
                quadrant = "/"
            elif x > MX and y < MY:
                quadrant = "%"
            elif x < MX and y > MY:
                quadrant = "&"
            elif x < MX and y < MY:
                quadrant = "$"
            quadrants[loc] = quadrant
        print(quadrants)
        q = [state]
        seen = set()
        while len(q) > 0:
            #print(q)
            (cost, locs, keys) = heapq.heappop(q)
            #print(locs)
            if (locs, keys) in seen:
                continue
            seen.add((locs, keys))
            if len(keys) == keyCount:
                return cost
            for loc in locs:
                for (nextNode, d) in me.locDistances[loc].items():
                    locs2 = list(locs)
                    locs2[qpos.index(quadrants[nextNode])] = nextNode
                    locs2 = tuple(locs2)
                    if nextNode.islower():
                        if nextNode in keys:
                            nextkeys = keys
                        else:
                            nextkeys = "".join(sorted(list(keys + nextNode)))
                        heapq.heappush(q, (cost+d, locs2, nextkeys))
                    elif nextNode in ROBOT:
                        heapq.heappush(q, (cost+d, locs2, keys))
                    elif nextNode.isupper() and nextNode in keys.upper():
                        heapq.heappush(q, (cost+d, locs2, keys))


                



    def calcDistances(me, pos):
        q = collections.deque()
        depths = {}
        result = {}
        depths[pos] = 0
        q.append(pos)
        while len(q) > 0:
            nextPos = q.popleft()
            for neighbor in neighbors(nextPos):
                tile = me.map[neighbor]
                if tile == '#':
                    continue
                if not neighbor in depths:
                    depths[neighbor] = depths[nextPos] + 1
                    if tile == '.':
                        q.append(neighbor)
                    else:
                        result[neighbor] = depths[neighbor]
        return result
                        
    def calcAllDistances(me):
        result = collections.defaultdict(lambda: dict())
        for (ch, loc) in me.locations.items():
            distances = me.calcDistances(loc)
            for (loc2, d) in distances.items():
                result[me.map[loc]][me.map[loc2]] = d
        return result

        


def main18():
    with open("input.txt", "r") as fh:
        lines = [line.strip() for line in fh]
    v = Vault(lines)
    print(v.calcAllDistances()["@"])
    print(v.solve())

def main18b():
    with open("input2.txt", "r") as fh:
        lines = [line.strip() for line in fh]
    v = Vault(lines)
    print(v.solve2())


main18b()
