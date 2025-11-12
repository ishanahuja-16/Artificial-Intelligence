goal = [[1,2,3],
        [8.0.4],
        [7,6,5]]

moves = [(-1,0),(1,0),(0,-1),(0,1)]

def find_zero(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j

def get_neighbors(state):
    x, y = find_zero(state)
    neighbors = []
    for dx, dy in moves:
        nx, ny = x+dx, y+dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)
    return neighbors

def dfs(state, visited):
    if state == goal:
        return [state]
    visited.add(str(state))
    for neighbor in get_neighbors(state):
        if str(neighbor) not in visited:
            path = dfs(neighbor, visited)
            if path:
                return [state] + path
    return None

def dls(state, goal, depth, path, visited):
    if state == goal:
        return path
    if depth == 0:
        return None
    visited.add(str(state))
    for neighbor in get_neighbors(state):
        if str(neighbor) not in visited:
            result = dls(neighbor, goal, depth-1, path+[neighbor], visited)
            if result:
                return result
    return None

def ids(start, goal, max_depth=20):
    for depth in range(max_depth+1):
        visited = set()
        result = dls(start, goal, depth, [start], visited)
        if result:
            return result
    return None

if __name__ == "__main__":
    start = [[1,2,3],
             [8,6,4],
             [0,7,5]]

    print("Solving 8-Puzzle using DFS:")
    solution_dfs = dfs(start, set())
    if solution_dfs:
        print(f"DFS solution found in {len(solution_dfs)-1} moves:")
        for step in solution_dfs:
            for row in step:
                print(row)
            print("----------------------------------------------")
    else:
        print("No solution found with DFS.")

    print("\nSolving 8-Puzzle using IDS:")
    solution_ids = ids(start, goal, max_depth=20)
    if solution_ids:
        print(f"IDS solution found in {len(solution_ids)-1} moves:")
        for step in solution_ids:
            for row in step:
                print(row)
            print("---------------------------------------------")
    else:
        print("No solution found with IDS.")