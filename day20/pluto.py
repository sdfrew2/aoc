import collections
# day 20

def neighbors(p):
    (x, y) = p
    return [(x+1, y), (x-1,y), (x, y+1), (x, y-1)]


class Maze:
    def __init__(me, data):
        lines = [line for line in data.split("\n") if line != ""]
        me.tiles = collections.defaultdict(lambda: " ")
        me.h = len(lines)
        me.w = len(lines[0])
        me.warps = {}
        labelPositions = collections.defaultdict(lambda: [])
        me.labelPositions = labelPositions
        for (y, line) in enumerate(lines):
            for (x, ch) in enumerate(line):
                me.tiles[(x, y)] = ch
        for ((x,y), t) in list(me.tiles.items()):
            if t.isalpha():
                tr = me.tiles[(x+1, y)]
                td = me.tiles[(x, y+1)]
                if tr.isalpha():
                    label = t + tr
                    if me.tiles[(x+2, y)] == ".":
                        labeledPos = (x+2, y)
                    else:
                        labeledPos = (x-1, y)
                elif td.isalpha():
                    label = t + td
                    if me.tiles[(x, y+2)] == ".":
                        labeledPos = (x, y+2)
                    else:
                        labeledPos = (x, y-1)
                if tr.isalpha() or td.isalpha():
                    #print((x,y), "appending ", labeledPos, "for" , label, ";tr=",tr,"td=",td)
                    labelPositions[label].append(labeledPos)
        for (l, ps) in labelPositions.items():
            if len(ps) == 2:
                me.warps[ps[0]] = ps[1]
                me.warps[ps[1]] = ps[0]
                
                
    def solve(me):
        start = me.labelPositions["AA"][0]
        goal = me.labelPositions["ZZ"][0]
        q = collections.deque()
        q.append((start, 0))
        seen = set()
        while len(q) > 0:
            #print(q)
            (node, depth) = q.popleft()
            if node == goal:
                return depth
            seen.add(node)  
            nextNodes = [p for p in neighbors(node) if me.tiles[p] == "."]
            if node in me.warps:
                nextNodes.append(me.warps[node])
            for nextNode in nextNodes:
                if not nextNode in seen:
                    q.append((nextNode, depth+1))
    

class RecMaze:
    def __init__(me, data):
        lines = [line for line in data.split("\n") if line != ""]
        me.tiles = collections.defaultdict(lambda: " ")
        me.h = len(lines)
        me.w = len(lines[0])
        me.warps = {}
        me.outer = set()
        labelPositions = collections.defaultdict(lambda: [])
        me.labelPositions = labelPositions
        for (y, line) in enumerate(lines):
            for (x, ch) in enumerate(line):
                me.tiles[(x, y)] = ch
        for ((x,y), t) in list(me.tiles.items()):
            if t.isalpha():
                tr = me.tiles[(x+1, y)]
                td = me.tiles[(x, y+1)]
                if tr.isalpha():
                    label = t + tr
                    if me.tiles[(x+2, y)] == ".":
                        labeledPos = (x+2, y)
                    else:
                        labeledPos = (x-1, y)
                elif td.isalpha():
                    label = t + td
                    if me.tiles[(x, y+2)] == ".":
                        labeledPos = (x, y+2)
                    else:
                        labeledPos = (x, y-1)
                if tr.isalpha() or td.isalpha():
                    #print((x,y), "appending ", labeledPos, "for" , label, ";tr=",tr,"td=",td)
                    labelPositions[label].append(labeledPos)
        for (l, ps) in labelPositions.items():
            if len(ps) == 2:
                me.warps[ps[0]] = ps[1]
                me.warps[ps[1]] = ps[0]
            for p in ps:
                (x,y) = p
                if x == 2 or y == 2 or x == me.w-3 or y == me.h-3:
                    me.outer.add(p)
            
                
                
    def solve(me):
        start = (me.labelPositions["AA"][0], 0)
        goal = (me.labelPositions["ZZ"][0], 0)
        q = collections.deque()
        q.append((start, 0))
        seen = set()
        while len(q) > 0:
            #print(q)
            (node, cost) = q.popleft()
            if node in seen:
                continue
            seen.add(node)
            if node == goal:
                return cost
            (p, depth) = node
            for n in neighbors(p):
                if me.tiles[n] == ".":
                    q.append(((n, depth), cost+1))
            if p in me.warps:
                if p in me.outer:
                    if depth > 0:
                        q.append(((me.warps[p], depth-1), cost+1))
                else:
                    q.append(((me.warps[p], depth+1), cost+1))

            
        
example = """
         A           
         A           
  #######.#########  
  #######.........#  
  #######.#######.#  
  #######.#######.#  
  #######.#######.#  
  #####  B    ###.#  
BC...##  C    ###.#  
  ##.##       ###.#  
  ##...DE  F  ###.#  
  #####    G  ###.#  
  #########.#####.#  
DE..#######...###.#  
  #.#########.###.#  
FG..#########.....#  
  ###########.#####  
             Z       
             Z       
"""


def main20():
    with open("input.txt", "r") as fh:
        data = fh.read()
    maze = Maze(data)
    print(maze.labelPositions)
    print(maze.solve())

def main20b():
    with open("help.txt", "r") as fh:
        data = fh.read()
    #data = example
    maze = RecMaze(data)
    print(maze.labelPositions)
    print(maze.outer)
    print(maze.solve())

main20b()


    
