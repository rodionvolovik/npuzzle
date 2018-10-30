class Board:
    def __init__(self, size, puzzle):
        self.size = size
        self.puzzle = list(puzzle)
        self.puzzle_tuple = self.make_puzzle_tuple(puzzle)
        self.puzzle_hash = hash(self.puzzle_tuple)
        self.heuristic_value = 0
        self.depth = 0
        self.parent = None

    # Returns True if given instance of puzzle is solvable
    def is_solvable(self):
        inversion = self.get_iversion()

        # If puzzle self.size is odd return true
        if self.size & 1:
            return inversion & 1
        else:
            empty_position = self.find_empty_element_row()
            if empty_position & 1:
                return inversion & 1
            else:
                return not inversion & 1

    # @todo could be optimized and check inversions again
    def get_iversion(self):
        inversion = 0
        for i in range(0, self.size ** 2 - 1):
            for j in range(i + 1, self.size ** 2):
                if self.puzzle[j] and self.puzzle[i] and self.puzzle[i] > self.puzzle[j]:
                    inversion = inversion + 1
        return inversion

    # @todo could be optimized
    def find_empty_element_row(self):
        for i in range(0, self.size ** 2):
                if self.puzzle[i] == 0:
                    return i/self.size

    def find_empty_element(self):
        row = self.find_empty_element_row()
        for col in range(self.size):
            if self.puzzle_tuple[row][col] == 0:
                return row, col

    def make_puzzle_tuple(self, puzzle):
        puzzle_tuple = []
        for i in range(0, self.size):
            puzzle_tuple.append([puzzle.pop(0) for j in range(0, self.size)])
        puzzle_tuple = tuple(tuple(line) for line in puzzle_tuple)
        return puzzle_tuple

    def state_new(self, row_0, col_0, row, col):
        import sys
        pos_0 = row_0 * self.size + col_0
        # print(row, col, row_0, col_0, pos_0)
        pos = row * self.size + col
        new_puzzle = list(self.puzzle)
        new_puzzle[pos_0] = new_puzzle[pos]
        new_puzzle[pos] = 0
        # print(self.puzzle, new_puzzle)

        new_board = Board(self.size, new_puzzle)
        new_board.depth = self.depth + 1
        new_board.parent = self
        return new_board


    def get_next_states(self):
        row_0, col_0 = self.find_empty_element()
        # print("EMPTY_ELEMENT", row_0, col_0)
        states = []
        if row_0 > 0:
            states.append((row_0 - 1, col_0))
        if col_0 > 0:
            states.append((row_0, col_0 - 1))
        if row_0 < self.size - 1:
            states.append((row_0 + 1, col_0))
        if col_0 < self.size - 1:
            states.append((row_0, col_0 + 1))

        return map(lambda x: self.state_new(row_0, col_0, x[0], x[1]), states)
