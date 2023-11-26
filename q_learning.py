global board
from ai import *
import math
import time

def hash(state):
    s = ""
    for i in range(len(state)):
        s+= '-'.join(str(x) for x in state[i]) + '-'
        #for j in range(len(state)):
        #    s+= str(state[i][j]) + "-"
    return s

def max_function(state):
    maximum = 0
    for row in state:
        maximum2 = max(row)
        if(maximum2 > maximum):
            maximum = maximum2
    return maximum

def hash3(state):
    s = ""
    for row in state:
        for item in row:
            if item == 0:
                base = 0
            else:
                base = item
            s += str(base)
            s += "-"
    return s

def loadState(hash):
    vals = hash.split("-")
    size = int(len(vals)**0.5)
    state = []
    for i in range(size):
        inner = []
        for j in range(size):
            inner.append(int(vals[i*size+j]))
        state.append(inner)
    return state

def getMove(qh):
    if(random.uniform(0, 1) < rand):
        m = random.choice(list(qh.keys()))
    else:
        m = max(qh, key=qh.get)
    return m

def modelToDisplay(board):
    returnBoard = []
    for i in range(len(board)):
        inner = []
        for j in range(len(board[0])):
            if(board[i][j] != 0):
                inner.append(2**board[i][j])
            else:
                inner.append(0)
        returnBoard.append(inner)
    return returnBoard


def playGame(size = 4):
    board = initialize_board()

    pygame.init()
    screen = pygame.display.set_mode((500, 500))
    clock = pygame.time.Clock()

    font = pygame.font.Font('freesansbold.ttf', 32)

    display_board(modelToDisplay(board))
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
                    text = font.render(str(modelToDisplay(board)[row][col]), True, "black")
    
                    textRect = text.get_rect()
                    
                    textRect.center = (rect.centerx, rect.centery)

                    pygame.draw.rect(screen, colors[int(math.log2(board[row][col])) - 1], rect)
                    screen.blit(text, textRect)
            
        for i in range(1, size):
            pygame.draw.line(screen, "#776e65", (i*500/size, 0), (i*500/size, 500), 5)
            pygame.draw.line(screen, "#776e65", (0, i*500/size), (500, i*500/size), 5)


        pygame.display.flip()

        clock.tick(60)

        h = hash(board)
        if(not h in q):
            init_dict = {}
            for i in getNextLegalMoves(board):
                init_dict[i] = 0
            q[h] = init_dict
        m = getMove(q[h])
        board = move(board, m)
        display_board(modelToDisplay(board))
        time.sleep(0.5)

    pygame.quit()   

with open('q_values.txt', 'r') as file1:
    lines = file1.readlines()
    q = {}
    count = 0
    for line in lines:
        count += 1
        if(count % 100000 == 0):
            print(count)
        e = line.split(" ")
        h =  e[0]
        if(not h in q):
            init_dict = {}
            for i in getNextLegalMoves(loadState(h)):
                init_dict[i] = 0
            q[h] = init_dict
        i = 1
        while(i < len(e)):
            q[h][e[i]] = float(e[i+1])
            i += 2

pg = False
rand = 0
if(pg):
    playGame()

learning_rate = 0.2
rand = 0.1
iterations = 10000
batches = 10
writeBatches = 100
discount = 1
topLeftQuadrant = [[0,0],[0,1],[1,0],[1,1]]
for k in range(writeBatches):
    print("writeBatch: " + str(k))
    print("learning (wont lose lots of data if closed)")
    for j in range(batches):
        total = 0
        total_maxes = 0
        num_reached = {4 : 0, 5 : 0, 6 : 0, 7 : 0, 8: 0, 9 : 0, 10 : 0}
        print("batch " + str(j) + ":")
        for i in range(iterations):
            board = initialize_board()
            h = hash(board)
            m = ''
            if(not h in q):
                init_dict = {}
                for i in getNextLegalMoves(board):
                    init_dict[i] = 0
                q[h] = init_dict
            m = getMove(q[h])
            hashes = []
            moves = []
            while not is_game_over(board):#for num_moves in range(k):
                #if(not is_game_over(board)):
                old_board = board
                board = move(board, m)
                #moves.append(m)
                h2 = hash(board)
                if(not h2 in q):
                    init_dict = {}
                    for i in getNextLegalMoves(board):
                        init_dict[i] = 0
                    q[h2] = init_dict
                if(not is_game_over(board)):
                    m2 = getMove(q[h2])
                else:
                    m2 = 'end'
                    if(m2 not in q[h2].keys()):
                        q[h2][m2] = 0
                if(q[h][m] == 0):
                    q[h][m] = discount * q[h2][m2]
                else:
                    q[h][m] = (1-learning_rate) *q[h][m] +learning_rate*(discount * q[h2][m2])
                m = m2
                h = h2
            q[h]['end'] = score(board)
            
            #for row in board:
            #    maximum2 = max(row)
            #    if(maximum2 > maximum):
            #        maximum = maximum2
            #for h, m  in zip(hashes, moves):
            #    curr_val = q[h][m]
            #    q[h][m] = (1-learning_rate)*curr_val + (learning_rate) * maximum
            #total_maxes += maximum
            max_reached = max_function(board)
            total += max_reached
            if(max_reached in num_reached):
                num_reached[max_reached] += 1
            else:
                num_reached[max_reached] = 1
        print(total/iterations)
        print(num_reached)
    print("writing (don't close this or you may lose data)")
    with open("q_values.txt", "w") as f:
        for h in q.keys():
            write = False
            s = h
            for m in q[h].keys():
                i = q[h][m]
                s += " " + m + " " + str(i)
                if(i != 0):
                    write = True
            if(write):
                f.write(s)
                f.write("\n")