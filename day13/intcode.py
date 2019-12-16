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


FONT = " +#=o"



class Game:
    def __init__(me, program):
        me.machine = IntCode(program)
        me.machine.output = me.handleOutput
        me.outputBuffer = []
        me.machine.input = me.queryInput
        me.screen = [0]*(36*24)
        me.score=0
        me.ball=0
        me.paddle=0

    def handleOutput(me, x):
        me.outputBuffer.append(x)
        if len(me.outputBuffer) == 3:
            me.paint(*me.outputBuffer)
            me.outputBuffer = []

    def paint(me, x, y, c):
        if c == 4:
            me.ball = x
        if c == 3:
            me.paddle = x 
        if x == -1 and y == 0:
            me.score = c
        else:
            me.screen[W*y+x] = c

    def showFrame(me):
        print("Score: " + str(me.score))
        for y in range(24):
            print()
            for x in range(W):
                print(FONT[me.screen[W*y+x]], sep="", end="")

    def queryInput(me):
        me.showFrame()
        if me.ball < me.paddle:
            return -1
        if me.ball > me.paddle:
            return 1
        return 0


    def run(me):
        m = me.machine
        while not m.hasHalted():
            m.step()
        me.showFrame()        
        


def main13():
    program = parseProgram("input.txt")
    game = Game(program)
    game.run()
    print(len([(pos, c) for (pos, c) in game.screen.items() if c == 2]))

def main13b():
    program = parseProgram("input.txt")
    program[0] = 2
    game = Game(program)
    game.run()

main13b()
