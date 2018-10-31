import heapq
import math

class Solver:
    def __init__(self, size, goal, heuristic, greedy):
        self.size = size
        self.goal = goal
        self.g = 1
        self.h = 1.01

        if heuristic == "M":
            self.heuristic = self.manhattan_heuristic
            print("You have chosen Manhattan distance as heuristic function")
        elif heuristic == "E":
            self.heuristic = self.euclidian_distance
            print("You have chosen Euclidus distance as heuristic function")
        elif heuristic == "T":
            self.heuristic = self.tiles_out_of_place
            print("You have Tiles-out-of-place as heuristic function")

        if greedy and greedy == "g":
            self.g = 0
        elif greedy and greedy == "uc":
            self.h = 0


    def manhattan_heuristic(self, board, other):
        estimate = 0
        for i in range(1, self.size ** 2):
            value1 = board.puzzle.index(i)
            value2 = self.goal.puzzle.index(i)
            x1, y1 = value1 / board.size, abs(value1 - value1 / board.size * board.size)
            x2, y2 = value2 / board.size, abs(value2 - value2 / board.size * board.size)
            # x1, y1 = board.coordinates[i][0], board.coordinates[i][1]
            # x2, y2 = self.goal.coordinates[i][0], self.goal.coordinates[i][1]
            estimate += abs(x1 - x2) + abs(y1 - y2)
        return estimate

    def euclidian_distance(self, board, other):
        estimate = 0
        for i in range(1, self.size ** 2):
            value1 = board.puzzle.index(i)
            value2 = self.goal.puzzle.index(i)
            x1, y1 = value1 / board.size, abs(value1 - value1 / board.size * board.size)
            x2, y2 = value2 / board.size, abs(value2 - value2 / board.size * board.size)
            # x1, x2 = board.coordinates[i][0], board.coordinates[i][1]
            # x1, x2 = self.goal.coordinates[i][0], self.goal.coordinates[i][1]
            estimate += math.sqrt(abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2)
        return estimate

    def tiles_out_of_place(self, board, other):
        estimate = 0
        for i in range(1, self.size ** 2):
            value1 = board.puzzle.index(i)
            value2 = self.goal.puzzle.index(i)
            x1, y1 = value1 / board.size, abs(value1 - value1 / board.size * board.size)
            x2, y2 = value2 / board.size, abs(value2 - value2 / board.size * board.size)
            if (x1 - x2) + (y1 - y2) != 0:
                estimate += 1
        return estimate


    # A* algorithm implementation
    def solve(self, board):
        closed_states = {}
        max_memory = 0

        queue = [board]
        heapq.heapify(queue)

        heur_score = self.manhattan_heuristic(board, self.goal)

        while len(queue) > 0:
            max_memory = max(max_memory, len(closed_states) + len(queue))
            current = heapq.heappop(queue)

            if current == self.goal:
                path = []
                while current.parent:
                    path.append(current)
                    current = current.parent
                path.reverse()
                return path, max_memory, len(queue)

            closed_states.update({current.hashsum: current})

            neighbours = current.get_neighbours()
            for neighbour in neighbours:
                # print(neighbour)
                is_closed = closed_states.get(neighbour.hashsum)
                if is_closed != None:
                    continue

                if current.parent != None and neighbour.hashsum == current.parent.hashsum:
                    continue

                neighbour.parent = current
                neighbour.depth = current.depth + self.g
                neighbour.heur = self.heuristic(neighbour, self.goal) * self.h

                heapq.heappush(queue, neighbour)

        return None, None, None