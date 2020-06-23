from util import before, after, between
import random, math
from mathsyStuff import pad
from standardiser import standardTransformation


class Choice:
    def __init__(self, encodingBeforeMove, priorChosen, playerID):
        self.encoding = encodingBeforeMove
        self.prior = priorChosen
        self.playerID = playerID
    
    def __str__(self):
        return "{0} ({1}): {2}".format(self.encoding, self.playerID, str(self.prior))
    
class Prior:
    def __init__(self, alpha, beta, coord):
        self.alpha = alpha
        self.beta = beta
        self.coord = coord
    
    @classmethod
    def fromString(cls, string):
        alpha, beta = [float(x) for x in before(string, " (").split(", ")]
        coord = [int(x) for x in between(string, " (", ")").split(", ")]
        
        return cls(alpha, beta, coord)

    def __str__(self):
        return "{0}, {1} ({2}, {3})".format(
            self.alpha,
            self.beta,
            self.coord[0],
            self.coord[1]
        )
    
    def mean(self):
        return self.alpha / (self.alpha + self.beta)
    
    def update(self, datum):
        return Prior(self.alpha + datum, self.beta + 1 - datum, self.coord)

    def __eq__(self, other):
        return self.alpha == other.alpha and self.beta == other.beta and self.coord == other.coord

class Learner:
    possibleStdBoards = int((3 ** 9) / 8)
    whenToPlaySmart = 20 * possibleStdBoards
    whenToStop = 60 * possibleStdBoards
    saveInterval = 100
    priorsFile = "priors.txt"

    def __init__(self):
        self.encodingToPriors = self.readPriors()
        self.amountOfData = self.readAmountOfData()
        self.movesMade = []

    def readAmountOfData(self):
        """
        amount of data is in first line
        """
        with open(Learner.priorsFile, "r") as f:
            return int(f.readline())

    def readPriors(self):
        """
        first line is amount of data, so is ignored

        lines are of format
        13072: <prior>; <prior>; <prior>
        """
        encodingToPriors = {}
        with open(Learner.priorsFile, "r") as f:
            for line in f.readlines()[1 : ]:
                encoding = int(before(line, ": "))
                priorsBit = after(line, ": ")
                encodingToPriors[encoding] =  [Prior.fromString(bit) for bit in priorsBit.split("; ")]
            return encodingToPriors
    
    def priorsToString(self):
        string = ""
        for encoding, priors in self.encodingToPriors.items():
            string += str(encoding) + ": "
            
            for i in range(len(priors)):
                string += str(priors[i])
                if i + 1 < len(priors):
                    string += "; "
            string += "\n"

        return string 
    
    def writeData(self):
        with open(Learner.priorsFile, "w") as f:
            f.write(str(self.amountOfData) + "\n")
            f.write(self.priorsToString())

    def choosePosition(self, board, playerID):
        """
            board 
                |--(matrix)-->               stdBoard 
                |--(choose best prior)-->    stdPos
                |--(matrix^-1)-->            pos 
        """

        transToStd = standardTransformation(board, playerID)
        stdBoard = transToStd.onBoard(board)
        prior = self.choosePrior(stdBoard)
        self.movesMade.append(Choice(stdBoard.encoding(), prior, playerID))
        pos = transToStd.inverse().onCoord(prior.coord)
        return pos
    
    def choosePrior(self, stdBoard):
        encoding = stdBoard.encoding()

        if encoding not in self.encodingToPriors.keys():
            self.setUnbiasedPriors(stdBoard)

        if self.amountOfData < self.whenToPlaySmart:
            return random.choice(self.encodingToPriors[encoding])
        else:
            return self.bestPrior(self.encodingToPriors[encoding]) 
    
    def setUnbiasedPriors(self, board):
        priors = [Prior(0.5, 0.5, coord) for coord in board.availableCoords()]
        self.encodingToPriors[board.encoding()] = priors

    def bestPrior(self, priors):
        bestPrior = priors[0]
        for prior in priors[1 : ]:
            if prior.mean() > bestPrior.mean():
                bestPrior = prior
        return bestPrior

    def learnAfterGame(self, winners):
        for choice in self.movesMade:
            datum = 1 if choice.playerID in winners else 0

            priors = self.encodingToPriors[choice.encoding]
            idx = priors.index(choice.prior)

            self.encodingToPriors[choice.encoding][idx] = priors[idx].update(datum)
            self.amountOfData += 1
        self.movesMade = []
    
    def printUncertainties(self, board, playerID):
        transToStd = standardTransformation(board, playerID)
        stdBoard = transToStd.onBoard(board)
        for y in [1, 0, -1]:
            for x in [-1, 0, 1]:
                priors = [p for p in self.encodingToPriors[stdBoard.encoding()] if p.coord == (x, y)]
                if priors == []:
                    print("___", end = "  ")
                else:
                    print(pad(100 * priors[0].mean(), 3) + "%", end = "  ")
        print()