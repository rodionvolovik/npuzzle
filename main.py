import argparse
import sys
from Solver import Solver
from Board import Board
from parsing_utilities import generate_aim_puzzle, read_file
import npuzzle_gen


# @ todo fix when size is even number
if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(prog='npuzzle')
    parser.add_argument('-p', '--path', type=str, default=False, help="Path to source file with puzzle")
    parser.add_argument('-heur', '--heuristic', type=str, help="Heusristic function for calculations",
                        choices=['M', 'Mlsq', 'E', "Elsq"], default='M')
    parser.add_argument('-i', '--iteration', type=int, help="Iterations for generation of a new puzzle",
                        default=60)
    parser.add_argument('-s', '--size', type=int, help="Size of puzzle", default=3)
    parser.add_argument('-type', '--greedy', default=False, type=str, choices=['greedy', 'uniform-cost'])
    args = parser.parse_args()

    # Extract data and/or generate a new puzzle
    if args.path:
        size, puzzle = read_file(args.path)
        board = Board(size, puzzle)
    else:
        board = Board(args.size, npuzzle_gen.make_puzzle(args.size, True, args.iteration))

    # @todo check solvability
    # if not board.is_solvable():
    #     print("ERROR - Puzzle is not solvable")
    #     sys.exit(1)

    solver = Solver(board, args.heuristic)
    result = solver.solve(board)
    print("RESULT", result[0], result[1], result[2])

    path = []
    x = result[0]
    while x.parent:
        path.append(x)
        x = x.parent
    path.reverse()

    for p in path:
        print(p.puzzle_tuple[0])
        print(p.puzzle_tuple[1])
        print(p.puzzle_tuple[2])
        print("------")
