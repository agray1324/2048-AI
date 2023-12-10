from game import *


def showBoard(board):
    for row in board:
        s = ""
        for item in row:
            s += str(item)
            for i in range(6-len(str(item))):
                s+=" "
        print(s)
    print()
def move(board, nesw):
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
    return board
    

def getNextStates(board):
    states = []
    states.append(move_up(board))
    states.append(move_right(board))
    states.append(move_down(board))
    states.append(move_left(board))
    return states

def score2(state):
    score = 0
    zeroCount =0
    for i in range(len(state)):
        for j in range(len(state[0])):
            score += state[i][j]/((2**(i+1))*(2**(j+1)))
            if state[i][j] == 0:
                zeroCount+=1
    return score*(2**zeroCount)

score_arr = [[24,23,22,21,20],[15,16,17,18,19],[14,13,12,11,10],[5,6,7,8,9],[4,3,2,1,0]]

score_arr_4 =[
    [15, 14, 13, 12],
    [8, 9, 10, 11],
    [7, 6, 5, 4],
    [0, 1, 2, 3]
]

def max_function(state):
    maximum = 0
    for row in state:
        maximum2 = max(row)
        if(maximum2 > maximum):
            maximum = maximum2
    return maximum

def score(state):
    score = 0
    count = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            score += state[i][j]*(4**score_arr[i][j])
            if(state[i][j] == 0):
                count+=1
    return score*1.05**count

def expectiscore(state):
    score = 0
    count = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            score += state[i][j]*(4**score_arr[i][j])
            if(state[i][j] == 0):
                count+=1
    return score#*1.05**count

def score2(state):
    score = 0
    for i in range(len(state)):
        for j in range(len(state[0])):
            score += state[i][j]*(2**score_arr[i][j])
    return score

def getScoresAndNextStates(board, expecti = False):
    states = getNextStates(board)
    scores = []
    for state in states:
        if(not expecti):
            scores.append(score(state))
        else:
            scores.append(expectiscore(state))
    return scores, states

def getNextLegalMoves(board):
    states = getNextStates(board)
    r = []
    i = 0
    moves = ['n', 'e', 's', 'w']
    for state in states:
        if(board != state):
            r.append(moves[i])
        i+=1
    return r

def getScoresAndNextLegalStates(board):
    states = getNextStates(board)
    r = []
    i = 0
    scores = []
    for state in states:
        if(board != state):
            r.append(state)
            scores.append(expectiscore(state))
        i+=1
    return r, scores