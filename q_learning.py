global board
from ai import *
import math

def hash(state):
    s = ""
    for row in state:
        for item in row:
            if item == 0:
                base = 0
            else:
                base = int(math.log(item, 2))
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
            inner.append(vals[i*size+j])
        state.append(inner)
    return state

with open('q_values.txt', 'r') as file1:
    lines = file1.readlines()
    q = {}
    for line in lines:
        e = line.split(" ")
        if(not e[0] in q):
            init_dict = {}
            for i in getNextLegalMoves(loadState(e[0])):
                init_dict[i] = 0
            q[e[0]] = init_dict
        q[e[0]][e[1]] = float(e[2])
learning_rate = 0.1
rand = 0.25
iter = 1000
total_maxes = 0
for i in range(iter):
    board = initialize_board()
    h = hash(board)
    hashes = []
    moves = []
    while not is_game_over(board):
        hashes.append(h)
        m = ''
        if(not h in q):
            init_dict = {}
            for i in getNextLegalMoves(board):
                init_dict[i] = 0
            q[h] = init_dict
        if(random.uniform(0, 1) < rand):
            m = random.choice(list(q[h].keys()))
        else:
            m = max(q[h], key=q[h].get)
        board = move(board, m)
        moves.append(m)
        h = hash(board)
    maximum = 0
    for row in board:
        maximum2 = max(row)
        if(maximum2 > maximum):
            maximum = maximum2
    for h, m  in zip(hashes, moves):
        curr_val = q[h][m]
        q[h][m] = (1-learning_rate)*curr_val + (learning_rate) * maximum
    total_maxes += maximum
print(total_maxes/iter)
with open("q_values.txt", "w") as f:
    for h in q.keys():
        for m in q[h].keys():
            f.write(h + " " + m + " " + str(q[h][m]) + "\n")