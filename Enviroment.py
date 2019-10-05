class Container:
    """Defines the container with features for the search algorithm"""

    def __init__(self, entry):
        self.entry = str(entry)
        self.rows = None
        self.columns = None
        self.key_values = {}

        with open(str(self.entry)) as file:
            self.load = [[int(num) for num in line.split()] for line in file if line]

            self.rows = self.load[0][0]
            self.columns = self.load[0][1]
            self.weight = self.load[1]

            # Initial and final configuration of the container
            self.initial_config = self.load[2:(2 + self.rows)]
            self.final_config = self.load[(2 + self.rows):]
            self.start_state = self.getList(self.initial_config)
            self.final_state = self.getList(self.final_config)

        # Create the dict "key_values" for all positions with vertices weight
        for line in self.initial_config:
            for num in line:
                self.key_values[num] = self.weight[num - 1]

        self.result = []
        for row in range(0, self.rows):
            for col in range(0, self.columns):
                self.result.append([row, col])


    def set_index(self):
        self.result = []
        for row in range(0, self.rows):
            for col in range(0, self.columns):
                self.result.append([row, col])
        return self.result

    def getList(self, l):
        return [item for sublist in l for item in sublist]
