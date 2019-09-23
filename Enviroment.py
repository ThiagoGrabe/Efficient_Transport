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
            # self.board_side = int(self.board_len**0.5)
            self.board_side = self.columns

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

        # self.index = self.set_index(self.initial_config, self.final_config)

        # if self.index is None:
        #     self.index = 1

    def set_index(self, current_state):
        self.result = list()
        self.unique_result = list()
        l1 = current_state
        l2 = self.final_config

        for row in range(0, self.rows):
            for col in range(0, self.columns):
                self.result.append([row, col, self.key_values[l1[row][col]]])
                # if l1[row][col] != l2[row][col]:
                #     self.result.append([row, col, self.key_values[l1[row][col]]])
                    #
                    # if (row - 1) > 0:
                    #     self.result.append([(row - 1), col, self.key_values[l1[(row - 1)][col]]])
                    # if (row +1) < self.rows:
                    #     self.result.append([(row + 1), col, self.key_values[l1[(row + 1)][col]]])
                    # if (col - 1) > 0:
                    #     self.result.append([row, (col - 1), self.key_values[l1[row][(col - 1)]]])
                    # if (col + 1) < self.columns:
                    #     self.result.append([row, (col + 1), self.key_values[l1[row][(col + 1)]]])
        #
        # for item in self.result:
        #     if item not in self.unique_result:
        #         self.unique_result.append(item)

        # self.result.sort(key=lambda x: x[2])
        try:
            return self.result
        except:
            return None
