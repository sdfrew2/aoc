import math

def addvec(v, w):
    return tuple((v[i] + w[i] for i in range(len(v))))

def subvec(v, w):
    return tuple((v[i] - w[i] for i in range(len(v))))

def negvec(v):
    return tuple((-a for a in v))

def sign(x):
    if x > 0:
        return 1
    if x < 0:
        return -1
    return 0
    

def computeVelocityUpdate(pos1, pos2):
    d = subvec(pos2, pos1)
    d = tuple(map(sign, d))
    return d

class Body:
    def __init__(me, pos, vel):
        me.pos = pos[:]
        me.v = vel[:]

    def __repr__(me):
        return str(me.pos) + " v=" + str(me.v)
    
    def energy(me):
        return sum((abs(x) for x in me.pos)) * sum((abs(x) for x in me.v))

def stepSystem(bodies):
    for i in range(len(bodies)):
        for j in range(i+1, len(bodies)):
            a = bodies[i]
            b = bodies[j]
            dv = computeVelocityUpdate(a.pos, b.pos)
            a.v = addvec(a.v, dv)
            b.v = subvec(b.v, dv)
    for a in bodies:
        a.pos = addvec(a.pos, a.v)

def stepAxis(pv):
    ps, vs = pv
    n = len(ps)
    dv = [0] * n
    for i in range(n):
        for j in range(i+1, n):
            delta = sign(ps[j] - ps[i])
            dv[i] += delta
            dv[j] -= delta
    vs = addvec(vs, dv)
    nextps = addvec(ps, vs)
    return (nextps, vs)

        

def findloop(x, f):
    seen = {}
    seen[x] = 0
    i = 0
    while True:
        x = f(x)
        i += 1
        if x in seen:
            s = seen[x]
            return (i-s, s)


            

def main12():
    z = (0, 0, 0)
    a = Body((-10, -10, -13), z)
    b = Body((5,5,-9), z)
    c = Body((3, 8, -16), z)
    d = Body((1, 3, -3), z)
    system = [a, b, c, d]
    for i in range(1000):
        stepSystem(system)
    print(sum((b.energy() for b in system)))

def main12b():
    system0 = ((-10, 5, 3, 1), (0, 0, 0, 0))
    system1 = ((-10, 5, 8, 3), (0, 0, 0, 0))
    system2 = ((-13, -9, -16, -3), (0, 0, 0, 0))
    l = 1
    for s in [system0, system1, system2]:
        loopsize = findloop(s, stepAxis)[0]
        l = (l * loopsize) // math.gcd(l, loopsize)
    print(l)

main12b()

