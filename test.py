from Enviroment import *
from Node import Node

goal_state = list()
goal_node = Node
initial_state = list()
board_length = 0
board_side = 0
nodes_to_expand = 0
max_depth = 0
moves = list()
costs = list()
depth = 0


def expand(node):
    """
        expand: Implement the expansion for search strategies algorithms

            input: The current node that shal be expanded
            output: The children nodes expanded from the father node
    """

    global nodes_to_expand
    nodes_to_expand += 1

    children = list()

    for possible_move in range(1, 5):
        children.append((Node(move(node.state, possible_move), node, possible_move, node.depth + 1, node.cost + 1, 0)))

    children = [child for child in children if child.state]

    return children


def move(state, position):
    new_state = state[:]

    index = new_state.index(0)

    if position == 1:  # Up

        if index not in range(0, board_side):

            temp = new_state[index - board_side]
            new_state[index - board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 2:  # Down

        if index not in range(board_length - board_side, board_length):

            temp = new_state[index + board_side]
            new_state[index + board_side] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 3:  # Left

        if index not in range(0, board_length, board_side):

            temp = new_state[index - 1]
            new_state[index - 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None

    if position == 4:  # Right

        if index not in range(board_side - 1, board_length, board_side):

            temp = new_state[index + 1]
            new_state[index + 1] = new_state[index]
            new_state[index] = temp

            return new_state
        else:
            return None


def A_star(start_state):
    """
        a_star: Implements the A-star search

            A-star search (a_star)

            A-star search (a_star) is a computer algorithm that is widely used in pathfinding and graph traversal,
            which is the process of finding a path between multiple points, called "nodes".
            It enjoys widespread use due to its performance and accuracy.
        input: Start state or initial state of the 8 puzzle game
    """
    global goal_node, max_depth, goal_state


def main():
    global initial_state, goal_state, board_side, board_length

    var = Container('entrada_1')
    initial_state = var.start_state
    goal_state = var.final_state
    board_length = var.board_len
    board_side = var.board_side