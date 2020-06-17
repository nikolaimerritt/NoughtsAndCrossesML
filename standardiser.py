from board import emptyGrid
"""
action: AMOUNT of rotation and transposition (pair of ints)
motion: rotations composed with transpositions (function) of a given (r, c) pair
motion on board: motion applied to whole board
"""
def encode(grid):
    encoding = 0
    for r in range(3): 
        for c in range(3):
            encoding += grid[r][c] * (3 ** (3 * r + c))
    return encoding

def compose(g, f):
    return lambda x:    g(f(x))

def identity(point):
    return point

def rotate90(point):
    return (2 - point[1], point[0])

def transpose(point):
    return (point[1], point[0])

def power(function, index):
    if index == 0:
        return identity
    else:
        return compose(function, power(function, index - 1))

def motionOnPos(action):
    rotations, transpositions = action
    return compose(
        power(rotate90, rotations), 
        power(transpose, transpositions)
    )

def motionOnGrid(motion, grid):
    movedGrid = emptyGrid()
    for r in range(3):
        for c in range(3):
            movedR, movedC = motion((r, c))
            movedGrid[r][c] = grid[movedR][movedC]
    return movedGrid

def actionOnGrid(action, grid):
    return motionOnGrid(motionOnPos(action), grid)

def standardisingAction(grid):
    minEncoding = encode(grid)
    minAction = (0, 0)
    for r in [1, 2, 3]:
        for t in [0, 1]:
            if encode(actionOnGrid((r, t), grid)) < minEncoding:
                minAction = (r, t)
    return minAction

def inverseAction(action):
    rotations, transpositions = action
    return (
        (4 - rotations) % 4, 
        (2 - transpositions) % 2
    )
