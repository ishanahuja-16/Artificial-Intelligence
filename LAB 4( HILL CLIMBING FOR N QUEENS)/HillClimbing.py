import random

def print_board(board):
    n = len(board)
    for i in range(n):
        row = ["Q" if board[i] == j else "." for j in range(n)]
        print(" ".join(row))
    print()

def calculate_cost(board):
    n = len(board)
    cost = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j] or abs(board[i] - board[j]) == abs(i - j):
                cost += 1
    return cost

def get_best_neighbor(board):
    n = len(board)
    best_board = list(board)
    best_cost = calculate_cost(board)

    for row in range(n):
        for col in range(n):
            if board[row] != col:
                neighbor = list(board)
                neighbor[row] = col
                cost = calculate_cost(neighbor)
                if cost < best_cost:
                    best_cost = cost
                    best_board = neighbor
    return best_board, best_cost

def hill_climbing(n):
    current_board = [random.randint(0, n - 1) for _ in range(n)]
    current_cost = calculate_cost(current_board)

    print("Initial Board:")
    print_board(current_board)
    print(f"Initial Cost: {current_cost}\n")

    step = 1
    while True:
        neighbor, neighbor_cost = get_best_neighbor(current_board)
        print(f"Step {step}:")
        print("Current Board:")
        print_board(current_board)
        print(f"Current Cost: {current_cost}")
        print(f"Best Neighbor Cost: {neighbor_cost}\n")

        if neighbor_cost >= current_cost:
            break

        current_board = neighbor
        current_cost = neighbor_cost
        step += 1

    print("Final Board:")
    print_board(current_board)
    print(f"Final Cost: {current_cost}")

    if current_cost == 0:
        print("Goal State Reached!")
    else:
        print("Stuck in Local Minimum!")

# Run for 4-Queens
hill_climbing(4)