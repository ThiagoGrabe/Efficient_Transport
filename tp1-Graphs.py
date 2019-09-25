import queue
from Enviroment import Container
from Node import Node
import heapq
import time
import sys

init_node = None


def dijkstra(world):
    global init_node

    init_node = Node(world.initial_config, 0, 0, None)
    frontier = queue.PriorityQueue()

    frontier.put((init_node.cost, init_node))

    cost_now = {}
    explored = {}
    visited = {}
    edge_cost = {}

    cost_now[init_node.map] = 0
    i = 0
    while frontier:
        i += 1
        t5 =time.time()
        node = frontier.get_nowait()[1]
        # print(time.time() - t5)

        if node.matrix_state == world.final_config:
            # print(i)
            return node, cost_now, edge_cost

        explored[node.map] = node
        t0 = time.time()
        idx = world.set_index(node.matrix_state)
        t1 = time.time()
        # print(t1 - t0)
        successor = expand(node, idx, cost_now, edge_cost, visited, explored)
        # print(time.time() - t1)

        t2 = time.time()
        for child in successor:
            if child.map not in explored:
                new_cost = cost_now[node.map] + child.edge_cost
                if child.map not in cost_now or new_cost < cost_now[child.map]:
                    cost_now[child.map] = new_cost
                    frontier.put((new_cost, child))
                    visited[child.map] = child


def expand(node, indices, cost_now, edge_cost, visited, explored):
    children = []
    for idx in indices:
        for possible_move in range(1, 5):
            state = node.matrix_state
            movement = move(state, possible_move, idx)
            if movement is not None:
                flatten = lambda l: [item for sublist in l for item in sublist]
                state_ = flatten(movement[0])
                map_ = ''.join(str(e) for e in state_)

                if map_ in visited:
                    a = cost_now[map_]
                    if a > node.cost + movement[1]:
                        new_node = visited[map_]
                        new_node.cost = node.cost + movement[1]
                        cost_now[new_node.map] = new_node.cost
                        edge_cost[new_node.map] = new_node.edge_cost
                        new_node.parent = node
                else:
                    new_node = (Node(movement[0], node.cost, movement[1], node))
                #
                #
                #
                #
                # if new_node.map in visited:
                #     try:
                #         a = cost_now[new_node.map]
                #         if a > node.cost + new_node.edge_cost:
                #             new_node.cost = node.cost + new_node.edge_cost
                #             cost_now[new_node.map] = new_node.cost
                #             edge_cost[new_node.map] = new_node.edge_cost
                #     except:
                #         pass
                # try:
                #     a = cost_now[new_node.map]
                #     if a < node.cost + new_node.edge_cost:
                #         children.append(new_node)
                # except:
                # if new_node.map in explored:
                #     continue
                # else:
                #     children.append(new_node)
                # visited[new_node.map] = new_node
                    children.append(new_node)
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
    # file = sys.argv[1]
    file = str('entrada_1')
    world = Container(str(file))
    node, cost_now, edge_cost = dijkstra(world)
    # final = time.time()
    # node = djk((world))
    # cost = node.cost + node.edge_cost
    cost = record_cost(node, edge_cost)
    final = time.time()
    # print(len(cost_now))
    print(cost, 'time: ' + str(round(final - init, 4)) + ' s')


if __name__ == '__main__':
    main()