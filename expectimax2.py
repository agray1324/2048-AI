from ai import *
import sys
import time
import random
    
def recursive(board, depth):
    states, scores = getScoresAndNextLegalStates(board)
    moves = getNextLegalMoves(board)
    if(moves == []):
        return "", -1000000000
    if(depth == 0):
        #print(board)
        #print(states)
        return moves[scores.index(max(scores))], max(scores)
    else:
        rec_scores = []
        rec_scores2 = []
        rec_scores4 = []
        trig = False
        for state in states:
            #print(state, board)
            if state == board:
                score = 0
                trig = True
            else:
                states2, states4 = getAllInsertStates(state)
                l = len(states2)
                if(l != 0):   
                    numExansion = min(l, depth, 4)
                    #print(numExansion)
                    if(l == numExansion):
                        statesExpanded = range(l)
                    else:
                        statesExpanded = random.sample(range(l), numExansion)
                    #print(l, depth, 4, statesExpanded)
                    #print("states expanded: ", statesExpanded)
                    for s in statesExpanded:
                        move, score = recursive(states2[s], depth-1)
                        rec_scores2.append(score)
                        move, score = recursive(states4[s], depth-1)
                        rec_scores4.append(score)
                    #print(rec_scores2)
                    score = 0.9 * (sum(rec_scores2)/len(rec_scores2)) + 0.1 * (sum(rec_scores4)/len(rec_scores4))
            rec_scores.append(score)
        return moves[rec_scores.index(max(rec_scores))], max(rec_scores)

def getMove(depth = 8, end = False):
    global board
    move, score = recursive(board, depth)
    #print(move, score)
    return move, score


def depthAnalysis(minimum = 1, maximum = 6):
    global board
    for d in range(minimum, maximum):
        print("depth: ", d)
        maxes = []
        iter = 10
        for i in range(iter):
            #print(i/iter)
            board = initialize_board()
            m = 0
            while not is_game_over(board):
                newMove, predScore = getMove(d)
                board = move(board, newMove)
                for row in board:
                    m2 = max(row)
                    if(m2 > m):
                        m = m2
            maxes.append(m)
        print("max: ", max(maxes))
        print("average: ",sum(maxes)/len(maxes))

def timedSearch(seconds):
    global board
    board = initialize_board()
    while not is_game_over(board):
        end = time.time() + seconds
        best_move, best_score = -1, 0
        depth = 1
        while(time.time() < end):
            newMove, newScore = getMove(depth, end)
            if(newScore >= best_score):
                best_score = newScore
                best_move = newMove
            depth+=1
        board = move(board, best_move)
        #print(depth-1)
        #print(score(board))
        #showBoard(board)
    return max_function(board)

def getTimedMove(board, seconds):
    end = time.time() + seconds
    best_move, best_score = -1, 0
    depth = 1
    while(time.time() < end):
        newMove, newScore = getMove(depth, end)
        if(newScore >= best_score):
            best_score = newScore
            best_move = newMove
        depth+=1
    return best_move

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


def playGame(seconds):
    global board
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

        m = getTimedMove(board, seconds)
        board = move(board, m)
        display_board(modelToDisplay(board))
        time.sleep(0.5)

    pygame.quit()   
            

def singleTest(depth):
    global board
    board = initialize_board()
    while not is_game_over(board):
        newMove, predScore = getMove(depth)
        print(newMove)
        board = move(board, newMove)
        print(score(board))
        showBoard(board)
    return max_function(board)

iterations = 100
results = {2:0, 3:0,4:0,5:0,6:0,7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
for i in range(iterations):
    print(i)
    depth = singleTest(4)
    results[depth]+=1
    with open("result.txt", "w") as f:
        f.write(str(results))



