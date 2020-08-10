import math
# the state class contains methods for tic tac toe
import state as s
import random
import copy

class Node:
    def __init__(self, state, action = None, parent = None):
        self.wins = 0
        self.visit_count = 0
        self.state = state
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

def best_uct(node):
    # returns the child with the highest uct value
    values = [n.get_value() for n in node.children]
    return node.children[values.index(max(values))]

def traverse(node, player):
    # traverse the tree from the root node to a leaf node
    while node.children:
        node = best_uct(node)
        player = s.next_player(player)
    # check if node has a visit count and is not terminal
    if node.visit_count > 0 and (action_space := s.get_action_space(node.state)):
        # append a child for each available action
        for action in action_space:
            # get the new state each child has
            state, _, _ = s.move(node.state, action, player)
            node.children.append(Node(state, action, node))
        node = node.children[0]
    return node, player

def rollout(node, player):
    state = copy.deepcopy(node.state)
    won = s.check_won(state)
    while not won:
        action = s.get_action_space_sample(state)
        state, player, won = s.move(state, action, player)
    return won

def best_child(node):
    visit_counts = [n.visit_count for n in node.children]
    return node.children[visit_counts.index(max(visit_counts))]

def backpropagate(node, simulation_result, player):
    while node:
        node.visit_count += 1
        if player != simulation_result: node.wins += 1
        player = s.next_player(player)
        node = node.parent

def mcts(root, player, iterations):
    for _ in range(iterations):
        leaf, player = traverse(root, player)
        simulation_result = rollout(leaf, player)
        backpropagate(leaf, simulation_result, player)
    return best_child(root)

root = Node(s.init())

won = False
# Player 1 = 1; Player 2 = 2; Nothing = 0
player = random.randrange(3)
state = s.init()

node = root

while not won:
    node = mcts(node, player, 1000)
    # action = s.get_action_space_sample(state)
    action = node.action
    state, player, won = s.move(state, action, player)
    print(state)

print(won)