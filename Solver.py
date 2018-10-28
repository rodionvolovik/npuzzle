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
        opened_states = []
        closed_states = {}

        heapq.heappush(opened_states, board)
        nodes = dict({board.puzzle_tuple: board})
        memory_used_by_states = len(nodes) # @todo clarify what memory is considered to count

        print(board.puzzle_tuple)
        print(self.heuristic(board.puzzle_tuple))

        while len(opened_states) > 0:
            pass

    def calculate_heuristic(self, puzzle, heuristic, operation):
        expression = 0
        for i in range(self.size):
            for j in range(self.size):
                print(i,j)
                value = puzzle[i][j]
                reference_position = self.aim_board_coordinates[value - 1]
                expression = expression + heuristic(i, reference_position[0], j, reference_position[1])
        return operation(expression)

    # Different heuristic functions
    def manhattan(self, puzzle):
        return self.calculate_heuristic(puzzle, lambda x1, x2, y1, y2: abs(x2 - x1) + abs(y2 - y1), lambda i:i)





# import time
# import heapq
# import  math

#
# def h_manhattan(puzzle):
#     return  calculate_heuristic(puzzle,
#                 lambda r, tr, c, tc: abs(tr - r) + abs(tc - c),
#                                 lambda t:t)
# def h_manhattan_lsq(puzzle):
#     return calculate_heuristic(puzzle,
#                 lambda r, tr, c, tc: (abs(tr - r) + abs(tc - c)) ** 2,
#                 lambda t: math.sqrt(t))
# def h_linear(puzzle):
#     return calculate_heuristic(puzzle,
#                 lambda r, tr, c, tc: (math.sqrt((tr - r) ** 2 + (tc - c) ** 2)),
#                 lambda t: t)
# def h_linear_lsq(puzzle):
#     return calculate_heuristic(puzzle,
#                 lambda r, tr, c, tc: (tr - r) ** 2 + (tc - c) ** 2,
#                 lambda t: math.sqrt(t))
# def calculate_heuristic(puzzle, item_calc, ret):
#     t = 0
#     for row in range(GLOBAL_SIZE):
#         for col in range(GLOBAL_SIZE):
#             val = puzzle.matrix[row][col]
#             point = GLOBAL_LIST[val - 1]
#             t += item_calc(row, point[0], col, point[1])
#     return ret(t)
#
# def index(item, seq):
#     for s in seq:
#         if s.hash == item.hash:
#             return seq.index(s)
#     return -1
#
# class Npuzzle:
#     def __init__(self, input):
#         self._depth = 0 # depth in a graph
#         self._heurvalue = 0 # heuristic value
#         self.parent = None # pointer to parent
#         self.matrix = []
#         for i in range(0, GLOBAL_SIZE):
#             self.matrix.append(input[i][:])
#         self.tuplematrix = 0
#         self.hash = 0
#
#     def init_tuple_matrix(self):
#         self.tuplematrix = tuple(tuple(line) for line in self.matrix)
#         self.hash = hash(self.tuplematrix)
#     def clone(self):
#         Np = Npuzzle(self.matrix)
#         return Np
#     def __lt__(self, other):
#         if self._depth + self._heurvalue > other._depth + other._heurvalue:
#             return False
#         elif self._depth + self._heurvalue == other._depth + other._heurvalue and self._depth > other._depth:
#             return True
#         else:
#             return True
#     def findcoord(self, val):
#         for row in range(0, GLOBAL_SIZE):
#             for col in range(0, GLOBAL_SIZE):
#                 if self.matrix[row][col] == val:
#                     return row, col
#
#     def set_for_swap(self, row, col, val):
#         self.matrix[row][col] = val
#
#     def swap(self, point_0, point_1):
#         tmp = self.matrix[point_1[0]][point_1[1]]
#         self.set_for_swap(point_0[0],point_0[1], tmp)
#         self.set_for_swap(point_1[0], point_1[1], 0)
#
#     def get_list_of_movies(self, row, col):
#         step = []
#         if row > 0:
#             step.append((row - 1, col))
#         if col > 0:
#             step.append((row, col - 1))
#         if row < GLOBAL_SIZE - 1:
#             step.append((row + 1, col))
#         if col < GLOBAL_SIZE - 1:
#             step.append((row, col + 1))
#         return step
#
#     def get_list_of_successor(self):
#         empty = self.findcoord(0)
#         movies = self.get_list_of_movies(empty[0], empty[1])
#         def create_succ(point_0, point_1):
#             new = self.clone()
#             new.swap(point_0, point_1)
#             new._depth = self._depth + DEPTH
#             new.parent = self
#             new.init_tuple_matrix()
#             return new
#         return map(lambda x: create_succ(empty, x), movies)
#
    # def findpath(self,h):
    #     """Get heuristic function as a parametr
    #     openvertex[] - binary tree with not considered puzzle state
    #     closevertex[] - hashmap with considered puzzle state (key is a puzzle matrix - value is member of Npuzzle class)"""


    #     openvertex = []                     # List of vertex wich will be considered
    #     heapq.heappush(openvertex, self)
    #     openvertexdict = dict({self.tuplematrix:self})                      # List of vertex which has been already considered
    #     closedvertex = dict()
    #     maxstatesinmemory = 0
    #     while len(openvertex)>0:
    #         maxstatesinmemory = max(maxstatesinmemory, len(openvertex) + len(closedvertex))
    #         x = heapq.heappop(openvertex)
    #         openvertexdict.pop(x.tuplematrix)
    #         if (x.hash == HashGlobal):
    #             return x, len(openvertex), maxstatesinmemory                        # We have been find solution
    #         ## IS Solved end
    #
    #         possiblesteps = x.get_list_of_successor()
    #
    #         for suc in possiblesteps:
    #             is_in_open = openvertexdict.get(suc.tuplematrix)
    #             is_in_close = closedvertex.get(suc.tuplematrix)
    #             # timestamp = time.time()
    #             hval = h(suc) * HEUR
    #             # timepp = time.time() - timestamp
    #             # T.append(timepp)
    #             fval = hval + suc._depth
    #             if is_in_open == None and is_in_close == None:
    #                 suc._heurvalue = hval
    #                 heapq.heappush(openvertex, suc)
    #                 openvertexdict.update({suc.tuplematrix:suc})
    #             elif is_in_open != None:
    #                 if fval < is_in_open._heurvalue + is_in_open._depth:
    #                     is_in_open._heurvalue = hval
    #                     is_in_open.parent = suc.parent
    #                     is_in_open._depth = suc._depth
    #             elif is_in_close != None:
    #                 if fval < is_in_close._depth + is_in_close._heurvalue:
    #                     suc._heurvalue = hval
    #                     closedvertex.pop(suc.tuplematrix)
    #                     heapq.heappush(openvertex, suc)
    #                     openvertexdict.update({suc.tuplematrix:suc})
    #         closedvertex.update({x.tuplematrix:x})
    #     return [], 0, 0