from ai import *
import sys
import time

def Player(board, depth, a, b, end = False):
    if end:
        if time.time() > end:
            return -1, 0
    scores, states = getScoresAndNextStates(board)
    moves = getNextLegalMoves(board)
    directions = ['n', 'e', 's', 'w']
    if((depth == 0) or (moves == [])):
        s = score(board)
        return s, ""
    else:
        rec_scores = []
        s = -1 * sys.maxsize
        bestAction = -1
        for move in moves:
            state = states[directions.index(move)]
            newScore, newAction = boardMove(state, depth, a, b, end)
            if(newScore > s):
                s = newScore
                bestAction = move
                a = max(a, s)
                if end:
                    if time.time() > end:
                        return -1, 0
                if(s > b):
                    return s, bestAction
        if end:
            if time.time() > end:
                return -1, 0
        return s, bestAction
        """if state == board:
            score = 0
        else:
            states2, states4 = getAllInsertStates(state)
            for s in states2:
                move, score = recursive(s, depth-1)
                rec_scores2.append(score)
            for s in states4:
                move, score = recursive(s, depth-1)
                rec_scores4.append(score)
            score = min(min(rec_scores2),min(rec_scores4))
        rec_scores.append(score)
    return moves[rec_scores.index(max(rec_scores))], max(rec_scores)"""
    
def boardMove(state, depth, a, b, end):
    states2, states4 = getAllInsertStates(state)
    states = states2 + states4
    s = sys.maxsize
    for state in states:
        newScore, newAction = Player(state, depth-1, a, b, end)
        if(newScore < s):
            s = newScore
            b = min(b, s)
            if end:
                if time.time() > end:
                    return -1, 0
            if (s < a):
                return s, ""
    if end:
        if time.time() > end:
            return -1, 0
    return s, ""

def getMove(depth = 5, end = False):
    global board
    score, move = Player(board, depth, -1*sys.maxsize, sys.maxsize, end)
    print(move, score)
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
        print(score(board))
        showBoard(board)
    return max_function(board)
            

def singleTest(depth):
    global board
    board = initialize_board()
    while not is_game_over(board):
        newMove, predScore = getMove(depth)
        board = move(board, newMove)
        print(score(board))
        showBoard(board)
    return max_function(board)

iterations = 100
results = {2:0, 3:0,4:0,5:0,6:0,7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0, 16:0}
for i in range(iterations):
    results[timedSearch(1)]+=1
    print(results)

