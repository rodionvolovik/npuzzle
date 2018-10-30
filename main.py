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

    if not board.is_solvable():
        print("ERROR - Puzzle is not solvable")
        sys.exit(1)

    solver = Solver(board, args.heuristic)
    result = solver.solve(board)
    print(result[0].puzzle_tuple, result[1], result[2])

    # if type == 'grd':
    #     DEPTH = 0
    # elif type == 'ufm':
    #     HEUR = 0
    # path = []
    # while x.parent:
    #     path.append(x)
    #     x = x.parent
    # path.reverse()
    # # i = 0
    # # for t in T:
    # #     i = i + t
    # # print(i)
    # print("openstate = ", lenopen)
    # print("number of movies = ", len(path))
    # print("max number of states in memory = ", max)
