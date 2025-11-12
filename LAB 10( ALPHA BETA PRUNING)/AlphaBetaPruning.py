import math


tree = {
    'A': ['B', 'C'],
    'B': ['D', 'E'],
    'C': ['F', 'G'],
    'D': ['H', 'I'],
    'E': ['J', 'K'],
    'F': ['L', 'M'],
    'G': ['N', 'O'],
    'H': [], 'I': [], 'J': [], 'K': [],
    'L': [], 'M': [], 'N': [], 'O': []
}

values = {
    'H': 3, 'I': 5,
    'J': 6, 'K': 9,
    'L': 1, 'M': 2,
    'N': 0, 'O': -1
}

def get_children(node):
    return tree.get(node, [])

def evaluate(node):
    return values.get(node, 0)

def alphabeta(node, depth, alpha, beta, maximizingPlayer):
    if not get_children(node) or depth == 0:
        return evaluate(node)
    
    if maximizingPlayer:
        value = -math.inf
        print(f"MAX Node {node}: α={alpha}, β={beta}")
        for child in get_children(node):
            value = max(value, alphabeta(child, depth - 1, alpha, beta, False))
            alpha = max(alpha, value)
            print(f"  MAX updating α={alpha} after visiting {child}")
            if alpha >= beta:
                print(f"   Pruned remaining children of {node} (α={alpha}, β={beta})")
                break
        return value
    else:
        value = math.inf
        print(f"MIN Node {node}: α={alpha}, β={beta}")
        for child in get_children(node):
            value = min(value, alphabeta(child, depth - 1, alpha, beta, True))
            beta = min(beta, value)
            print(f"  MIN updating β={beta} after visiting {child}")
            if beta <= alpha:
                print(f"   Pruned remaining children of {node} (α={alpha}, β={beta})")
                break
        return value


print("\n--- Running Alpha–Beta Pruning on Minimax Tree ---\n")
optimal_value = alphabeta('A', depth=4, alpha=-math.inf, beta=math.inf, maximizingPlayer=True)
print("\nOptimal value at the root (A):", optimal_value)