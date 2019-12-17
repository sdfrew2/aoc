from itertools import permutations
import collections
import re

FORMATS = {1: "IIO", 2: "IIO", 3: "O", 4: "I", 5: "II", 6: "II", 7: "IIO", 8: "IIO", 9: "I" , 99: ""}

class Channel:
    def __init__(me):
        me.q = collections.deque()
    def feed(me, x):
        me.q.append(x)
    def read(me):
        if len(me.q) == 0:
            return None
        return me.q.popleft()
W = 36

class IntCode:
    def __init__(me, program):
        me.program = program[:]
        me.reset()

    def hasHalted(me):
        return me.state == 1
            
    def reset(me):
        me.mem = me.program[:] + [0]*500000
        me.pos = 0
        me.state = 0
        me.input = lambda: 1/0
        me.output = lambda: 1/0
        me.dp = 0

    def decodeInstruction(me, p):
        op = me.mem[p]
        baseOp = op % 100
        fmt = FORMATS[baseOp]
        modes = op // 100
        params = []
        for (i, paramStyle) in enumerate(fmt):
            mode = modes % 10
            modes = modes // 10
            params.append((me.mem[p+1+i], paramStyle, mode))
        return (baseOp, params)

    def resolveParam(me, x, style, mode):
        if style == "I":
            if mode == 0:
                return me.mem[x]
            elif mode == 1:
                return x
            elif mode == 2:
                return me.mem[x+me.dp]
        else:
            if mode == 0:
                return x
            elif mode == 2:
                return x + me.dp

    def step(me):
        if me.state == 1:
            return False
        op, params = me.decodeInstruction(me.pos)
        #print("[" + str(me.pos) + "]" , op, params)
        paramValues = []
        for (p, style, mode) in params:
            pval = me.resolveParam(p, style, mode)
            paramValues.append(pval)
        me.pos += 1 + len(params)
        me.executeInstruction(op, paramValues)
        if me.pos < 0:
            return False
        return True

    def run(me):
        while me.step():
            pass
        
    def executeInstruction(me, op, p):
        if op == 1:
            me.mem[p[2]] = p[0] + p[1]
        elif op == 2:
            me.mem[p[2]] = p[0] * p[1]
        elif op == 3:
            val = me.input()
            if val == None:
                me.pos -= 2
            else:
                me.mem[p[0]] = val
        elif op == 4:
            me.output(p[0])
        elif op == 5:
            if p[0] != 0:
                me.pos = p[1]
        elif op == 6:
            if p[0] == 0:
                me.pos = p[1]
        elif op == 7:
            me.mem[p[2]] = 0
            if p[0] < p[1]:
                me.mem[p[2]] = 1
        elif op == 8:
            v = 0
            if p[0] == p[1]:
                v = 1
            me.mem[p[2]] = v
        elif op == 9:
            me.dp += p[0]
        elif op == 99:
            me.state = 1
        
        

def parseProgram(fn):
    with open(fn, "r") as fh:
        for line in fh:
            return [int(t) for t in line.strip().split(",")]

def makeArrayAssigner(array):
    def result(x):
        array[0] = x
    return result

def neighborhood(p):
    (x, y) = p
    return [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]

class CamSystem:
    def __init__(me, program):
        me.machine = IntCode(program)
        me.machine.output = me.handleOutput
        me.y = 0
        me.x = 0
        me.picture = collections.defaultdict(lambda: '.')

    def handleOutput(me, c):
        print(chr(c), sep="", end="")
        if c == 10:
            me.y += 1
            me.x = 0
        else:
            me.picture[(me.x,me.y)] = chr(c)
            me.x += 1


    def findIntersections(me):
        result = []
        while not me.machine.hasHalted():
            me.machine.step()
        for (p, c) in list(me.picture.items()):
            if c == '#':
                found = all(me.picture[n] == '#' for n in neighborhood(p))
                if found:
                    result.append(p)
        return result

    def findWalk(me):
        while not me.machine.hasHalted():
            me.machine.step()
        p = [(p, c) for (p, c) in me.picture.items() if c in "<>^v"][0][0]
        d = (1, 0)
        yield "R"
        while True:
            pn = (p[0] + d[0], p[1] + d[1])
            c = me.picture[pn]
            if c == '#':
                p = pn
                yield "F"
            else:
                dl = (d[1], -d[0])
                dr = (-d[1], d[0])
                foundDir = False
                for (d2, l) in ((dl, "L"), (dr, "R")):
                    if me.picture[(p[0] + d2[0], p[1] + d2[1])] == '#':
                        d = d2
                        yield l
                        foundDir = True
                        break
                if not foundDir:
                    return
                

        


def main17():
    program = parseProgram("input.txt")
    cams = CamSystem(program)
    print(sum(x*y for (x, y) in cams.findIntersections()))

