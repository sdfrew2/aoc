

class Shuffle:
    def __init__(me, n, data):
        me.cardpos = list(range(n))
        print("initial:", me.deck())
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

    
        


        
        
        
        
        
            
        

def main22():
    with open("input.txt", "r") as fh:
        data = fh.read()
    s = Shuffle(10007, data)
    print(s.cardpos[2019])



main22()


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
