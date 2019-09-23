import queue
from Enviroment import Container
from Node import Node
import heapq
import time

world = None
max_depth = 0
init_node = None
check_dict = {}

#
# def bfs(world):
#     global max_depth, init_node
#     resultado = []
#     open_list, closed_list = queue.Queue(), {}
#
#     node = Node(world.initial_config, None, None, 0, 0, 0)
#     init_node = node
#
#     open_list.put(node)
#
#     while open_list:
#
#         node = open_list.get()
#         if node.state == world.final_state:
#             resultado.append(node)
#             continue
#             # return node
#
#         closed_list[node.map] = node
#         # world.set_index(node.matrix_state)
#         idx = world.set_index(node.matrix_state)
#         # if idx is not None:
#
#         # for out_position in idx:
#         successor = expand(node, idx)
#         # for child in successor:
#         # print (child.matrix_state)
#         for child in successor:
#             if not child.map in closed_list:
#                 child.heuristic = euclidean(child)  # + child.cost
#                 # child.heuristic = MHD(child)  # + child.cost
#                 child.key = check(child)
#                 if child.depth > max_depth:
#                     max_depth += 1
#
#                 open_list.put(child)
#
#     return resultado
#
#
# def ids(world):
#     global max_depth, init_node
#     ids_max_depth = 10
#     closed_list, open_list = {}, queue.Queue()
#
#     node = Node(world.initial_config, None, None, 0, 0, 0)
#     open_list.put(node)
#
#     while ids_max_depth < float('inf'):
#         depth = 0
#
#         while True:
#
#             node = open_list.get()
#             closed_list[node.map] = node
#
#             if node.state == world.final_state:
#                 return node
#
#             elif depth == ids_max_depth:
#                 break
#
#             world.set_index(node.matrix_state)
#             idx = world.set_index(node.matrix_state)
#             # for out_position in idx:
#             successor = expand(node, idx)
#
#             for child in successor:
#                 if not child.map in closed_list:
#                     child.heuristic = euclidean(child)  # + child.cost
#                     # child.heuristic = MHD(child)  # + child.cost
#                     child.key = check(child)
#                     if child.depth > max_depth:
#                         max_depth += 1
#                     open_list.put(child)


def a_star(world):
    global max_depth, init_node, check_dict
    resultado = []
    open_list, closed_list = queue.PriorityQueue(), {}
    # open_list, closed_list = [], {}
    node = Node(world.initial_config, None, None, 0)
    init_node = node
    open_list.put((node.cost[0], node))

    # heapq.heappush(open_list, (node.cost, node.depth, node))
    while open_list:

        node = open_list.get()[1]
        # node = heapq.heappop(open_list)[2]

        if node.state == world.final_state:
            resultado.append(node)
            break
            # return node

        closed_list[node.map] = node
        check_dict[node.map] = node
        idx = world.set_index(node.matrix_state)
        successor = expand(node, idx)

        for child in successor:
            if not child.map in closed_list:
                check_dict[child.map] = child
                # print(child.heuristic, child.cost, child.depth, child.map)

                # heapq.heappush(open_list, (child.cost, node.depth, child))
                open_list.put((child.cost[0], child))

    return resultado


def check(node):
    global world
    value = 0
    result = list()
    l1 = node.matrix_state
    l2 = world.final_config

    for row in range(0, world.rows):
        for col in range(0, world.columns):
            if l1[row][col] != l2[row][col]:
                value += world.key_values[l1[row][col]]
    return value


def MHD(node):
    global world
    cost2goal_sum = 0
    goal_state = world.final_state

    if len(node.state) != len(goal_state):
        raise ValueError('List of different length!')

    # for i in range(len(node.state)):
    #     for j in range(i+1, len(node.state)):
    #         cost2goal_sum += (abs(world.key_values[node.state[i]] - world.key_values[node.state[j]]) +
    #                           abs(world.key_values[world.final_state[i]] - world.key_values[world.final_state[j]]))
    # #
    for i in range(len(goal_state)):
        for j in range(i + 1, len(goal_state)):
            cost2goal_sum += (abs(node.state[i] - node.state[j]) + abs(goal_state[i] - goal_state[j]))
    # node.heuristic = cost2goal_sum
    return cost2goal_sum


def euclidean(node):
    global world
    v1 = node.state
    v2 = world.final_state
    euclidian_distance = sum((p - q) ** 2 for p, q in zip(v1, v2)) ** .5
    # node.heuristic = euclidian_distance
    # print(euclidian_distance)
    return euclidian_distance


def matrix_map(matrix_state):
    if matrix_state:
        flatten = lambda l: [item for sublist in l for item in sublist]
        state = flatten(matrix_state)
        map = ''.join(str(e) for e in state)
    return map


def expand(node, out):
    global check_dict

    children = list()
    for p in out:
        for possible_move in range(1, 5):
            state = node.matrix_state
            movement = move(state, possible_move, p)
            if movement is not None:
                map_test = matrix_map(movement[0])
                if map_test in check_dict:
                    child_node = check_dict[map_test]
                    child_node.add_parent(node, movement[1])
                    children.append(child_node)
                else:
                    new_node = (Node(movement[0], node, possible_move, movement[1]))
                    children.append(new_node)
            else:
                pass
    #
    # children = [child for child in children if child.state]
    # unique_children = []
    # for child in children:
    #     if child not in unique_children:
    #         unique_children.append(child)

    # return unique_children
    return children


def move(state, position, out):
    global world

    new_state = [i[:] for i in state]

    # index = new_state.index(0)
    # idx = world.index
    idx = out
    row, col = idx[0], idx[1]

    if position == 1:  # Up
        if idx is None:
            raise Exception('Should you be looking at this exception?')
        if (row - 1) < 0:
            return None
        else:
            temp = new_state[row - 1][col]
            new_state[row - 1][col] = new_state[row][col]
            new_state[row][col] = temp
            cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row - 1][col]]
        return new_state, cost

    if position == 2:  # Down
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

    if position == 3:  # Left
        if idx is None:
            raise Exception('Should you be looking at this exception?')
        if (col - 1) < 0:
            return None
        else:
            temp = new_state[row][col - 1]
            new_state[row][col - 1] = new_state[row][col]
            new_state[row][col] = temp
            cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row][col - 1]]
            return new_state, cost

    if position == 4:  # Right
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


def record_cost(node):
    cost = 0
    current_node = node
    while init_node.state != current_node.state:
        cost += current_node.cost
        print('Node ', current_node.map, ' Cost: ', current_node.cost, '- Partial Cost: ' + str(cost))
        current_node = current_node.parent
        # print('Node ', current_node.map, ' Cost: ', current_node.cost, '- Partial Cost: ' + str(cost))
    print('Node ', current_node.map, ' Cost: ', current_node.cost, '- Partial Cost: ' + str(cost))
    print('\n')
    return cost


def main():
    init = time.time()
    global world
    world = Container('entrada_1')
    solver = a_star(world)
    # solver = bfs(world)
    # solver = ids(world)
    cost = float('inf')
    for results in solver:
        save = record_cost(results)
        if save < cost:
            cost = save
    final = time.time()
    print(cost, 'time: ' + str(round(final - init, 3)) + ' s')


if __name__ == '__main__':
    main()
