from board import *

class SquareMatrix:
    @classmethod
    def identity(cls, dimemsion = 2):
        """
        only bothering for 2x2 case
        """
        return cls([
            [1, 0],
            [0, 1]
        ])

    @classmethod
    def dot(cls, vect1, vect2):
        return sum([vect1[i] * vect2[i] for i in range(len(vect1))])

    def __init__(self, rows):
        self.rows = rows
        self.dim = len(self.rows)
    
    def __str__(self):
        string = ""
        for row in self.rows:
            for x in row:
                string += str(x) + "\t"
            string += "\n"
        return string
    
    def row(self, r):
        return self.rows[r]
    
    def col(self, c):
        return [self.rows[r][c] for r in range(self.dim)]
    
    def __rmul__(self, scalar):
        return SquareMatrix([
            [scalar * self.rows[r][c] for c in range(self.dim)]
                for r in range(self.dim)
        ])
    
    def __matmul__(self, other):
        if type(other) == SquareMatrix:
            return self.actOnMatrix(other)
        else:
            return self.actOnVector(other)
    
    def actOnVector(self, vector):
        return [SquareMatrix.dot(self.row(r), vector) for r in range(self.dim)]
    
    def transpose(self):
        return SquareMatrix([
            [self.rows[c][r] for c in range(self.dim)] 
                for r in range(self.dim)
        ])

    def actOnMatrix(self, matrix):
        return SquareMatrix([
            self.actOnVector(matrix.col(c)) for c in range(matrix.dim)
        ]).transpose()
    
    def det(self):
        """
        case of 2x2 matrix
        """
        return self.rows[0][0] * self.rows[1][1] - self.rows[0][1] * self.rows[1][0]

    def inverse(self):
        """
        case of 2x2 matrix
        """
        if self.det() == 0:
            raise ValueError("Trying to find the inverse of {0}, which does not exist".format(str(self)))
            return 1 / 0
        else:
            invDet = 1 / self.det()
            if 1 / self.det() == int(1/self.det()):
                invDet = int(invDet)
            
            return invDet * SquareMatrix([
                [self.rows[1][1], -self.rows[0][1]],
                [-self.rows[1][0], self.rows[0][0]]
            ])

class Transformation:
    @classmethod
    def integerSin(cls, multOf90):
        """
        returns only 0, 1, 0, -1, ...
        """
        k = int(multOf90 / 90)
        return 0 if k % 2 == 0 else (-1) ** int((k - 1) / 2)

    @classmethod
    def integerCos(cls, multOf90):
        """
        returns only 1, 0, -1, 0, ...
        """
        k = int(multOf90 / 90)
        return 0 if k % 2 != 0 else (-1) ** int(k / 2)

    reflect45 = SquareMatrix([
        [0, 1],
        [1, 0]
    ])
    
    @classmethod
    def rotationMatrix(cls, angle):
        c = cls.integerCos(angle)
        s = cls.integerSin(angle)
        return SquareMatrix([
            [c, -s], 
            [s, c]
        ])
    
    @classmethod
    def swapPlayerIdx(cls, num):
        if num == 2:
            return 1
        if num == 1:
            return 2
        return num
    
    @classmethod
    def identity(cls):
        return cls.fromProperties(0, False, False)
    
    @classmethod
    def fromProperties(cls, rotationAngle, reflect, swap):
        matrix = cls.reflect45 @ cls.rotationMatrix(rotationAngle) if reflect else cls.rotationMatrix(rotationAngle)
        return cls(matrix, swap)

    def __init__(self, matrix, swap):
        self.matrix = matrix
        self.swap = swap
    
    def onCoord(self, coord):
        """
        Note that this has no way to swap pieces
        """
        return self.matrix @ coord

    def onBoard(self, board):
        newBoard = Board()
        for y in [1, 0, -1]:
            for x in [-1, 0, 1]:
                pieceAtxy = board.atCoord((x, y))
                imgCoord = self.onCoord((x, y))
                if pieceAtxy != 0:
                    newBoard.makeMove(imgCoord, pieceAtxy)
        return newBoard
    
    def inverse(self):
        return Transformation(self.matrix.inverse(), self.swap)

def pad(num, digits):
    numAsString = str(float(num))
    amountOfZeroes = max(digits - len(numAsString.replace(".", "")), 0)
    return numAsString[0 : digits] + "0" * amountOfZeroes

def elSuchThat(list, condition):
    elsThatMatchCondition = [x for x in list if condition(x)]
    return elsThatMatchCondition[0] if elsThatMatchCondition else None