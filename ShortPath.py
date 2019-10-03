import queue
from Enviroment import Container
from Node import Node
import time
import sys
import os

world = None
init_node = None


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
            try:
                explored[child.map]
            # if child.map not in explored:
            except:
                new_cost = cost_now[node.map] + child.edge_cost
                if child.map not in cost_now or new_cost < cost_now[child.map]:
                    cost_now[child.map] = new_cost
                    frontier.put((child.cost, child))
                    visited[child.map] = child


def expand(node, indices, cost_now, visited):
    children = []
    for idx in indices:
        for possible_move in [1, 2]:
            movement = move(node.matrix_state, possible_move, idx)
            if movement is not None:
                state_ = getList(movement[0])
                map_ = ''.join(map(str, state_))
                try:
                    visited[map_]
                # if map_ in visited:
                    a = cost_now[map_]
                    b = node.cost + movement[1]
                    if a > b:
                        new_node = visited[map_]
                        new_node.cost = b
                        cost_now[map_] = new_node.cost
                        new_node.parent = node
                        children.append(new_node)
                except:
                    new_node = (Node(movement[0], node.cost + movement[1], movement[1], node))
                    children.append(new_node)
    # print(len(children))
    return children


def getList(l):
    return [item for sublist in l for item in sublist]


def move(state, position, out):
    global world

    new_state = [i[:] for i in state]
    row, col = out[0], out[1]

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
        if (col + 1) > world.columns - 1:
            return None
        else:
            temp = new_state[row][col + 1]
            new_state[row][col + 1] = new_state[row][col]
            new_state[row][col] = temp
            cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row][col + 1]]
            return new_state, cost


def write_output(output, file):
    with open(str(file), 'w') as f:
        f.write(str(output) + '\n')
        f.write('\n')
    f.close()


def main():
    init = time.time()
    global world
    try:
        input = sys.argv[1]
        output = os.getcwd() + (str('/out/output_') + input)
        # output = os.getcwd() + sys.argv[2]
    except:
        input = str('entrada_4')
        output = os.getcwd() + (str('/out/output_') + input)
    world = Container(str(input))
    node, cost_now = dijkstra(world)
    cost = node.cost
    # write_output(cost, output)
    final = time.time()

    # print(cost, 'time: ' + str(round(final - init, 4)) + ' s')


if __name__ == '__main__':
    main()