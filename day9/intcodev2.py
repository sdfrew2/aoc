from itertools import permutations

FORMATS = {1: "IIO", 2: "IIO", 3: "O", 4: "I", 5: "II", 6: "II", 7: "IIO", 8: "IIO", 9: "I" , 99: ""}

class Cell:
    def __init__(me, machine, val, mode):
        me.mode = mode
        me.machine = machine
        me.val = val

    def set(me, x):
        mem = me.machine.mem
        dp = me.machine.dp
        if me.mode == 0:
            mem[me.val] = x
        elif me.mode == 2:
            mem[me.val + dp] = x

    def get(me):
        mem = me.machine.mem
        dp = me.machine.dp
        if me.mode == 0:
            return mem[me.val]
        elif me.mode == 1:
            return me.val
        elif me.mode == 2:
            return mem[me.val + dp]

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
            params.append(Cell(me, me.mem[p + 1 + i], mode))
        return (baseOp, params)

    def feed(me , x):
        me.inqueue.append(x)

    def step(me):
        if me.state == 1:
            return False
        op, params = me.decodeInstruction(me.pos)
        #print("[" + str(me.pos) + "]" , op, params)
        me.pos += 1 + len(params)
        me.executeInstruction(op, params)
        if me.pos < 0:
            return False
        return True

    def run(me):
        while me.step():
            pass
        
    def executeInstruction(me, op, p):
        if op == 1:
            p[2].set(p[0].get() + p[1].get())
        elif op == 2:
            p[2].set(p[0].get() * p[1].get())
        elif op == 3:
            if len(me.inqueue) == 0:
                me.pos -= 2
            else:
                x = me.inqueue.pop(0)
                p[0].set(x)
        elif op == 4:
            me.output(p[0].get())
        elif op == 5:
            if p[0].get() != 0:
                me.pos = p[1].get()
        elif op == 6:
            if p[0].get() == 0:
                me.pos = p[1].get()
        elif op == 7:
            v = 0
            if p[0].get() < p[1].get():
                v = 1
            p[2].set(v)
        elif op == 8:
            v = 0
            if p[0].get() == p[1].get():
                v = 1
            p[2].set(v)
        elif op == 9:
            me.dp += p[0].get()
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


main9a()
