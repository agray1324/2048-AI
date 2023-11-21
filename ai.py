from game import *


def showBoard():
    global board
    for row in board:
        s = ""
        for item in row:
            s += str(item)
            for i in range(6-len(str(item))):
                s+=" "
        print(s)
    print()
def move(nesw):
    global board
    match(nesw):
        case 'n':
            newboard = move_up(board)
        case 'e':
            newboard = move_right(board)
        case 's':
            newboard = move_down(board)
        case 'w':
            newboard = move_left(board)
    if(newboard!=board):
        #print(newboard, board)
        add_random_tile(newboard)
        board = newboard
    

def getNextStates(board):
    states = []
    states.append(move_up(board))
    states.append(move_right(board))
    states.append(move_down(board))
    states.append(move_left(board))
    return states

def score(state):
    score = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            score += state[i][j]/(i+j+1)
    return score

def getScoresAndNextStates(board):
    states = getNextStates(board)
    scores = []
    for state in states:
        scores.append(score(state))
    return scores, states



def recursive(board, depth):
    scores, states = getScoresAndNextStates(board)
    moves = ['n', 'e', 's', 'w']
    if(depth == 0):
        return moves[scores.index(max(scores))], max(scores)
    else:
        rec_scores = []
        rec_scores2 = []
        rec_scores4 = []
        trig = False
        for state in states:
            if state == board:
                score = 0
                trig = True
            else:
                states2, states4 = getAllInsertStates(state)
                for s in states2:
                    move, score = recursive(s, depth-1)
                    rec_scores2.append(score)
                for s in states4:
                    move, score = recursive(s, depth-1)
                    rec_scores4.append(score)
                score = 0.9 * (sum(rec_scores2)/len(rec_scores2)) + 0.1 * (sum(rec_scores4)/len(rec_scores4))
            rec_scores.append(score)
        return moves[rec_scores.index(max(rec_scores))], max(rec_scores)

def getMove(depth = 5):
    global board
    return recursive(board, depth)


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
                move(newMove)
                for row in board:
                    m2 = max(row)
                    if(m2 > m):
                        m = m2
            maxes.append(m)
        print("max: ", max(maxes))
        print("average: ",sum(maxes)/len(maxes))

def singleTest(depth):
    global board
    board = initialize_board()
    while not is_game_over(board):
        newMove, predScore = getMove(depth)
        move(newMove)
        showBoard()

singleTest(2)