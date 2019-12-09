from itertools import permutations

FORMATS = {1: "IIO", 2: "IIO", 3: "O", 4: "I", 5: "II", 6: "II", 7: "IIO", 8: "IIO", 9: "I" , 99: ""}

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
        me.inqueue = []
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

    def feed(me , x):
        me.inqueue.append(x)

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
            if len(me.inqueue) == 0:
                me.pos -= 2
            else:
                x = me.inqueue.pop(0)
                me.mem[p[0]] = x
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


main9b()
