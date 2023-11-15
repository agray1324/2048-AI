# taken from https://medium.com/@sarahisdevs/2048-game-in-python-2c10695a8d27
# modified to use kb listeners

import random
from pynput import keyboard

def initialize_board():
    board = [[0] * 4 for _ in range(4)]
    add_random_tile(board)
    return board

def add_random_tile(board):
    empty_cells = [(i, j) for i in range(4) for j in range(4) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def display_board(board):
    for row in board:
        print(" ".join(str(cell) if cell != 0 else '.' for cell in row))
    print()

def merge_tiles(row):
    new_row = [0] * 4
    index = 0
    for tile in row:
        if tile != 0:
            if new_row[index] == 0:
                new_row[index] = tile
            elif new_row[index] == tile:
                new_row[index] *= 2
                index += 1
            else:
                index += 1
                new_row[index] = tile
    return new_row

def transpose_board(board):
    return [list(row) for row in zip(*board)]

def move_left(board):
    new_board = []
    for row in board:
        new_row = merge_tiles(row)
        new_board.append(new_row)
    return new_board

def move_right(board):
    reversed_board = [row[::-1] for row in board]
    new_board = []
    for row in reversed_board:
        new_row = merge_tiles(row)
        new_board.append(new_row[::-1])
    return new_board

def move_up(board):
    transposed_board = transpose_board(board)
    new_board = move_left(transposed_board)
    return transpose_board(new_board)

def move_down(board):
    transposed_board = transpose_board(board)
    new_board = move_right(transposed_board)
    return transpose_board(new_board)

def is_game_over(board):
    for row in board:
        if 0 in row:
            return False
        for i in range(3):
            if row[i] == row[i + 1]:
                return False
    return True

move = None

def on_press(key):
    global move
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'w' or k == 'up':
        move = 'W'
    elif k == 's' or k == 'down':
        move = 'S'
    elif k == 'a' or k == 'left':
        move = 'A'
    elif k == 'd' or k == 'right':
        move = 'D'
    else:
        print('Please use either wasd or arrow keys.') 

	

def main():
    board = initialize_board()
    listener = keyboard.Listener(on_press=on_press)
    listener.start()  # start to listen on a separate thread	

    while True:
        display_board(board)
        if is_game_over(board):
            print("Game Over")
            break
        global move
        move = None

        while move not in ['W', 'A', 'S', 'D']:
            pass

        if move == 'W':
            board = move_up(board)
            add_random_tile(board)
        elif move == 'A':
            board = move_left(board)
            add_random_tile(board)
        elif move == 'S':
            board = move_down(board)
            add_random_tile(board)
        elif move == 'D':
            board = move_right(board)
            add_random_tile(board)

if __name__ == "__main__":
    main()