def encodeWalk(walk):
    forward = None
    result = []
    parts = re.split("(F+)", walk)
    for part in parts:
        if part == "":
            continue
        if part[0] == "F":
            result.append(str(len(part)))
        else:
            for c in part:
                result.append(c)
    return ",".join(result)
        
def substringStats(s):
    result = {}
    for i in range(len(s)):
        for j in range(i+1, len(s)):
            ss = s[i:j]
            if ss in result:
                continue
            result[ss] = s.count(ss)
    return result

def substringPositions(base, sub):
    start = 0
    maxpos = len(base) - len(sub)
    result = []
    while True:
        pos = base.find(sub, start)
        if pos == -1:
            return result
        result.append(pos)
        start = pos+1

            

   

def main17b():
    program = parseProgram("input.txt")
    cams = CamSystem(program)
    walk = "".join(list(cams.findWalk()))
    print(walk.replace("F", ""))
    edit(encodeWalk(walk))
    #print(substringStats(walk.replace("F", ""))))
    return
    solver = Solver(walk)
    for res in solver.solve(0, [], "", 0):
        print(res)
    return
    stats = substringStats(walk)
    candidates = []
    candidatePositions = collections.defaultdict(lambda: [])
    candidatesByPos = {}
    for (s, count) in stats.items():
        e = encodeWalk(s)
        if len(e) <= 20:
            candidates.append(s)
    candidates.sort(key=lambda s: -len(encodeWalk(s)))
    for c in candidates:
        for p in substringPositions(walk, c):
            if not p in candidatesByPos:
                candidatesByPos[p] = []
            candidatesByPos[p].append(c)

# s
# pos
# macroTable
# macros: ascending list of integers
# totalCost: ...

class Solver:
    def __init__(me, walk):
        me.walk = walk
        me.candidates = []
        stats = substringStats(walk)
        for (s, count) in stats.items():
            e = encodeWalk(s)
            if len(e) <= 20:
                me.candidates.append(s)
        me.candidates.sort(key=lambda s: -stats[s] * (1+len(encodeWalk(s)) - len(s)))
        me.validMacros = set()
        me.candidatesByPosition = collections.defaultdict(lambda: [])
        me.encoded = {}
        me.cost = {}
        for (i, c) in enumerate(me.candidates):
            enc = encodeWalk(c)
            if len(enc) > 12:
                me.validMacros.add(i)
            me.cost[i] = len(enc)
            me.encoded[i] = enc
            ps = substringPositions(me.walk, c)
            for p in ps:
                me.candidatesByPosition[p].append(i)
        me.exclusions = collections.defaultdict(lambda: set())
        for (i, cs) in me.candidatesByPosition.items():
            for j in range(len(cs)):
                for k in range(j+1, len(cs)):
                    me.exclusions[j].add(k)
                    me.exclusions[k].add(j)
        print("initialized")

    def solve(me, pos, macros, main, cost):
        minMacro = 0
        if cost > 20:
            return
        if pos == len(me.walk):
            yield((main, [encodeWalk(me.candidates[i]) for i in macros]))
            return
        lastMacro = -1
        if len(macros) > 0:
            lastMacro = macros[-1]
        if len(macros) < 3 and lastMacro < len(me.candidates) - 1:
            for c in me.candidatesByPosition[pos]:
                if pos == 0:
                    print("*")
                if c in me.validMacros:
                    if c > lastMacro and not any((c in me.exclusions[l]) for l in macros):
                        for res in me.solve(pos + len(me.candidates[c]), macros + [c], main + "," + "ABC"[len(macros)], cost + 2):
                            yield res
        for c in me.candidatesByPosition[pos]:
            if pos == 0:
                print("*")
            for (mi, m) in enumerate(macros):
                if m == c:
                    for res in me.solve(pos + len(me.candidates[m]), macros, main + "," + "ABC"[mi], cost + 2):
                        yield res
            for j in range(pos+1, len(me.walk)):
                delta = me.walk[pos:j]
                enc = encodeWalk(delta)
                for res in me.solve(j, macros, main + "," + enc, cost + 1 + len(enc)):
                    yield res


def edit(base):
    var = 0
    history = [base]
    vars = []
    while True:
        for v in vars:
            print(v)
        print("-"*22)
        print(":" , history[-1])
        cmd = input().strip()
        if cmd == "":
            continue
        if cmd  == "exit":
            return
        elif cmd == "pop":
            history.pop()
            vars.pop()
        else:
            if len(cmd) > 20:
                print("WARNING")
            varname = "ABCD"[len(history)-1]
            vars.append(varname + "=" + cmd)
            history.append(history[-1].replace(cmd, varname))

                
            
            





main17b()
