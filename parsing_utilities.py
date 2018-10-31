import sys
import re


def check_puzzle_consistency(matrix, size):
    ref_matrix = [i for i in range(0, size ** 2)]
    if sorted(matrix) != ref_matrix:
        if len(matrix) != len(ref_matrix):
            print("OOOPS! Puzzle should have %d elements instead of %d", size ** 2, len(matrix))
            sys.exit()
        print("OOOPS! Puzzle elements should be sequential and not repeating")
        sys.exit()


def read_file(path_to_file):
    size = 0
    matrix = []
    try:
        file = open(path_to_file)
    except:
        print("OOOPS! This is not a file $(")
        sys.exit()
    # @todo check if there is information
    lines = []
    for line in file:
        try:
            line = line.split("#")[0].strip()
        except:
            pass
        if line.strip().startswith("#") or line == "":
            continue
        lines.append(line)
    print(lines)
    for line in lines:
        if size == 0:
            match = re.match("^([0-9]+\s?)", line)
            if match:
                size = int(match.group())
            else:
                print("OOOPS! Please, provide a matrix size")
                sys.exit()
        else:
            match = re.match("^([0-9]+\s?){%d,}" % size, line)
            if match:
                elements = match.group().split()
                if len(elements) > size:
                    print("OOOPS! Something is wrong, dude")
                    sys.exit()
                for item in elements:
                    matrix.append(int(item))
            else:
                print("OOOPS! Provided puzzle isn't correct")
                sys.exit()
    check_puzzle_consistency(matrix, size)
    return size, matrix

# @todo do refactor
def generate_goal_puzzle(size):
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
    puzzle = []
    for i in range(size):
        for j in range(size):
            puzzle.append(matrix_goal[i][j])
    return puzzle

