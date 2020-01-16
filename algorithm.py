import copy

####################################################
# calulate number of monsters around the explorer
####################################################

# calulate number of monsters around the explorer
def clue(data):
    newMap = data.coinPos
    rows = len(newMap)
    cols = len(newMap[0])
    direction = [[-1, -1], [-1, 0], [-1, 1], [0, -1], \
                 [0, 1], [1, -1], [1, 0], [1, 1]]
    length = len(direction)
    result = {}
    maxCol = 19
    maxRow = 9
    label1 = 6 # label for monsters
    label2 = 7
    for row in range(rows):
        for col in range(cols):
            count = 0
            for i in range(length):
                newRow = row + direction[i][0]
                newCol = col + direction[i][1]
                if newRow == -1 or newRow == (maxRow + 1) or \
                    newCol == -1 or newCol == (maxCol + 1) or \
                    newMap[row][col] == label1 or newMap[row][col] == label2:
                    pass
                else:
                    if newMap[newRow][newCol] == label1 or \
                       newMap[newRow][newCol] == label2:
                        count += 1
            if count != 0:
                key = (row, col)
                result[key] = count
    return result     
    
    
###########################################################
# check whether the maze is legal 
# some of the below codes are cited from 15-112 website
###########################################################

# helper function to rearrange the maze
def mazeHelper(maze):
    rows = len(maze)
    cols = len(maze[0])
    for row in range(rows):
        for col in range(cols):
            if maze[row][col] != 1:
                maze[row][col] = 0    
    return maze

# helper function to check whether the row and col are valid    
def isValid(maze, row, col):
    if not (0 <= row < len(maze) and 0 <= col < len(maze[0]) \
            and maze[row][col] == 0):
        return False
    else:
        return True

# helper function to check whether the maze is legal
def solve(maze, row, col, visited, alreadySeen, direction):
    if row == len(maze)-1 and col == len(maze[0])-1:
        return True
    for d in direction:
        drow, dcol = d
        if isValid(maze, row, col) and \
            (row + drow, col + dcol) not in alreadySeen:
            visited.append((row + drow, col + dcol))
            alreadySeen.add((row + drow, col + dcol))
            tmpSolution = solve(maze, row + drow, col + dcol, \
                                visited, alreadySeen, direction)
            if tmpSolution != False:
                return tmpSolution
            visited.pop()
    return False
    
# check whether the maze is legal
def solveMaze(data):
    maze = copy.deepcopy(data.initMap)
    newMaze = mazeHelper(maze)
    visited = [(0, 0)]
    alreadySeen = set()
    direction = [(-1, 0), (1, 0), (0, 1), (0, -1)]
    return solve(newMaze, 0, 0, visited, alreadySeen, direction)
    
    