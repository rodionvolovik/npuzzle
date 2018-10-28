class Board:
    def __init__(self, size, puzzle):
        self.size = size
        self.puzzle = list(puzzle)
        self.puzzle_tuple = self.make_puzzle_tuple(puzzle)

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
                    return self.size - i/self.size

    def make_puzzle_tuple(self, puzzle):
        # @todo remake this function
        puzzle_tuple = []
        for i in range(0, self.size):
            puzzle_tuple.append([puzzle.pop(0) for j in range(0, self.size)])
        puzzle_tuple = tuple(tuple(line) for line in puzzle_tuple)
        return puzzle_tuple

