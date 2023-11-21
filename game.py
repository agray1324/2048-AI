# taken from https://medium.com/@sarahisdevs/2048-game-in-python-2c10695a8d27
# modified to use kb listeners

import random
from pynput import keyboard
import pygame
import math

size = 4

def initialize_board(s = 4):
    global size
    size = s
    board = [[0] * size for _ in range(size)]
    add_random_tile(board)
    #print(board)
    return board

def add_random_tile(board):
    empty_cells = [(i, j) for i in range(size) for j in range(size) if board[i][j] == 0]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = 2 if random.random() < 0.9 else 4

def display_board(board):
    for row in board:
        print(" ".join(str(cell) if cell != 0 else '.' for cell in row))
    print()

def merge_tiles(row):
    new_row = [0] * size
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
        for i in range(size-1):
            if row[i] == row[i + 1]:
                return False
    
    for row in range(size - 1):
        for i in range(size):
            if board[row][i] == board[row + 1][i]:
                return False
    return True

def main():
    board = initialize_board()
    global size

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 32)

    display_board(board)
    running = True

    while running:
        if is_game_over(board):
            print("Game Over")
            break

        colors = ["#eee4da", "#ede0c8", "#f2b179", "#f59563", "#f67c5f", "#f65e3b", "#edcf72", "#edcc61", "#edc850", "#edc53f", "#edc22e"]
        screen.fill("#bbada0")

        for row in range(len(board)):
            for col in range(len(board[row])):
                if board[row][col] != 0:
                    rect = pygame.Rect(col*500/size, row*500/size, 500/size, 500/size)
                    text = font.render(str(board[row][col]), True, "black")
    
                    textRect = text.get_rect()
                    
                    textRect.center = (rect.centerx, rect.centery)

                    pygame.draw.rect(screen, colors[int(math.log2(board[row][col])) - 1], rect)
                    screen.blit(text, textRect)
            
        for i in range(1, size):
            pygame.draw.line(screen, "#776e65", (i*500/size, 0), (i*500/size, 500), 5)
            pygame.draw.line(screen, "#776e65", (0, i*500/size), (500, i*500/size), 5)


        pygame.display.flip()

        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    board = move_up(board)
                    add_random_tile(board)
                    display_board(board)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    board = move_left(board)
                    add_random_tile(board)
                    display_board(board)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    board = move_down(board)
                    add_random_tile(board)
                    display_board(board)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    board = move_right(board)
                    add_random_tile(board)
                    display_board(board)
            elif event.type == pygame.QUIT:
                running = False

    pygame.quit()   

if __name__ == "__main__":
    main()