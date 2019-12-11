from itertools import permutations
import collections

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


def main9a():
    program = parseProgram("input.txt")
    machine = IntCode(program)
    machine.feed(1)
    machine.output = print
    while not machine.hasHalted():
        machine.step()

def main9b():
    program = parseProgram("input.txt")
    machine = IntCode(program)
    machine.feed(2)
    machine.output = print
    while not machine.hasHalted():
        machine.step()

class Drone:
    def __init__(me, program, board):
        machine = IntCode(program)
        me.machine = machine
        me.position = 0+0j
        me.direction = 0+1j
        me.output = [ None ] 
        me.board = board
        me.painted = set()
        me.turn = 0
        me.white = set()
        machine.input = me.getColor
        machine.output = me.handleOutput

    def getColor(me):
        return me.board[me.position]
    
    def handleOutput(me, x):
        if me.turn % 2 == 0:
            me.board[me.position] = x
            me.painted.add(me.position)
            if x == 1:
                me.white.add(me.position)
        else:
            if x == 0:
                me.direction *= 0+1j
                me.position += me.direction
            else:
                me.direction *= 0-1j
                me.position += me.direction
        me.turn += 1

    def run(me):
        while not me.machine.hasHalted():
            me.machine.step()

def main11():
    program = parseProgram("input.txt")
    board = collections.defaultdict(lambda: 0)
    drone = Drone(program, board)
    drone.run()
    print(len(drone.painted))

        
def main11b():
    program = parseProgram("input.txt")
    board = collections.defaultdict(lambda: 0)
    board[0+0j] = 1
    drone = Drone(program, board)
    drone.run()
    white = drone.white
    minx = min((x.real for x in white))
    miny = min((x.imag for x in white))
    maxx = max((x.real for x in white))
    maxy = max((x.imag for x in white))
    coords = set()
    for x in white:
        p = (int(x.real - minx), int(10 - (x.imag - miny)))
        coords.add(p)
    for i in range(16):
        print()
        for j in range(50):
            ch = ' '
            if (j, i) in coords:
                ch = '8'
            print(ch, sep='', end='')



main11b()
