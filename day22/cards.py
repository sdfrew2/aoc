

class Shuffle:
    def __init__(me, n, data):
        me.cardpos = list(range(n))
        for line in data.split("\n"):
            line = line.strip()
            tokens = line.split()
            for t in tokens:
                try:
                    num = int(t)
                except:
                    pass
            if "new" in line:
                me.reverse()
            elif "cut" in line:
                me.cut(num)
            elif "reme" in line:
                me.dealWithIncrement(num)
            else:
                print("error", line)
            #print(line, ": " , me.deck())

    def deck(me):
        result = [0]*len(me.cardpos)
        for (card, pos) in enumerate(me.cardpos):
            #print(card, pos)
            result[pos] = card
        return result

        
            


    def cut(me, n):
        if n < 0:
            n = len(me.cardpos) + n
        newpos = me.cardpos[:]
        for (card, pos) in enumerate(me.cardpos):
            newpos[card] = (pos - n) % len(me.cardpos)
            me.cardpos = newpos

    def reverse(me):
        n = len(me.cardpos)
        me.cardpos = [n - 1 - p for p in me.cardpos]

    def dealWithIncrement(me, k):
        n = len(me.cardpos)
        me.cardpos = [(k*p) % n  for p in me.cardpos]

    
        


def computeShufflePositionFunction(m, data):
    a = 1
    c = 0 # ax+c
    for line in data.split("\n"):
        line = line.strip()
        tokens = line.split()
        for t in tokens:
            try:
                num = int(t)
            except:
                pass
        if "new" in line:
            a = -a
            c = -c-1
        elif "cut" in line:
            if num < 0:
                num = num + m
            c -= num
        elif "reme" in line:
            a *= num
            c *= num
        else:
            print("error", line)
    a %= m
    c %= m
    return (a, c)
        
        
def solveLDE2(a, b, c):
    if a < b:
        (y, x) = solveLDE2(b, a, c)
        return (x,y)
    if b == 0:
        return (c // a, 0)
    # ax + by = c
    q = a // b
    r = a % b
    # (qb + r)x + by = c
    # qbx + rx + by = c
    # b(qx+y) + rx = c
    # x2 = qx+y
    # y2 = x
    (x2, y2) = solveLDE2(b, r, c)
    x = y2
    y = x2 - q*x
    return (x,y)
            
def invertModulo(a, m):
    (x, y) = solveLDE2(a, m, 1)
    return x % m


def main22():
    with open("input.txt", "r") as fh:
        data = fh.read()
    s = Shuffle(10007, data)
    print(s.cardpos[2019])
    (a,c) = computeShufflePositionFunction(10007, data)
    print((a*2019 + c) % 10007)
    print(a,c)



def main22b():
    with open("input.txt", "r") as fh:
        data = fh.read()
    M = 119315717514047
    S = 101741582076661
    s = computeShufflePositionFunction(M, data)
    origPoint = 2020
    point = None
    j = 0
    while point != origPoint:
        if point == None:
            point = origPoint
        point = s[0] * point + s[1]
        point %= M
        j += 1
    print(j)
        

    sp = powerShuffle(M, s, S)
    (a2, b2) = invertShuffle(M, sp)
    print((a2 * 2020 + b2) % M)

def composeShuffle(m, s1, s2):
    (a1, b1) = s1
    (a2, b2) = s2
    # (a1*x+b1)*a2 + b2 = a1*a2*x + b1*a2 + b2
    ar = a1*a2 % m
    br = (b1*a2 + b2) % m
    return (ar, br)

def invertShuffle(m, s):
    (a, b) = s
    # z(ax + b ) + s = x
    # a'(ax+b) = x + a'b 
    a2 = invertModulo(a, m)
    b2 = (-a2 * b) % m 
    return (a2, b2)
    


def powerShuffle(m, s, n):
    if n == 1:
        return s
    if n == 0:
        return (1, 0)
    half = powerShuffle(m, s, n // 2)
    if n % 2 == 0:
        return composeShuffle(m, half, half)
    else:
        return composeShuffle(m, composeShuffle(m, half, half), s)


main22b()

DATA = """deal into new stack
cut -2
deal with increment 7
cut 8
cut -4
deal with increment 7
cut 3
deal with increment 9
deal with increment 3
cut -1"""

#s = Shuffle(10, DATA)
#print(s.deck())
