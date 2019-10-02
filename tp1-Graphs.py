import queue
from Enviroment import Container
from Node import Node
import heapq
import time
import sys

world = None
init_node = None


# def h(node):
#     global world
#     count = 0
#     price = 0
#     for i in range(0, world.rows):
#         for j in range(0, world.columns):
#             if node.matrix_state[i][j] != world.final_config[i][j]:
#                 count += 1
#                 price += world.key_values[node.matrix_state[i][j]]
#     return count, price


# def a_star(world):
#     global init_node
#
#     init_node = Node(world.initial_config, 0, 0, 0, None)
#     init_node.heuristic = h(init_node)
#     idx = world.set_index(init_node.matrix_state)
#     frontier = queue.PriorityQueue()
#
#     frontier.put((init_node.cost + init_node.heuristic[0] * init_node.heuristic[1], init_node))
#
#     explored = {}
#     visited = {}
#     while frontier:
#         node = frontier.get_nowait()[1]
#         if node.matrix_state == world.final_config:
#             return node
#
#         explored[node.map] = node
#         successor = expand_(node, idx, visited)
#
#         for child in successor:
#             if child.map not in explored:
#                     frontier.put((child.cost+child.heuristic[0]*child.heuristic[1], child))
#                     visited[child.map] = child
#



def dijkstra(world):
    global init_node

    init_node = Node(world.initial_config, 0, 0, None)
    idx = world.set_index(init_node.matrix_state)
    frontier = queue.PriorityQueue()

    frontier.put((init_node.cost, init_node))

    cost_now = {}
    explored = {}
    visited = {}

    cost_now[init_node.map] = 0
    while frontier:
        node = frontier.get()[1]
        if node.matrix_state == world.final_config:
            return node, cost_now

        explored[node.map] = node
        successor = expand(node, idx, cost_now, visited)

        for child in successor:
            if child.map not in explored:
                new_cost = cost_now[node.map] + child.edge_cost
                if child.map not in cost_now or new_cost < cost_now[child.map]:
                    cost_now[child.map] = new_cost
                    frontier.put((child.cost, child))
                    visited[child.map] = child


def expand(node, indices, cost_now, visited):
    children = []
    for idx in indices:
        for possible_move in range(1, 3):
            state = node.matrix_state
            movement = move(state, possible_move, idx)
            if movement is not None:
                # flatten = lambda l: [item for sublist in l for item in sublist]
                state_ = getList(movement[0])
                # map_ = ''.join(str(e) for e in state_)
                map_ = ''.join(map(str, state_))
                if map_ in visited:
                    a = cost_now[map_]
                    if a > node.cost + movement[1]:
                        new_node = visited[map_]
                        new_node.cost = node.cost + movement[1]
                        cost_now[map_] = new_node.cost
                        new_node.parent = node
                        children.append(new_node)
                else:
                    new_node = (Node(movement[0], node.cost + movement[1], movement[1], node))
                    children.append(new_node)
    return children


def getList(l):
    return [item for sublist in l for item in sublist]

# def expand_(node, indices, visited):
#     children = []
#     for idx in indices:
#         for possible_move in range(1, 5):
#             state = node.matrix_state
#             movement = move(state, possible_move, idx)
#             if movement is not None:
#                 new_node = (Node(movement[0], node.cost + movement[1], movement[1], 0, node))
#                 new_node.heuristic = h(new_node)
#                 children.append(new_node)
#     return children


def move(state, position, out):
    global world

    new_state = [i[:] for i in state]
    idx = out
    row, col = idx[0], idx[1]

    # if position == 1:  # Up
    #     if idx is None:
    #         raise Exception('Should you be looking at this exception?')
    #     if (row - 1) < 0:
    #         return None
    #     else:
    #         temp = new_state[row - 1][col]
    #         new_state[row - 1][col] = new_state[row][col]
    #         new_state[row][col] = temp
    #         cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row - 1][col]]
    #     return new_state, cost

    if position == 1:  # Down
        if idx is None:
            raise Exception('Should you be looking at this exception?')
        if (row + 1) > (world.rows - 1):
            return None
        else:
            temp = new_state[row + 1][col]
            new_state[row + 1][col] = new_state[row][col]
            new_state[row][col] = temp
            cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row + 1][col]]
            return new_state, cost

    # if position == 3:  # Left
    #     if idx is None:
    #         raise Exception('Should you be looking at this exception?')
    #     if (col - 1) < 0:
    #         return None
    #     else:
    #         temp = new_state[row][col - 1]
    #         new_state[row][col - 1] = new_state[row][col]
    #         new_state[row][col] = temp
    #         cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row][col - 1]]
    #         return new_state, cost

    if position == 2:  # Right
        if idx is None:
            raise Exception('Should you be looking at this exception?')
        if (col + 1) > world.columns - 1:
            return None
        else:
            temp = new_state[row][col + 1]
            new_state[row][col + 1] = new_state[row][col]
            new_state[row][col] = temp
            cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row][col + 1]]
            return new_state, cost


# def record_cost(node):
#     global init_node
#     cost = 0
#     current_node = node
#     while init_node.state != current_node.state:
#         cost += node.cost
#         current_node = current_node.parent
#     return cost
def record_cost(node, cost_dict=None):
    cost = 0
    current_node = node
    while init_node.state != current_node.state:
        cost += node.cost
        # try:
        #     cost += cost_dict[current_node.map]
        # except:
        #     cost += current_node.edge_cost
        # print('Node ', current_node.map, ' Cost: ', current_node.edge_cost, '- Partial Cost: ' + str(cost))
        current_node = current_node.parent
        # print('Node ', current_node.map, ' Cost: ', current_node.cost, '- Partial Cost: ' + str(cost))
    # print('Node ', current_node.map, ' Cost: ', current_node.cost, '- Partial Cost: ' + str(cost))
    # print('\n')
    return cost

def main():
    init = time.time()
    global world
    file = sys.argv[1]
    # file = str('entrada_1')
    world = Container(str(file))
    node, cost_now = dijkstra(world)
    # node = a_star(world)
    cost = node.cost
    # cost = record_cost(node)
    final = time.time()
    # print(len(cost_now))
    print(cost, 'time: ' + str(round(final - init, 4)) + ' s')


if __name__ == '__main__':
    main()