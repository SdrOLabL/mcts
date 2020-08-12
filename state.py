import numpy as np
import random
import copy

# returns new board
def init():
    return np.zeros((3, 3), dtype=int)

def move(state, action, player):
    state = copy.deepcopy(state)
    x = action % state.shape[0]
    y = action // state.shape[0]
    if state[y][x] != 0: print("wrong move")
    state[y][x] = player
    player = next_player(player)
    won = check_won(state)
    return state, player, won

def next_player(player):
    return 1 + 1 * (player == 1)

# returns legal actions in given state
def get_action_space(state):
    flat_list = [item for row in state for item in row]
    return [i for i, item in enumerate(flat_list) if item == 0]

# returns random legal action
def get_action_space_sample(state):
    return random.choice(get_action_space(state))

def check_won(state):
    diagonal1 = list(np.diag(np.fliplr(state)))
    diagonal2 = list(np.diag(state))
    if diagonal1.count(diagonal1[0]) == len(diagonal1) and diagonal1[0] != 0: return diagonal1[0]
    if diagonal2.count(diagonal2[0]) == len(diagonal2) and diagonal2[0] != 0: return diagonal2[0]
    for row1, row2 in zip(state, state.T):
        if list(row1).count(row1[0]) == len(row1) and row1[0] != 0: return row1[0]
        if list(row2).count(row2[0]) == len(row2) and row2[0] != 0: return row2[0]
    if 0 not in state: return -1