import math

def check_win(board):
    wins = [(0,1,2),(3,4,5),(6,7,8),
            (0,3,6),(1,4,7),(2,5,8),
            (0,4,8),(2,4,6)]
    for a,b,c in wins:
        if board[a] == board[b] == board[c] != 0:
            return board[a]
    return 0 if 0 not in board else None

def selection(board, player):
    result = check_win(board)
    if result is not None: return result
    scores = []
    for i in range(9):
        if board[i] == 0:
            board[i] = player
            scores.append(selection(board, -player))
            board[i] = 0
    return max(scores) if player == 1 else min(scores)

def best_move(board):
    return max((selection(board[:i]+[1]+board[i+1:], -1), i)
               for i in range(9) if board[i]==0)[1]

def print_board(board):
    s = {1:'X', -1:'O', 0:' '}
    for i in range(0,9,3):
        print(f"{s[board[i]]}|{s[board[i+1]]}|{s[board[i+2]]}")
        if i<6: print("-----")

board=[0]*9; player=1
while True:
    print_board(board)
    res = check_win(board)
    if res is not None:
        print("X wins!" if res==1 else "O wins!" if res==-1 else "Tie!")
        break
    if player==1:
        print("AI thinking...")
        board[best_move(board)] = 1
    else:
        move=int(input("Move (0-8): "))
        if 0<=move<=8 and board[move]==0: board[move]=-1
        else: print("Invalid"); continue
    player*=-1