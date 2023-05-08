import turtle
import queue
import numpy as np
from collections import deque
import random
# Global value
SIZE = 25
startX = -300
startY = -300
SQUARE_SIDE = 4
directionX = [-1, 0, 1, 0]
directionY = [0, 1, 0, -1]
colorList = ['blue', 'cyan', 'olive',
             'chartreuse', 'chocolate', 'firebrick', 'navajowhite',
             'maroon', 'darkgoldenrod', 'fuchsia', 'lightsalmon']
# Initialize turtle
screen = turtle.Screen()
cursor = turtle.Turtle()
cursor.pensize(1.5)


def createMaze(size, StartGoal, obstacle):  # size[0]: x, size[1]: y
    height = size[1]
    width = size[0]
    maze = np.zeros([height+1, width+1], dtype=int)  # create X+1*Y+1 0-maze
    for i in range(size[1]+1):
        for j in range(size[0]+1):
            if i == 0 or i == size[1] or j == 0 or j == size[0]:
                maze[i][j] = 2
            elif (i == StartGoal[0] and j == StartGoal[1]) or (i == StartGoal[2] and j == StartGoal[3]):
                maze[i][j] = 9
            else:
                maze[i][j] = 0

    for i in range(len(obstacle)):
        for j in range(-len(obstacle[i]), -1, 2):
            maze = draw_line(
                maze, obstacle[i][j+3], obstacle[i][j+2], obstacle[i][j+1], obstacle[i][j])
    return maze


def draw_line(mat, x0, y0, x1, y1, inplace=False):
    if not (0 <= x0 < mat.shape[0] and 0 <= x1 < mat.shape[0] and
            0 <= y0 < mat.shape[1] and 0 <= y1 < mat.shape[1]):
        raise ValueError('Invalid coordinates.')
    if not inplace:
        mat = mat.copy()
    if (x0, y0) == (x1, y1):
        mat[x0][y0] = 3
        return mat if not inplace else None
    transpose = abs(x1 - x0) < abs(y1 - y0)
    if transpose:
        mat = mat.T
        x0, y0, x1, y1 = y0, x0, y1, x1
    if x0 > x1:
        x0, y0, x1, y1 = x1, y1, x0, y0
    mat[x0][y0] = 4
    mat[x1][y1] = 4
    x = np.arange(x0 + 1, x1)
    y = np.round(((y1 - y0) / (x1 - x0)) * (x - x0) + y0).astype(x.dtype)
    mat[x, y] = 3
    if not inplace:
        return mat if not transpose else mat.T


def drawSquare(cursor, color):
    cursor.fillcolor(color)
    cursor.begin_fill()
    for i in range(SQUARE_SIDE):
        cursor.forward(SIZE)
        cursor.left(90)
    cursor.forward(SIZE)
    cursor.end_fill()


def drawBoard(size, StartGoal, obstacle, maze):
    for i in range(size[1]+1):
        cursor.up()
        cursor.setpos(startX, startY + SIZE*i)
        cursor.down()
        cursor.speed(0)
        for j in range(size[0]+1):
            if maze[i][j] == 2:
                color = 'gray'
            elif maze[i][j] == 9:
                color = 'green'
            elif maze[i][j] == 3:
                color = 'pink'
            elif maze[i][j] == 4:
                color = 'purple'
            else:
                color = 'white'
            drawSquare(cursor, color)
        cursor.hideturtle()


def drawPosition(x, y, cursor, color):
    PosX = startX + (x * SIZE)
    PosY = startY + (y * SIZE)
    cursor.up()
    cursor.goto(PosX, PosY)
    cursor.down()
    drawSquare(cursor, color)
    cursor.speed(0)


def setupBoard():
    screen.setup(1000, 800)
    screen.tracer(10, 100)
    cursor.speed(0)


