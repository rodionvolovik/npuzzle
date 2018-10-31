# @todo Optimize A* algorithm for N > 3
# @todo Figure out inversion problem
# @todo Refactor parsing_utilities
# @todo Add more documentation to README.md

import time
import argparse
from Solver import Solver
from Board import Board
from parsing_utilities import generate_goal_puzzle, read_file
import npuzzle_gen
import sys


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(prog='npuzzle')
    parser.add_argument('-p', '--path', type=str, default=False, help="Path to source file with puzzle")
    parser.add_argument('-heur', '--heuristic', type=str, help="Heusristic function for calculations",
                        choices=['M', 'E', "T"], default='M')
    parser.add_argument('-i', '--iteration', type=int, help="Iterations for generation of a new puzzle",
                        default=60)
    parser.add_argument('-s', '--size', type=int, help="Size of puzzle", default=3)
    parser.add_argument('-t', '--type', default=False, type=str, choices=['g', 'uc'])
    args = parser.parse_args()

    # Extract data and/or generate a new puzzle
    if args.path:
        size, puzzle = read_file(args.path)
        board = Board(size, puzzle)
    else:
        board = Board(args.size, npuzzle_gen.make_puzzle(args.size, True, args.iteration))

    goal = Board(board.size, generate_goal_puzzle(board.size))
    if not board.is_solvable(goal):
        print("WhOOOPS! Puzzle is not solvable")
        print(board)
        sys.exit()

    print("Solving...")
    solver = Solver(board.size, goal, args.heuristic, args.type)

    time_start = time.time()
    path, max_memory, openstate_len = solver.solve(board)
    calculation_time = time.time() - time_start

    if path == None:
        import sys
        print("OOOPS! Puzzle is unsolvable")
        sys.exit()

    print("\nMaximum memory used is = %d" % max_memory)
    print("Openstates lost after resolving = %d" % openstate_len)
    print("Moves made to solve = %d" % len(path))
    print("Time spent for calculations %.5f s" % calculation_time)
    print("Authors: rvolovik, vpopovyc")

    quit = ''
    while quit != 'y' or quit != 'Y' or quit != 'n':
        quit = input("Would you like to see all the steps? 'Y' 'n': ")
        if not len(path):
            print(board)
        if quit == 'y' or quit == 'Y':
            for step in path:
                print(step)
            print("\nThanks for watching :)")
            break
        else:
            break

