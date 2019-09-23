class Node:
    """Defines the graph's node"""

    def __init__(self, matrix_state, parent, movement, cost):

        self.matrix_state = matrix_state
        self.parent = []
        self.move = movement
        self.cost = []
        self.path_cost = 0
        self.minId = 0

        self.flatten = lambda l: [item for sublist in l for item in sublist]
        self.state = self.flatten(self.matrix_state)

        if self.matrix_state:
            self.map = ''.join(str(e) for e in self.state)

        if parent is not None:
            self.parent.append(parent)
        if cost is not None:
            self.cost.append(cost)

    def add_parent(self, parent, cost):
        self.parent.append(parent)
        self.cost.append(cost)
        self.getMinCost()

    def getMinCost(self, cost=False, idx=False):
        m, i = max((v, i) for i, v in enumerate(self.cost))
        self.minId = i
        if cost:
            return m
        if idx:
            return i

    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map