def readFile():
    size = []
    StartGoal = []
    obstacle = []
    list = []

    with open("input.txt", "r") as my_file:
        for line in my_file:
            str = line.split()
            list.append(str)
        my_file.close()

    for i in range(len(list)):
        if i == 0:
            size = list[i]
        elif i == 1:
            StartGoal = list[i]
        elif i > 2:
            obstacle.append(list[i])

    size = [int(i) for i in size]
    StartGoal = [int(i) for i in StartGoal]

    for i in range(len(obstacle)):
        for j in range(len(obstacle[i])):
            obstacle[i][j] = int(obstacle[i][j])
    return size, StartGoal, obstacle


def BFS(startGoal, maze, size):
    solution = {}
    x, y = startGoal[0], startGoal[1]
    solution[x, y] = (x, y)  # backtrack
    costExpandedNode = 0
    goalState = False
    frontier = deque()
    frontier.append((x, y))

    while len(frontier) > 0:
        currCell = frontier.popleft()
        costExpandedNode += 1
        currX = currCell[0]
        currY = currCell[1]
        for i in range(4):
            if (goalState == True):
                break
            adjacentX = currX + directionX[i]
            adjacentY = currY + directionY[i]
            if (adjacentY > size[0] + 1 or adjacentX > size[1]+1 or adjacentX < 0 or adjacentY < 0):
                continue
            if adjacentX == startGoal[0] and adjacentY == startGoal[1]:
                continue
            if (maze[adjacentX][adjacentY] == 0):
                frontier.append((adjacentX, adjacentY))
                solution[adjacentX, adjacentY] = (currX, currY)
                maze[adjacentX][adjacentY] = 1
                color = 'cyan'
                drawPosition(adjacentY, adjacentX, cursor, color)
            if maze[adjacentX][adjacentY] == 9:
                solution[adjacentX, adjacentY] = (currX, currY)
                goalState = True
    # print(solution)
    costPath = 0
    goalX, goalY = startGoal[2], startGoal[3]
    a, b = goalX, goalY
    while(goalX, goalY) != (x, y):
        color = 'red'
        maze[goalX][goalY] = -1
        costPath += 1
        drawPosition(goalY, goalX, cursor, color)
        goalX, goalY = solution[goalX, goalY]
    drawPosition(b, a, cursor, 'green')

    show = "Cost of the path: " + str(costPath)
    print(show)
    print("Cost of the expanded nodes: " + str(costExpandedNode))


def UCS(startGoal, maze, size):
    solution = {}
    x, y = startGoal[0], startGoal[1]
    solution[x, y] = (x, y)  # backtrack
    costExpandedNode = 0
    goalState = False
    costList = np.ones([size[1]+1, size[0]+1], dtype=int)
    frontier = []
    frontier.append([x, y])

    while len(frontier) > 0:
        min = 100000
        index = -100000
        for i in range(len(frontier)):
            temp = frontier[i]
            if (costList[temp[1]][temp[2]] < min):
                min = costList[temp[1]][temp[2]]
                index = i
        currCell = frontier.pop(index)
        costExpandedNode += 1
        currX = currCell[0]
        currY = currCell[1]
        for i in range(4):
            adjacentX = currX + directionX[i]
            adjacentY = currY + directionY[i]
            if (adjacentY > size[0] + 1 or adjacentX > size[1]+1 or adjacentX < 0 or adjacentY < 0):
                continue
            if adjacentX == startGoal[0] and adjacentY == startGoal[1]:
                continue
            if (maze[adjacentX][adjacentY] == 0):
                frontier.append((adjacentX, adjacentY))
                costList[adjacentX][adjacentY] = costList[currX][currY] + 1
                solution[adjacentX, adjacentY] = (currX, currY)
                maze[adjacentX][adjacentY] = 1
                color = 'cyan'
                drawPosition(adjacentY, adjacentX, cursor, color)
            if adjacentX == startGoal[2] and adjacentY == startGoal[3]:
                solution[adjacentX, adjacentY] = (currX, currY)
                costList[adjacentX][adjacentY] = costList[currX][currY] + 1
                goalState = True
                break

        if (goalState == True):
            break

    costPath = 0
    goalX, goalY = startGoal[2], startGoal[3]
    a, b = goalX, goalY
    while(goalX, goalY) != (x, y):
        color = 'red'
        maze[goalX][goalY] = -1
        costPath += 1
        drawPosition(goalY, goalX, cursor, color)
        goalX, goalY = solution[goalX, goalY]
    drawPosition(b, a, cursor, 'green')

    print("Cost of the path (included the goal):", costPath)
    print("Cost of the expanded nodes:", costExpandedNode)
    print(costList)


