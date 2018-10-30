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

        board.heuristic_value = self.heuristic(board.puzzle_tuple)
        print(board.heuristic_value, board.puzzle_tuple)
        heapq.heappush(queue, (board.heuristic_value, board.puzzle_hash))
        opened_states = dict({board.puzzle_hash: board})
        memory_used_by_states = len(queue) # @todo clarify what memory is considered to count

        while len(queue) > 0:
            heap_top = heapq.heappop(queue)
            state_current = opened_states.pop(heap_top[1])

            memory_used_by_states = max(memory_used_by_states, len(opened_states) + len(closed_states))

            if state_current.puzzle_hash == self.aim_board_hash:
                return state_current, len(opened_states), memory_used_by_states

            state_current_nodes = state_current.get_next_states()

            for state_node in state_current_nodes:
                in_opened = opened_states.get(state_node.puzzle_hash)
                in_closed = opened_states.get(state_node.puzzle_hash)

                heuristic_value = self.heuristic(state_node.puzzle_tuple)
                final_value = heuristic_value + state_node.depth
                print(heuristic_value, final_value, state_node.depth, state_node.puzzle_tuple)

                if in_opened == None and in_closed == None:
                    state_node.heuristic_value = heuristic_value
                    heapq.heappush(queue, (final_value, state_node.puzzle_hash))
                    opened_states.update({state_node.puzzle_hash: state_node})
                # elif in_opened != None:
                #     if final_value < in_opened.depth + in_opened.heuristic_value:
                #         in_opened.heuristic_value = final_value
                #         in_opened.parent = state_node.parent
                #         in_opened.depth = state_node.depth

            closed_states.update({state_current.puzzle_hash: state_current})
            if state_current.depth == 1:
                break
        while len(queue):
            s = heapq.heappop(queue)
            print(opened_states.get(s[1]).puzzle_tuple, opened_states.get(s[1]).heuristic_value)

        return [], len(opened_states), None


    def calculate_heuristic(self, puzzle, heuristic, operation):
        expression = 0
        for i in range(self.size):
            for j in range(self.size):
                value = puzzle[i][j]
                if value == 0:
                    continue
                reference_position = self.aim_board_coordinates[value - 1]
                if heuristic(i, reference_position[0], j, reference_position[1]) != 0:
                    expression += 1
        return operation(expression)

    # Different heuristic functions
    def manhattan(self, puzzle):
        return self.calculate_heuristic(puzzle, lambda x1, x2, y1, y2: abs(x2 - x1) + abs(y2 - y1), lambda i:i)

