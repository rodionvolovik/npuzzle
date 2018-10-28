import argparse
import sys
import re
import npuzzle_gen
from ClassNpuzzle import Npuzzle
from heuristics import *


def check_puzzle_consistency(matrix, size):
    ref_matrix = [i for i in range(0, size ** 2)]
    if sorted(matrix) != ref_matrix:
        if len(matrix) != len(ref_matrix):
            print("ERROR - Puzzle should have %d elements instead of %d", size ** 2, len(matrix))
            sys.exit()
        print("ERROR - Puzzle elements should be sequential and not repeating")
        sys.exit()


# @todo do refactor
def generate_aim_puzzle(size):
    k = size ** 2
    matrix_goal = [[0 for i in range(size)] for j in range(size)]
    elements_position = k * [[None, None]]
    # Fills column sequence
    def fill_row(row, col, flag, num):
        i = col
        while i in range(size) and matrix_goal[row][i] == 0:
            matrix_goal[row][i] = num
            elements_position[num - 1] = [row, i]
            num = num + 1
            i = i + flag
        if num > k:
            return
        if flag == 1:
            fill_col(row + 1, i - 1, 1, num)
        else:
            fill_col(row - 1, i + 1, -1, num)
    # Fills row sequence
    def fill_col(row, column, flag, num):
        i = row
        while i in range(size) and matrix_goal[i][column] == 0:
            matrix_goal[i][column] = num
            elements_position[num - 1] = [i, column]
            num = num + 1
            i = i + flag
        if num > k:
            return
        if flag == -1:
            fill_row(i + 1, column + 1,  1, num)
        else:
            fill_row(i - 1, column - 1,  -1, num)
    fill_row(0, 0, 1, 1)
    matrix_goal[elements_position[k - 1][0]][elements_position[k - 1][1]] = 0
    # optimize access time by creating a tuple for reference matrix
    matrix_goal = tuple(tuple(line) for line in matrix_goal)
    return matrix_goal, elements_position


def read_file(path_to_file):
    size = 0
    matrix = []
    file = open(path_to_file)
    for line in file:
        if line.strip().startswith("#"):
            continue
        try:
            line = line.split("#")[0].strip()
        except:
            pass
        if size == 0:
            match = re.match("^([0-9]+\s?)", line)
            if match:
                size = int(match.group())
            else:
                print("ERROR - Please, provide a matrix size")
                sys.exit()
        else:
            match = re.match("^([0-9]+\s?){%d}" % size, line)
            if match:
                elements = match.group().split()
                row = []
                for item in elements:
                    matrix.append(int(item))
            else:
                print("ERROR - Provided puzzle isn't correct")
                sys.exit()
    check_puzzle_consistency(matrix, size)
    matrix_goal, elements_position = generate_aim_puzzle(size)
    return size, matrix, matrix_goal, elements_position


# @todo could be optimized
def get_iversion(matrix, size):
    inversion = 0
    for i in range(0, size ** 2 - 1):
        for j in range(i + 1, size ** 2):
            if matrix[j] and matrix[i] and matrix[i] > matrix[j]:
                inversion = inversion + 1
    return inversion


# @todo could be optimized
def find_empty_element(matrix, size):
    for i in range(0, size - 1):
        for j in range(0, size - 1):
            if matrix[i][j] == 0:
                return size - i


# Returns True if given instance of puzzle is solvable
def is_solvable(matrix, size):
    inversion = get_iversion(matrix, size)

    if size & 1:
        return inversion & 1
    else:
        empty_position = find_empty_element(matrix, size)
        if empty_position & 1:
            return inversion & 1
        else:
            return not inversion & 1


# @ todo fix when size is even number
if __name__ == "__main__":
    func_pointer = {
        'M': manhatten,
        'Mlsq': manhetten_lsq,
        'E': euclidus,
        'Elsq': euclidus_lsq,
    }

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
        size, matrix, matrix_goal, elements_position = read_file(args.path)
    else:
        matrix_goal, elements_position = generate_aim_puzzle(args.size)
        size, matrix = args.size, npuzzle_gen.make_puzzle(args.size, True, args.iteration)

    print(size, matrix, matrix_goal, elements_position)

    if not is_solvable(matrix, size):
        print("ERROR - Puzzle is not solvable")
        sys.exit(1)

    temp = []
    row = []
    for i in range(0, size):
        row.append(matrix.pop(0) for j in range(0, size))
        temp.append(row)

    puzzle = Npuzzle(temp)
    puzzle.solve(args.heuristic, matrix_goal)



    # p, heuristic, type = read_and_parse()
    # if type == 'grd':
    #     DEPTH = 0
    # elif type == 'ufm':
    #     HEUR = 0
    # GLOBAL_SIZE, matrix = p[0], p[1]
    # #print(matrix)

    # GLOBAL_STATE = tuple(tuple(line) for line in GLOBAL_STATE)

    # HashGlobal = hash(GLOBAL_STATE)

    # Np = Npuzzle(matrix)
    # Np.init_tuple_matrix()
    # #start_time = time.time()
    # if heuristic == 'M':
    #     x, lenopen, max = Np.findpath(h_manhattan)
    # elif heuristic == 'Mlsq':
    #     x, lenopen, max = Np.findpath(h_manhattan_lsq)
    # elif heuristic == 'E':
    #     x, lenopen, max = Np.findpath(h_linear)
    # elif heuristic == 'Elsq':
    #     x, lenopen, max = Np.findpath(h_linear_lsq)
    # #print("time =", time.time() - start_time)
    #
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
    #
    # while True:
    #     text = raw_input("Search is over. Do you want to see all steps ? [y/n]: ")
    #     if text == 'y' or text == 'Y':
    #         for i in path:
    #             for line in i.matrix:
    #                 print(line)
    #             print("")
    #         break
    #     elif text == 'N' or text == 'n':
    #         break