def DFS(startGoal, maze, size):
    solution = {}
    x, y = startGoal[0], startGoal[1]
    solution[x, y] = (x, y)  # backtrack
    costExpandedNode = 0
    goalState = False
    frontier = []
    frontier.append((x, y))

    while len(frontier) > 0:
        currCell = frontier.pop()
        costExpandedNode += 1
        currX = currCell[0]
        currY = currCell[1]
        for i in range(4):
            adjacentX = currX + directionX[i]
            adjacentY = currY + directionY[i]
            if (adjacentY > size[0] + 1 or adjacentX > size[1]+1 or adjacentX < 0 or adjacentY < 0):
                continue
            if adjacentX == startGoal[0] and adjacentY == startGoal[1]:
                continue
            if (maze[adjacentX][adjacentY] == 0):
                frontier.append((adjacentX, adjacentY))
                solution[adjacentX, adjacentY] = (currX, currY)
                maze[adjacentX][adjacentY] = 1
                color = 'cyan'
                drawPosition(adjacentY, adjacentX, cursor, color)
            if maze[adjacentX][adjacentY] == 9:
                solution[adjacentX, adjacentY] = (currX, currY)
                goalState = True
                break
        if (goalState == True):
            break
    costPath = 0
    goalX, goalY = startGoal[2], startGoal[3]
    while(goalX, goalY) != (x, y):
        color = 'red'
        maze[goalX][goalY] = -1
        costPath += 1
        drawPosition(goalY, goalX, cursor, color)
        goalX, goalY = solution[goalX, goalY]
    drawPosition(startGoal[3], startGoal[2], cursor, 'green')

    # for i in range(size[1]+1):
    #     for j in range(size[0]+1):
    #         if (maze[i][j]) == -1:
    #             costPath += 1

    print("Cost of the path (included the goal):", costPath)
    print("Cost of the expanded nodes:", costExpandedNode)


def IDSwithDFS(startGoal, maze, size):
    solution = {}
    x, y = startGoal[0], startGoal[1]
    solution[x, y] = (x, y)  # backtrack
    expandedNode = 0
    goalState = False
    deepLevel = 0
    returnLevel = []

    while not goalState:
        expandedNode = 0
        levelList = np.zeros([size[1]+1, size[0]+1], dtype=int)
        frontierStack = []
        frontierStack.append((x, y))
        while len(frontierStack) > 0:
            currCell = frontierStack.pop()
            expandedNode += 1
            currX = currCell[0]
            currY = currCell[1]
            for i in range(4):
                adjacentX = currX + directionX[i]
                adjacentY = currY + directionY[i]
                # if levelList exceed deepLevel, break
                if (levelList[adjacentX][adjacentY] >= deepLevel):
                    break
                if (adjacentY > size[0] or adjacentX > size[1] or adjacentX < 1 or adjacentY < 1):
                    continue
                if (adjacentX == startGoal[0] and adjacentY == startGoal[1]):
                    continue
                if (maze[adjacentX][adjacentY] == 0 and levelList[adjacentX][adjacentY] == 0):
                    frontierStack.append([adjacentX, adjacentY])
                    levelList[adjacentX][adjacentY] = levelList[currX][currY] + 1
                    solution[adjacentX, adjacentY] = (currX, currY)
                    drawPosition(adjacentY, adjacentX, cursor, 'cyan')
                # reach goal
                if (adjacentX == startGoal[2] and adjacentY == startGoal[3]):
                    solution[adjacentX, adjacentY] = (currX, currY)
                    goalState = True
                    break
            # if goalState == True:
            #     break
        deepLevel += 1

    print(levelList)
    goalX, goalY = startGoal[2], startGoal[3]

    while(goalX, goalY) != (x, y):
        color = 'red'
        maze[goalX][goalY] = -1
        drawPosition(goalY, goalX, cursor, color)
        goalX, goalY = solution[goalX, goalY]
    drawPosition(startGoal[3], startGoal[2], cursor, 'green')

    costPath = 0
    for i in range(size[1]+1):
        for j in range(size[0]+1):
            if (maze[i][j]) == -1:
                costPath += 1

    print("Deep level: " + str(deepLevel))
    print("Cost of expanded nodes: " + str(expandedNode))
    print("Path cost: " + str(costPath))


