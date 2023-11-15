import pygame
import math

pygame.init()
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()
running = True

size = 4

font = pygame.font.Font('freesansbold.ttf', 32)


while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame

    colors = ["#eee4da", "#ede0c8", "#f2b179", "#f59563", "#f67c5f", "#f65e3b", "#edcf72", "#edcc61", "#edc850", "#edc53f", "#edc22e"]
    screen.fill("#776e65")

    board = [
        [0, 0, 2, 0],
        [0, 1024, 4, 0],
        [2, 0, 8, 0],
        [512, 256, 128, 64]
    ]

    # RENDER YOUR GAME HERE
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] != 0:
                pygame.draw.rect(screen, colors[int(math.log2(board[row][col])) - 1], pygame.Rect(col*500/size, row*500/size, 500/size, 500/size))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60

pygame.quit()