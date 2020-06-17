def emptyGrid():
    return [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0]
        ]

class Board:
    """ 
    I have sacrified good design (checking if a move is valid, using functions in other functions, etc) for efficiency
    """

    idToSymbol = {
        0:  " ",
        1:  "x",
        2:  "o"
    }

    def __init__(self, grid = None):
        self.grid = grid if grid else emptyGrid()
    
    def print(self):
        for r in range(3):
            for c in range(3):
                print("|" + Board.idToSymbol[self.grid[r][c]], end = "")
            print("|")
    
    def availablePositions(self):
        positions = []
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] == 0:
                    positions.append((r, c))
        return positions
    
    def swapIDs(self):
        swappedIDsGrid = emptyGrid()
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] != 0:
                    swappedIDsGrid[r][c] = 3 - self.grid[r][c]
        return Board(swappedIDsGrid)

    def isFull(self):
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] == 0:
                    return False
        return True
    
    def isWinningBoard(self):
        # horizontal / vertical win
        for x in range(3):
            # horizontal win
            if self.grid[x][0] != 0 and self.grid[x][0] == self.grid[x][1] == self.grid[x][2]:
                return True 
            # vertical win
            if self.grid[0][x] != 0 and self.grid[0][x] == self.grid[1][x] == self.grid[2][x]:
                return True
        # left / right diagonal win
        if self.grid[1][1] != 0:
            # left -> right diagonal win
            if self.grid[0][0] == self.grid[1][1] == self.grid[2][2]:
                return True
            # right -> left diagonal win
            if self.grid[0][2] == self.grid[1][1] == self.grid[2][0]:
                return True

    def makeMove(self, point, playerID):
        self.grid[point[0]][point[1]] = playerID
    