import math
# the state class contains methods for tic tac toe
import state as s
import random
import copy

class Node:
    def __init__(self, actions, action = None, parent = None):
        self.wins = 0
        self.visit_count = 0
        self.actions = actions
        self.parent = parent
        # action -> the action that lead to this node
        self.action = action
        self.children = []
    def get_value(self):
        if self.visit_count == 0: return math.inf
        exploitation = self.wins / self.visit_count
        exploration = math.sqrt(2) * math.sqrt(math.log(self.parent.visit_count) / self.visit_count)
        # returns the uct value
        return exploitation + exploration
    def is_leaf(self):
        return len(self.actions) != len(self.children)

def best_uct(node):
    values = [n.get_value() for n in node.children]
    return node.children[values.index(max(values))]

def traverse(node, player, state):
    while not node.is_leaf() and not s.check_won(state):
        node = best_uct(node)
        state, player, _ = s.move(state, node.action, player)
    if not s.check_won(state):
        unexpanded = set(node.actions) - set([n.action for n in node.children])
        action = random.choice(tuple(unexpanded))
        state, player, _ = s.move(state, action, player)
        child = Node(s.get_action_space(state), action, node)
        node.children.append(child)
        node = child
    return node, player, state

def rollout(node, player, state):
    won = s.check_won(state)
    while not won:
        action = s.get_action_space_sample(state)
        state, player, won = s.move(state, action, player)
    return won

def backpropagation(node, result, player):
    increase = s.next_player(result)
    while node:
        node.visit_count += 1
        if result != -1:
            node.wins += (increase == player) * 1
        player = s.next_player(player)
        node = node.parent

def best_child(node):
    visit_counts = [n.visit_count for n in node.children]
    return node.children[visit_counts.index(max(visit_counts))]

def mcts(root, player, state):
    state_copy = copy.deepcopy(state)
    for _ in range(1000):
        leaf, leaf_player, state_ = traverse(root, player, state_copy)
        result = rollout(leaf, leaf_player, state_)
        backpropagation(leaf, result, leaf_player)
    return best_child(root)

root = Node(s.get_action_space(s.init()))

for _ in range(10):
    won = False
    # Player 1 = 1; Player 2 = 2; Nothing = 0
    player = random.randrange(2) + 1
    state = s.init()

    node = root

    print(state)

    while not won:

        print(f"Player: {player}")

        best = mcts(node, player, state)

        if player == 1:
            node = best
        else:
            child_actions = [n.action for n in node.children]
            random_action = int(input("Field: "))
            node = node.children[child_actions.index(random_action)]

        action = node.action

        state, player, won = s.move(state, action, player)

        print(state)

    print(won)