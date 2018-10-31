import heapq

class Solver:
    def __init__(self, size, goal, heuristic):
        self.size = size
        self.goal = goal
        if heuristic == "M":
            self.heuristic = self.manhattan_heuristic

    def manhattan_heuristic(self, board, other):
        estimate = 0
        for i in range(1, self.size ** 2):
            value1 = board.puzzle.index(i)
            value2 = self.goal.puzzle.index(i)
            x1, y1 = value1 / board.size, abs(value1 - value1 / board.size * board.size)
            x2, y2 = value2 / board.size, abs(value2 - value2 / board.size * board.size)
            estimate += abs(x1 - x2) + abs(y1 - y2)
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
                is_closed = closed_states.get(neighbour.hashsum)
                if is_closed != None:
                    continue

                if current.parent != None and neighbour.hashsum == current.parent.hashsum:
                    continue

                heapq.heappush(queue, neighbour)

                neighbour.parent = current
                neighbour.depth = current.depth + 1 # @todo Change to constant value of uniform-cost search
                neighbour.heur = self.manhattan_heuristic(neighbour, self.goal) * 1.01

        return None * 3