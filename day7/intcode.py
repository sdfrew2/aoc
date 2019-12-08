from itertools import permutations

FORMATS = {1: "IIO", 2: "IIO", 3: "O", 4: "I", 5: "II", 6: "II", 7: "IIO", 8: "IIO", 99: ""}

class IntCode:
    def __init__(me, program):
        me.program = program[:]
        me.reset()

    def hasHalted(me):
        return me.state == 1
            
    def reset(me):
        me.mem = me.program[:]
        me.pos = 0
        me.state = 0
        me.inqueue = []

    def decodeInstruction(me, p):
        op = me.mem[p]
        baseOp = op % 100
        fmt = FORMATS[baseOp]
        modes = op // 100
        params = []
        for (i, paramStyle) in enumerate(fmt):
            mode = modes % 10
            if paramStyle == "O":
                mode = 1
            modes = modes // 10
            params.append((me.mem[p+1+i], mode))
        return (baseOp, params)

    def resolveParam(me, x, mode):
        if mode == 1:
            return x
        return me.mem[x]

    def feed(me , x):
        me.inqueue.append(x)

    def step(me):
        if me.state == 1:
            return False
        op, params = me.decodeInstruction(me.pos)
        paramValues = []
        for (p, mode) in params:
            pval = me.resolveParam(p, mode)
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
        elif op == 7:
            v = 0
            if p[0] == p[1]:
                v = 1
            me.mem[p[2]] = v
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

def main7a():
    d = parseProgram("input7.dat")
    scores = []
    machines = []
    for phaseConfig in permutations((0, 1, 2, 3, 4)):
        lastOut = [ 0 ]
        for i in range(5):
            machine = IntCode(d)
            params = iter([phaseConfig[i], lastOut[0]])
            machine.feed(phaseConfig[i])
            machine.feed(lastOut[0])
            machine.output = makeArrayAssigner(lastOut)
            machine.run()
        scores.append(lastOut[0])
    print(max(scores))
    
def main7b():
    d = parseProgram("input7.dat")
    scores = []
    machines = []
    for phaseConfig in permutations((5,6,7,8,9)):
        machines = [None] * 5
        lastOutputs = {}
        def makeOutputter(j):
            def result(o):
                machines[(j+1) % 5].feed(o)
                lastOutputs[j] = o
            return result
        for i in range(5):
            machines[i] = IntCode(d)
            machines[i].feed(phaseConfig[i])
            machines[i].output = makeOutputter(i)
        machines[0].feed(0)
        while not all((m.hasHalted() for m in machines)):
            for m in machines:
                m.step()
        score = lastOutputs[4]
        scores.append(score)
    print(max(scores))



main7b()
