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

score_arr =[
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
    for i in range(len(state)):
        for j in range(len(state[0])):
            score += state[i][j]*(2**score_arr[i][j])
    return score

def getScoresAndNextStates(board):
    states = getNextStates(board)
    scores = []
    for state in states:
        scores.append(score(state))
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