def getManhattanDist(startGoal, currX, currY):
    return abs(currX - startGoal[2]) + abs(currY - startGoal[3])


def Astar(startGoal, maze, size):
    heuristicList = []
    frontier = []
    frontier.append((startGoal[0], startGoal[1]))
    solution = {}
    solution[(startGoal[0], startGoal[1])] = (startGoal[0], startGoal[1])
    costList = np.ones([size[1]+1, size[0]+1], dtype=int)
    goalState = False
    costExpandedNode = 0

    for i in range(1, size[1], 1):
        temp = []
        for j in range(1, size[0], 1):
            temp.append(getManhattanDist(startGoal, i, j))
        heuristicList.append(temp)

    while len(frontier) > 0:
        poppedVal = 0
        index = -100000
        indexHeuristic = 100000
        for i in range(len(frontier)):
            temp = heuristicList[frontier[i][0]][frontier[i]
                                                 [1]] + costList[frontier[i][0]][frontier[i][1]]
            if indexHeuristic > temp:
                indexHeuristic = temp
                index = i
        poppedVal = frontier[index]
        frontier.pop(index)

        currX, currY = poppedVal[0], poppedVal[1]
        for i in range(4):
            adjacentX = currX + directionX[i]
            adjacentY = currY + directionY[i]
            if (adjacentY > size[0] + 1 or adjacentX > size[1]+1 or adjacentX < 0 or adjacentY < 0):
                continue
            if adjacentX == startGoal[0] and adjacentY == startGoal[1]:
                continue
            if (maze[adjacentX][adjacentY] == 0):
                frontier.append((adjacentX, adjacentY))
                costExpandedNode += 1
                solution[adjacentX, adjacentY] = (currX, currY)
                maze[adjacentX][adjacentY] = 1
                color = 'cyan'
                drawPosition(adjacentY, adjacentX, cursor, color)
            if (adjacentX == startGoal[2] and adjacentY == startGoal[3]):
                solution[adjacentX, adjacentY] = (currX, currY)
                goalState = True
        if goalState == True:
            break

    costPath = 0
    goalX, goalY = startGoal[2], startGoal[3]
    a, b = goalX, goalY
    while(goalX, goalY) != (startGoal[0], startGoal[1]):
        color = 'red'
        drawPosition(goalY, goalX, cursor, color)
        maze[goalX][goalY] = -1
        costPath += 1
        goalX, goalY = solution[goalX, goalY]
    drawPosition(b, a, cursor, 'green')

    print("Cost of the path (included the goal):", costPath)
    print("Cost of the expanded nodes:", costExpandedNode)


