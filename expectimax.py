from ai import *

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
        print(score(board))
        showBoard()

singleTest(3)