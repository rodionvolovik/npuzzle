import heapq
from parsing_utilities import generate_aim_puzzle

class Solver:
    def __init__(self, board, heuristic):
        self.size = board.size
        self.aim_board, self.aim_board_coordinates = generate_aim_puzzle(self.size)
        self.aim_board_hash = hash(self.aim_board)
        if heuristic == "M":
            self.heuristic = self.manhattan

    # A* algorithm implementation
    def solve(self, board):
        opened_states = {}
        closed_states = {}
        queue = [] # Prioritized by heuristics value

        heapq.heappush(queue, (self.heuristic(board.puzzle_tuple), board.puzzle_hash))
        opened_states = dict({board.puzzle_hash: board})
        memory_used_by_states = len(queue) # @todo clarify what memory is considered to count

        while len(queue) > 0:
            state_current = heapq.heappop()


    def calculate_heuristic(self, puzzle, heuristic, operation):
        expression = 0
        for i in range(self.size):
            for j in range(self.size):
                value = puzzle[i][j]
                reference_position = self.aim_board_coordinates[value - 1]
                expression = expression + heuristic(i, reference_position[0], j, reference_position[1])
        return operation(expression)

    # Different heuristic functions
    def manhattan(self, puzzle):
        return self.calculate_heuristic(puzzle, lambda x1, x2, y1, y2: abs(x2 - x1) + abs(y2 - y1), lambda i:i)

