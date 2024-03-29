from Enviroment import Container
from Node import Node
import sys
import Queue

world = None
init_node = None
cost_now = {}
explored = {}
visited = {}


def dijkstra(world):
    global init_node, cost_now, explored, visited

    init_node = Node(world.initial_config, 0, 0, None)
    idx = world.result
    frontier = Queue.PriorityQueue()

    frontier.put((init_node.cost, init_node))
    cost_now[init_node.map] = 0

    while frontier:
        node = frontier.get_nowait()[1]
        if node.matrix_state == world.final_config:
            return node, cost_now

        explored[node.map] = node
        successor = expand(node, idx)

        for child in successor:
            try:
                explored[child.map]
            # if child.map not in explored:
            except:
                new_cost = cost_now[node.map] + child.edge_cost
                try:
                    if new_cost < cost_now[child.map]:
                        cost_now[child.map] = new_cost
                        frontier.put_nowait((child.cost, child))
                        visited[child.map] = child
                except:
                    cost_now[child.map] = new_cost
                    frontier.put((child.cost, child))
                    visited[child.map] = child

def expand(node, indices):
    global cost_now, explored, visited
    children = []
    for idx in indices:
        for possible_move in [1, 2]:
            movement = move(node.matrix_state, possible_move, idx)
            if movement is not None:
                state_ = getList(movement[0])
                map_ = ''.join(map(str, state_))
                try:
                    visited[map_]
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
    return children


def getList(l):
    return [item for sublist in l for item in sublist]


def move(state, position, out):
    global world

    new_state = [i[:] for i in state]
    row, col = out[0], out[1]

    if position == 1:  # Down
        if (row + 1) > (world.rows - 1):
            return None
        else:
            temp = new_state[row + 1][col]
            new_state[row + 1][col] = new_state[row][col]
            new_state[row][col] = temp
            cost = world.key_values[new_state[row][col]] + world.key_values[new_state[row + 1][col]]
            return new_state, cost

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
    global world

    input = sys.argv[1]
    output = sys.argv[2]

    world = Container(str(input))
    node, cost_now = dijkstra(world)
    write_output(node.cost, output)


if __name__ == '__main__':
    main()
