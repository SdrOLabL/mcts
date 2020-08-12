import math
# the state class contains methods for tic tac toe
import state as s
import random
import copy

class Node:
    def __init__(self, state, actions, action = None, parent = None):
        self.wins = 0
        self.visit_count = 0
        self.state = state
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

def traverse(node, player):
    while not node.is_leaf() and not s.check_won(node.state):
        node = best_uct(node)
        player = s.next_player(player)
    if not s.check_won(node.state):
        unexpanded = set(node.actions) - set([n.action for n in node.children])
        action = random.choice(tuple(unexpanded))
        state, player, _ = s.move(node.state, action, player)
        child = Node(state, s.get_action_space(state), action, node)
        node.children.append(child)
        node = child
    return node, player

def rollout(node, player):
    state = copy.deepcopy(node.state)
    won = s.check_won(state)
    while not won:
        action = s.get_action_space_sample(state)
        state, player, won = s.move(state, action, player)
    return won

def backpropagation(node, result):
    while node:
        node.visit_count += 1
        if result == 1: node.wins += 1
        node = node.parent

def best_child(node):
    visit_counts = [n.visit_count for n in node.children]
    return node.children[visit_counts.index(max(visit_counts))]

def mcts(root, player):
    for _ in range(1000):
        leaf, leaf_player = traverse(root, player)
        result = rollout(leaf, leaf_player)
        backpropagation(leaf, result)
    return best_child(root)

root = Node(s.init(), s.get_action_space(s.init()))

for i in range(10):

    won = False
    # Player 1 = 1; Player 2 = 2; Nothing = 0
    player = 1
    state = s.init()

    node = root

    print(state)

    while not won:

        print(f"Player: {player}")

        best = mcts(node, player)

        if player == 1:
            node = best
        else:
            child_actions = [n.action for n in node.children]
            print(f"Possible Actions: {sorted(child_actions)}")
            random_action = int(input("Action: "))
            node = node.children[child_actions.index(random_action)]

        action = node.action

        state, player, won = s.move(state, action, player)

        print(state)

    print(won)