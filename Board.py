from copy import copy, deepcopy

class Board:
    def __init__(self, size, puzzle):
        self.size = size
        self.puzzle = puzzle
        self.hashsum = hash(tuple(self.puzzle))
        self.heur = 0
        self.depth = 0
        self.parent = None

    def __str__(self):
        string_puzzle = ""
        for i in range(self.size ** 2):
            if i % self.size == 0:
                string_puzzle += "\n"
            string_puzzle += str(self.puzzle[i]) + 2 * " "
        return string_puzzle

    def __eq__(self, other):
        if other == None:
            return False
        return self.hashsum == other.hashsum

    def __lt__(self, other):
        if other == None:
            return False
        return self.heur + self.depth < other.heur + other.depth

    def get_inversion(self):
        inversion = 0
        for i in range(self.size ** 2 - 1):
            for j in range(i + 1, self.size ** 2):
                if self.puzzle[i] and self.puzzle[j] and self.puzzle[i] > self.puzzle[j]:
                    inversion += 1

        return inversion

    def is_solvable(self):
        inversion = self.get_inversion()

        if (self.size & 1):
            return not inversion & 1
        else:
            pos_0 = self.puzzle.index(0) / self.size
            print(self.puzzle, pos_0)
            if pos_0 & 1:
                return not inversion & 1
            else:
                return inversion & 1

    def create_coordinate_list(self):
        coordinates = {}
        for i in range(0, self.size ** 2):
            value = self.puzzle.index(i)
            col, row = value / self.size, abs(value - value / self.size * self.size)
            coordinates[value] = [col, row]
        return coordinates

    def state_new(self, empty_cell, x):
        new_puzzle = list(self.puzzle)
        new_puzzle[empty_cell] = new_puzzle[empty_cell + x]
        new_puzzle[empty_cell + x] = 0
        new_board = Board(self.size, new_puzzle)
        new_board.depth = self.depth + 1
        new_board.parent = self
        return new_board

    def get_neighbours(self):
        empty_cell = self.puzzle.index(0)
        possible_moves = [1, -1,  3, -3]
        moves = []
        for move in possible_moves:
            row_old, col_old = empty_cell / self.size, abs(empty_cell - empty_cell / self.size * self.size)
            row_new, col_new = (empty_cell + move) / self.size, abs((empty_cell + move) - (empty_cell + move) / self.size * self.size)
            if empty_cell + move < self.size ** 2 and empty_cell + move > -1 and (row_new == row_old or col_new == col_old):
                moves.append(move)

        return map(lambda x: self.state_new(empty_cell, x), moves)
