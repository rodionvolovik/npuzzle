def create_goal_puzzle(n):
    k = n ** 2  #number of elements

    arr = [[0 for i in range(n)] for j in range(n)] #create zerro array N * N

    list = k * [[None, None]]

    #  1   2   3   4  5
    # 16  17  18  19  6
    # 15  24  25  20  7
    # 14  23  22  21  8
    # 13  12  11  10  9

    def row_fill(row, column, flag, num):
        i = column
        while i in range(n) and arr[row][i] == 0:
            arr[row][i] = num
            list[num - 1] = [row, i]
            num = num + 1
            i = i + flag
        if num > k:
            return
        if flag == 1:
            column_fill(row + 1, i - 1, 1, num)
        else:
            column_fill(row - 1, i + 1, -1, num)


    def column_fill(row, column, flag, num):
        i = row
        while i in range(n) and arr[i][column] == 0:
            arr[i][column] = num
            list[num - 1] = [i, column]
            num = num + 1
            i = i + flag
        if num > k:
            return
        if flag == -1:
            row_fill(i + 1, column + 1,  1, num)
        else:
            row_fill(i - 1, column - 1,  -1, num)

    row_fill(0, 0, 1, 1)
    arr[list[k - 1][0]][list[k - 1][1]] = 0
    return arr, list

def inversion(size, puzzle):
    inv = 0
    for i in range(size * size - 1):
        for j in range(i + 1, size * size):
            if puzzle[i] > puzzle[j] and puzzle[i] != 0 and puzzle[j] != 0:
                inv += 1
    return inv

def is_solvable(size, goalmatrix, puzzlematrix):
    goal, puzzle = [], []
    for rawgoal, rawmatrix in zip(goalmatrix, puzzlematrix):
        for g,p in zip(rawgoal, rawmatrix):
            goal.append(g)
            puzzle.append(p)
    inv_goal = inversion(size, goal)
    inv_puzzl = inversion(size, puzzle)

    if size % 2 == 0:
        inv_goal += goal.index(0)
        inv_puzzl += puzzle.index(0)

    return (inv_puzzl % 2 == inv_goal % 2)
