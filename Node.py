class Node:
    """Defines the graph's node"""

    def __init__(self, matrix_state, cost, edge_cost, parent):

        self.matrix_state = matrix_state
        self.cost = cost
        self.edge_cost = edge_cost
        self.parent = parent
        self.state = self.getList(self.matrix_state)
        self.h = float('inf')

        if self.matrix_state:
            self.map = ''.join(str(e) for e in self.state)

    def getList(self, l):
        return [item for sublist in l for item in sublist]
    #
    def __eq__(self, other):
        return self.map == other.map

    def __lt__(self, other):
        return self.map < other.map
