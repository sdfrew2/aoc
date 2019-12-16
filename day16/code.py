
BASEKEY = [0, 1, 0, -1]

def key(si, ti):
    l = len(BASEKEY)
    return BASEKEY[(si + 1) // ((ti+1) * 1) % l]

def func(data):
    output = [0] * len(data)
    s = 0    
    for si in range(len(data)):
        for ti in range(len(data)):
            output[ti] += data[si] * key(si, ti)
    for i in range(len(data)):
        d = output[i]
        if d < 0:
            output[i] = (-output[i]) % 10
        else:
            output[i] %= 10
    return output

def encode(data,m=0):
    for i in range(100):
        print("pass", i)
        data = func2(data,m=m)
    return data

def parseData(s):
    return [int(c) for c in s.strip()]

def main16():
    with open("input.txt", "r") as fh:
        raw = fh.read().strip()
        data = [int(c) for c in raw]
    print(encode(data)[0:8])


def keychunks(y):
    n = 0
    while True:
        base = 4*y*n - 1
        yield (base + y, y, 1)
        yield (base + 3*y, y, -1)
        n += 1

def cappedKeychunks(y, maxl):
    for (start, l, s) in keychunks(y):
        if start >= maxl:
            return
        if start + l > maxl:
            yield (start, maxl - start, s)
            return
        else:
            yield (start, l, s)



class Buffer:
    def __init__(me, message):
        me.message = message
        me.csums = {}
    def sum(me, start, l):
        if l == 0:
            return 0
        start = start % len(me.message)
        if start + l <= len(me.message):
            key = (start, l)
            if key in me.csums:
                return me.csums[key]
            else:
                s = sum(me.message[start:(start+l)])
                me.csums[key] = s
                return s
        elif start == 0:
            k = l // len(me.message)
            r = l % len(me.message)
            return k*me.sum(0, len(me.message)) + me.sum(0, r)
        else:
            return me.sum(start, len(me.message) - start) + me.sum(0, l - len(me.message) + start)

            

def pows2(n):
    multiplier = 1
    result = []
    while n > 0:
        bit = n % 2
        n = n // 2
        if bit != 0:
            result.append(multiplier)
        multiplier *= 2
    return result


class Buffer2:
    def __init__(me, message):
        me.message = message
        me.sums = [0] * (len(message) + 1)
        s = 0
        for i in range(len(message)):
            s += message[i]
            me.sums[i+1] = s
        me.cache = {}
    def sum(me, start, l):
        return me.sums[start+l] - me.sums[start]
            




def func2(data,m=0):
    buf = Buffer2(data)
    result = [0] * len(data)
    for i in range(m, len(data)):
        s = 0
        for (start, l, sign) in cappedKeychunks(i+1, len(data)):
            s += buf.sum(start, l) * sign
        if s < 0:
            s = -s
        result[i] = s % 10
    return result


def cached(f):
    cache = {}
    def result(*args):
        if args in cache:
            return cache[args]
        return f(*args)
    return result




def recsolv0(data, y_, x_):
    @cached 
    def recsolv(y, x):
        if y == 0:
            return data[x]
        result = 0
        for (s, l, sgn) in cappedKeychunks(y, len(data)):
            result += recsolv(y-1, x)
                
        
        
    

def main16b():
    with open("input.txt", "r") as fh:
        raw = fh.read().strip()
        data = [int(c) for c in raw] * 10000
    index = int(raw[0:7])
    final = encode(data,m=index)
    print(final[index:index+8])


main16b()

#print(encode([1, 0, 0, 0, 0] * 10)) 