def GBFS(startGoal, maze, size):
    heuristicList = []
    frontier = []
    heuristic = getManhattanDist(startGoal, startGoal[0], startGoal[1])
    goalState = False
    solution = {}
    solution[startGoal[0], startGoal[1]] = (startGoal[0], startGoal[1])
    costExpandedNode = 0

    for i in range(1, size[1], 1):
        temp = []
        for j in range(1, size[0], 1):
            temp.append(getManhattanDist(startGoal, i, j))
        heuristicList.append(temp)

    frontier.append((startGoal[0], startGoal[1]))

    while len(frontier) > 0:
        poppedVal = 0
        index = -100000
        indexHeuristic = 100000

        for i in range(len(frontier)):
            temp = heuristicList[frontier[i][0]][frontier[i][1]]
            if (indexHeuristic > temp):
                indexHeuristic = temp
                index = i
        poppedVal = frontier[index]
        frontier.pop(index)
        currX, currY = poppedVal[0], poppedVal[1]
        for i in range(4):
            adjacentX = currX + directionX[i]
            adjacentY = currY + directionY[i]
            if (adjacentY > size[0] + 1 or adjacentX > size[1]+1 or adjacentX < 0 or adjacentY < 0):
                continue
            if adjacentX == startGoal[0] and adjacentY == startGoal[1]:
                continue
            if (maze[adjacentX][adjacentY] == 0):
                frontier.append((adjacentX, adjacentY))
                costExpandedNode += 1
                solution[adjacentX, adjacentY] = (currX, currY)
                maze[adjacentX][adjacentY] = 1
                color = 'cyan'
                drawPosition(adjacentY, adjacentX, cursor, color)
            if (adjacentX == startGoal[2] and adjacentY == startGoal[3]):
                solution[adjacentX, adjacentY] = (currX, currY)
                goalState = True
        if goalState == True:
            break

    costPath = 0
    goalX, goalY = startGoal[2], startGoal[3]
    a, b = goalX, goalY
    while(goalX, goalY) != (startGoal[0], startGoal[1]):
        color = 'red'
        maze[goalX][goalY] = -1
        costPath += 1
        drawPosition(goalY, goalX, cursor, color)
        goalX, goalY = solution[goalX, goalY]
    drawPosition(b, a, cursor, 'green')

    print("Cost of the path (included the goal):", costPath)
    print("Cost of the expanded nodes:", costExpandedNode)


if __name__ == '__main__':
    print("1. BFS\n2. UCS\n3. IDS\n4. Greedy Best-first Search\n5. A*")
    userInput = int(input("Choose the Algorithm (1-5): "))
    if (userInput == 1):
        size, StartGoal, obstacle = readFile()
        maze = createMaze(size, StartGoal, obstacle)
        setupBoard()
        drawBoard(size, StartGoal, obstacle, maze)
        BFS(StartGoal, maze, size)
        screen.update()
        turtle.done()
    elif (userInput == 2):
        size, StartGoal, obstacle = readFile()
        maze = createMaze(size, StartGoal, obstacle)
        setupBoard()
        drawBoard(size, StartGoal, obstacle, maze)
        BFS(StartGoal, maze, size)
        screen.update()
        turtle.done()
    elif (userInput == 3):
        size, StartGoal, obstacle = readFile()
        maze = createMaze(size, StartGoal, obstacle)
        setupBoard()
        drawBoard(size, StartGoal, obstacle, maze)
        IDSwithDFS(StartGoal, maze, size)
        screen.update()
        turtle.done()
    elif (userInput == 4):
        size, StartGoal, obstacle = readFile()
        maze = createMaze(size, StartGoal, obstacle)
        setupBoard()
        drawBoard(size, StartGoal, obstacle, maze)
        GBFS(StartGoal, maze, size)
        screen.update()
        turtle.done()
    elif (userInput == 5):
        size, StartGoal, obstacle = readFile()
        maze = createMaze(size, StartGoal, obstacle)
        setupBoard()
        drawBoard(size, StartGoal, obstacle, maze)
        Astar(StartGoal, maze, size)
        screen.update()
        turtle.done()