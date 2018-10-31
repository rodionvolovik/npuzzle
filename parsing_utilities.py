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
    matrix_goal = [0 for i in range(size ** 2)]

    def is_filled(x):
        if x >= size ** 2 - 1:
            return True
        return False

    i = 0
    index = -1
    moves_size = size
    horisontal = 1
    vertical = size
    number = 0
    while True:
        # right
        for move_step in range(moves_size):
            number += 1
            index += horisontal
            matrix_goal[index] = number
        if is_filled(number):
            break
        moves_size -= 1

        # bottom
        for move_step in range(moves_size):
            index += vertical
            number += 1
            matrix_goal[index] = number
        if is_filled(number):
            break

        # left
        for move_step in range(moves_size):
            index -= horisontal
            number += 1
            matrix_goal[index] = number
        if is_filled(number):
            break
        moves_size -= 1

        # top
        for move_step in range(moves_size):
            index -= vertical
            number += 1
            matrix_goal[index] = number
        if is_filled(number):
            break

        if moves_size <= 0:
            return matrix_goal

    return matrix_goal

