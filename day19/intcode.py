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
        #print(chr(c), sep="", end="")
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

    def run(me):
        while not me.machine.hasHalted():
            me.machine.step()

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
                


def findWalkFromLines(lines):
    picture = collections.defaultdict(lambda: ".")
    for (y, line) in enumerate(lines):
        for (x, c) in enumerate(line):
            picture[(x, y)] = c
    p = [(p, c) for (p, c) in picture.items() if c in "<>^v"][0][0]
    d = (1, 0)
    yield "R"
    while True:
        pn = (p[0] + d[0], p[1] + d[1])
        c = picture[pn]
        if c == '#':
            p = pn
            yield "F"
        else:
            dl = (d[1], -d[0])
            dr = (-d[1], d[0])
            foundDir = False
            for (d2, l) in ((dl, "L"), (dr, "R")):
                if picture[(p[0] + d2[0], p[1] + d2[1])] == '#':
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
    print(len(encodeWalk(walk)))
    solver = Solver(walk)
    for res in solver.solve(0, [], "", 0):
        break
    inputArray = [res[0], *res[1], "n"]
    inputData = chr(10).join(inputArray) + chr(10)
    program[0] = 2
    cams = CamSystem(program)
    inputIter = (ord(c) for c in inputData)
    cams.machine.input = inputIter.__next__
    def outputter(x):
        if x < 128:
            print(chr(x), sep="", end="")
        else:
            print()
            print(x)
    cams.machine.output = outputter
    cams.run()

def main17c():
    with open("hard.txt", "r") as fh:
        lines = [line.strip() for line in fh]
    print(lines)
    walk ="".join(list(findWalkFromLines(lines)))
    print(walk)
    print(encodeWalk(walk))
    solver = Solver(walk)
    for res in solver.solve(0, [], "", 0):
        print(res)
                
    
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
            if True: # len(enc) > 12:
                me.validMacros.add(i)
            me.cost[i] = len(enc)
            me.encoded[i] = enc
            ps = substringPositions(me.walk, c)
            for p in ps:
                me.candidatesByPosition[p].append(i)
        me.exclusions = collections.defaultdict(lambda: set())
        #for (i, cs) in me.candidatesByPosition.items():
        #    for j in range(len(cs)):
        #        for k in range(j+1, len(cs)):
        #            me.exclusions[j].add(k)
        #            me.exclusions[k].add(j)
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
        for m in macros:
            if m in me.candidatesByPosition[pos]:
                addendum = "ABC"[macros.index(m)]
                if main == "":
                    main2 = addendum
                    dc = 1
                else:
                    main2 = main + "," + addendum
                    dc = 2
                for res in me.solve(pos + len(me.candidates[m]), macros, main2, cost + dc):
                    yield res
        if len(macros) < 3:
            for c in me.candidatesByPosition[pos]:
                if c in macros:
                    continue
                if c in me.validMacros:
                    addendum = "ABC"[len(macros)]
                    if main == "":
                        main2 = addendum
                        dc = 1
                    else:
                        main2 = main + "," + addendum
                        dc = 2
                    for res in me.solve(pos + len(me.candidates[c]), macros + [c], main2, cost + dc):
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

                
PROGRAM = parseProgram("input.txt")
def tractor(x, y):
    machine = IntCode(PROGRAM)
    inputList = [x, y]
    machine.input = iter(inputList).__next__
    o  = []
    machine.output = o.append
    while not machine.hasHalted():
        machine.step()
    return o[0]
            


def main19():
    t = {}
    out = 0
    outputs = set()
    def output(x):
        nonlocal out
        outputs.add(x)
        out += x
        
    for y in range(50):
        print()
        for x in range(50):
            print(".8"[tractor(x,y)], sep="", end="")

def main19b():
    l = 4
    r = 4
    y = 4
    ls = [None, None, None, None, 4]
    rs = [None, None, None, None, 4]
    while True:
        y += 1
        l2 = ls[-1]
        r2 = rs[-1]
        while tractor(l2, y) == 0:
            l2 += 1
        while tractor(r2, y) == 0:
            r2 += 1
        while tractor(r2+1, y) == 1:
            r2 += 1
        ls.append(l2)
        rs.append(r2)
        if y > 120:
            pl = ls[y - 99]
            pr = rs[y - 99]
            if pl <= l2 <= pr and pl <= (l2 + 99) <= pr and r2 - l2 + 1 >= 100:
                print(l2 ,  y - 99)
                return
           
        


main19b()
