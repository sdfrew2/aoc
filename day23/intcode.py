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



class NIC(IntCode):
    def __init__(me, program, network, index):
        super().__init__(program)
        me.network = network
        me.initialized = False
        me.index = index
        me.queue = collections.deque()
        me.partialOutput = []
        me.input = me._input
        me.output = me._output
    
    def _input(me):
        if me.initialized:
            if len(me.queue) == 0:
                #print("R", me.index, -1)
                return -1
            else:
                v = me.queue.popleft()
                print("R", me.index, v)
                return v
        else:
            me.initialized = True
            return me.index

    def transmit(me, address, value):
        print("T", address, value)
        if address == 255:
            print(value)
        else:
            me.network[address].queue.append(value)
            print("*")

    def _output(me, x):
        me.partialOutput.append(x)
        if len(me.partialOutput) == 3:
            for o in (me.partialOutput[1:]):
                me.transmit(me.partialOutput[0], o)

        



    
class Controller:
    def __init__(me, program):
        me.machines = []
        for i in range(50):
            me.machines.append(me.createMachine(program, i))

    def createMachine(me, program, index):
        return NIC(program, me.machines, index)

    def run(me):
        z = 0
        while True:
            for (i, m) in enumerate(me.machines):
                if not m.hasHalted():
                    m.step()
                if z > 100000 and i == 29:
                    pass # print("#", i, m.pos)
            z += 1

def main23():
    con = Controller(parseProgram("input.txt"))
    con.run()
    
        

main23()
