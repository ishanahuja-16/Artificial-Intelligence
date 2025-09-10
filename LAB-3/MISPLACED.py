import heapq
from collections import deque

GOAL = (1,2,3,4,5,6,7,8,0)

def h_misplaced(state):
    return sum(1 for i,v in enumerate(state) if v!=0 and v!=GOAL[i])

def neighbors(state):
    idx = state.index(0)
    r,c = divmod(idx,3)
    moves=[]
    for dr,dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr,nc = r+dr,c+dc
        if 0<=nr<3 and 0<=nc<3:
            nidx=nr*3+nc
            new=list(state)
            new[idx],new[nidx]=new[nidx],new[idx]
            moves.append(tuple(new))
    return moves

def reconstruct_path(came_from, cur):
    path=deque()
    while cur in came_from:
        path.appendleft(cur)
        cur=came_from[cur]
    path.appendleft(cur)
    return list(path)

def a_star(start):
    if start==GOAL:
        return [start]
    open_heap=[]
    entry=0
    g={start:0}
    f=g[start]+h_misplaced(start)
    heapq.heappush(open_heap,(f,entry,start))
    came_from={}
    closed=set()

    while open_heap:
        _,_,cur=heapq.heappop(open_heap)
        if cur==GOAL:
            return reconstruct_path(came_from,cur)
        closed.add(cur)
        for nb in neighbors(list(cur)):
            tentative_g=g[cur]+1
            if nb in closed and tentative_g>=g.get(nb,float('inf')):
                continue
            if tentative_g<g.get(nb,float('inf')):
                came_from[nb]=cur
                g[nb]=tentative_g
                f=tentative_g+h_misplaced(nb)
                entry+=1
                heapq.heappush(open_heap,(f,entry,nb))
    return None

def pretty(state):
    return "\n".join(
        " ".join(str(x) if x!=0 else "_" for x in state[i:i+3])
        for i in range(0,9,3)
    )

if __name__=="__main__":
    start=(1,2,3,0,4,6,7,5,8)
    print("Start:\n",pretty(start))
    print("Goal:\n",pretty(GOAL))
    path=a_star(start)
    if path:
        print(f"\nSolved in {len(path)-1} moves (Misplaced Tiles Heuristic):")
        for i,st in enumerate(path):
            print(f"\nStep {i}:")
            print(pretty(st))
    else:
        print("No solution found.")