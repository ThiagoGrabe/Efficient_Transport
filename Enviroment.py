class Container:
    """Defines the container with features for the search algorithm"""

    def __init__(self, entry):
        self.entry = str(entry)
        self.rows = None
        self.columns = None
        self.key_values = dict()
        self.min = 1
        self.nm = 9

        with open(str(self.entry)) as file:
            self.load = [[int(num) for num in line.split()] for line in file]

            self.rows = self.load[0][0]
            self.columns = self.load[0][1]
            self.weight = self.load[1]
            self.board_len = self.rows * self.columns

            # Check if the container has a valid size (max=9)
            if not self.min <= (self.rows * self.columns) <= self.nm:
                raise Exception('Entry not valid! Maximum items = 9.')

            # Initial and final configuration of the container
            self.initial_config = self.load[2:(2 + self.rows)]
            self.final_config = self.load[(2 + self.rows):]

            # Create the initial and final state
            self.flatten = lambda l: [item for sublist in l for item in sublist]
            self.start_state = self.flatten(self.initial_config)
            self.final_state = self.flatten(self.final_config)

        # Create the dict "key_values" for all positions with vertices weight
        for line in self.initial_config:
            for num in line:
                self.key_values[num] = self.weight[num - 1]

    def set_index(self, current_state):
        self.result = list()
        self.unique_result = list()
        l1 = current_state
        l2 = self.final_config

        for row in range(0, self.rows):
            for col in range(0, self.columns):
                self.result.append([row, col, self.key_values[l1[row][col]]])
        try:
            return self.result
        except:
            return None
