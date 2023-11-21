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
    zeroCount =0
    for i in range(len(state)):
        for j in range(len(state[0])):
            score += state[i][j]/((2**(i+1))*(2**(j+1)))
            if state[i][j] == 0:
                zeroCount+=1
    return score*(2**zeroCount)

def getScoresAndNextStates(board):
    states = getNextStates(board)
    scores = []
    for state in states:
        scores.append(score(state))
    return scores, states