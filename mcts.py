import math
import state as s
import copy
import numpy as np

class MCTS:
    def __init__(self):
        self.visit_counts = {}
        self.values = {}
        self.uct = {}

    def is_leaf(self, state):
        return state not in self.visit_counts

    def find_leaf(self, state, player):
        states = []
        actions = []
        cur_state = state
        cur_player = player
        value = None
        while not self.is_leaf(cur_state):
            states.append(cur_state)
            uct_values = self.uct[cur_state]
            invalid_actions = set(range(9)) - set(s.get_action_space(cur_state))
            for invalid_action in invalid_actions:
                uct_values[invalid_action] = -math.inf
            action = np.argmax(uct_values)
            actions.append(action)
            cur_state, cur_player, won = s.move(cur_state, action, cur_player)
            if won:
                value = 0 if won == -1 else -1

        return cur_state, cur_player, states, actions, value

    def expand(self, state):
        self.visit_counts[state] = [0] * 9
        self.values[state] = [0] * 9
        self.uct[state] = [math.inf] * 9

    def rollout(self, state, player):
        cur_player = player
        while True:
            action = s.get_action_space_sample(state)
            state, cur_player, won = s.move(state, action, cur_player)
            if won:
                if won == player: return 1
                elif won == -1: return 0
                else: return -1

    def backpropagate(self, states, actions, value):
        cur_value = -value
        for state, action in zip(reversed(states), reversed(actions)):
            self.visit_counts[state][action] += 1
            self.values[state][action] += cur_value

            visit_counts = self.visit_counts[state]
            values = self.values[state]
            parent_visit_count = sum(visit_counts)
            self.uct[state] = [value / visit_count + 
                               math.sqrt(2) * math.sqrt(math.log(parent_visit_count) / visit_count)
                               if visit_count > 0 else math.inf for value, visit_count in zip(values, visit_counts)]

            cur_value = -cur_value

    def get_policy(self, state):
        visit_counts = self.visit_counts[state]
        return np.argmax(visit_counts)

    def monte_carlo_tree_search(self, state, player, iterations):
        for _ in range(iterations):
            leaf_state, leaf_player, states, actions, value = self.find_leaf(state, player)
            if value is None:
                self.expand(leaf_state)
                value = self.rollout(leaf_state, leaf_player)
            self.backpropagate(states, actions, value)
        return self.get_policy(state)

mcts = MCTS()

results = {-1: 0, 1: 0, 2: 0}

for i in range(100):

    won = False
    player = s.get_random_player()
    state = s.init()

    while not won:

        # print(f"Player: {player}")

        action = mcts.monte_carlo_tree_search(state, player, 100)
        state, player, won = s.move(state, action, player)

        # print(s.decode(state))

    print(i, won)
    results[won] += 1

print(results)