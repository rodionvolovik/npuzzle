
import argparse
import sys
from Solver import Solver
from Board import Board
from parsing_utilities import generate_goal_puzzle, read_file
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
    #     print("OOOPS! Puzzle is not solvable")
    #     sys.exit(1)

    goal = generate_goal_puzzle(board.size)
    solver = Solver(board.size, Board(board.size, goal), args.heuristic)
    path, max_memory, openstate_len = solver.solve(board)

    print("\nMaximum memory used is = %d" % max_memory)
    print("Openstates lost after resolving = %d" % openstate_len)
    print("Moves made to solve = %d" % len(path))
    print("Authors: rvolovik, vpopovyc")

    quit = ''
    while quit != 'y' or quit != 'Y' or quit != 'n':
        quit = input("Would you like to see all the steps? 'Y' 'n': ")
        if quit == 'y' or quit == 'Y':
            for step in path:
                print(step)
            print("\nThanks for watching :)")
            break
        else:
            break

