import os
import time

def write_move(player, row, col):
    filename = f"{player}moves.txt"
    with open(filename, "w") as file:
        file.write(f"{player}{row+1}{chr(col+97)}\n")

def read_opponent_move(player):
    opponent = 'x' if player == 'o' else 'o'
    filename = f"{opponent}moves.txt"
    while not os.path.exists(filename):
        time.sleep(0.5)
    with open(filename, "r") as file:
        move = file.readline().strip()
    os.remove(filename)
    try:
        row = int(move[1]) - 1
        col = ord(move[2]) - 97
        return row, col
    except (IndexError, ValueError):
        print("Invalid move format from opponent. Waiting for a valid move...")
        return read_opponent_move(player)


def print_board(board):
    n = len(board)
    for i in range(n):
        row_str = ''
        for j in range(n):
            cell = board[i][j]
            row_str += f' {cell if cell != " " else "-"} '
            if j < n -1:
                row_str += '|'
        print(row_str)
        if i < n -1:
            print('-' * (n * 4 - 1))
    print()
