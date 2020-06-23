def coordToRowCol(coord):
    """
    centre of grid is origin
    """
    row = 1 - coord[1]
    col = 1 + coord[0]
    return row, col
    
def rowColToCoord(row, col):
    """
    centre of grid is origin
    """
    x = col - 1
    y = 1 - row
    return (x, y)

def numberToCoord(n):
    """
    returns a number 0, ..., 8 to a coord on a 3x3 board
    """
    return rowColToCoord(int(n / 3), n - 3 * int(n / 3))


def emptyGrid():
    return [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]
            ]

class Board:
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
    
    def atCoord(self, coord):
        r, c = coordToRowCol(coord)
        return self.grid[r][c]

    def availableCoords(self):
        coords = []
        for r in range(3):
            for c in range(3):
                if self.grid[r][c] == 0:
                    coords.append(rowColToCoord(r, c))
        return coords

    def isFull(self):
        return self.availableCoords() == []

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

    def makeMove(self, coord, playerID):
        r, c = coordToRowCol(coord)
        if self.grid[r][c] != 0:
            raise ValueError("Tried to erase someone's move")
        self.grid[r][c] = playerID
    
    def encoding(self):
        encoding = 0
        for r in range(3):
            for c in range(3):
                exponent = 3 * r + c
                encoding += self.grid[r][c] * (3 ** exponent)
        return encoding