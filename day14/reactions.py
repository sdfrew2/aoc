import math
import re
import collections

def parseProduct(p):
    p = p.strip()
    parts = re.split("([0-9]+)", p)
    return (parts[2], int(parts[1]))

def parseReaction(line):
    line = line.strip()
    line = line.replace(" ", "")
    lr = line.split("=>")
    lhs = [parseProduct(p) for p in lr[0].split(",")]
    rhs = [parseProduct(p) for p in lr[1].split(",")]
    return (lhs, rhs[0])

class ReactionTable:
    def __init__(me, reactions):
        me.requirements = {}
        me.outputAmounts = {}
        for r in reactions:
            out = r[1]
            me.requirements[out[0]] = r[0]
            me.outputAmounts[out[0]] = out[1]
    def __repr__(me):
        return "REQ="+str(me.requirements)+", OA=" + str(me.outputAmounts)



def stepReactionSystem(state, rt):
    c = None
    a = None
    for (_c, _a) in state.items():
        if _a >= 0 or _c == "ORE":
            continue
        (c, a) = (_c, _a)
        break
    if c == None:
        return False
    required = -a
    numReactions = int(math.ceil(required / rt.outputAmounts[c]))
    state[c] += numReactions * rt.outputAmounts[c]
    for (rc, ra) in rt.requirements[c]:
        state[rc] -= ra*numReactions
    ks = list(state.keys())
    for k in ks:
        if state[k] == 0:
            del state[k]
    return True
    
    
    
        
        

import time
            
                               
            

def main14():
    with open("input.txt", "r") as fh:
        rt = ReactionTable([parseReaction(line) for line in fh])
    reqFuel = rt.outputAmounts["FUEL"]
    print(requiredOre(rt, reqFuel))
    state = collections.defaultdict(lambda: 0)
    state["FUEL"] = -reqFuel
    while stepReactionSystem(state, rt):
        pass

def main14b():
    with open("input.txt", "r") as fh:
        rt = ReactionTable([parseReaction(line) for line in fh])
    fuel = potentialFuel(rt, 1000000**2)
    print(fuel)

def requiredOre(rt, fuel):
    state = collections.defaultdict(lambda: 0)
    state["FUEL"] = -fuel
    while stepReactionSystem(state, rt):
        pass
    return -state["ORE"]

def potentialFuel(rt, ore):
    fuelCandidate = 1
    while True:
        req = requiredOre(rt, fuelCandidate)
        if req > ore:
            break
        fuelCandidate *= 2
    return fuelSearch(rt, ore, fuelCandidate // 2, fuelCandidate)

def fuelSearch(rt, ore, loFuel, hiFuel):
    if hiFuel - loFuel <= 1:
        return loFuel
    midFuel = (loFuel + hiFuel) // 2
    req = requiredOre(rt, midFuel)
    if req > ore:
        return fuelSearch(rt, ore, loFuel, midFuel)
    return fuelSearch(rt, ore, midFuel, hiFuel)

        


    
    
    
main14b()
    
    
