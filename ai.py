from util import before, after, between
from board import Board
import random
from math import ceil
from standardiser import *

class Choice:
    def __init__(self, encodingBeforeMove, priorChosen, playerID):
        self.encoding = encodingBeforeMove
        self.prior = priorChosen
        self.playerID = playerID


class Prior:
    def __init__(self, alpha, beta, pos):
        self.alpha = alpha
        self.beta = beta
        self.pos = pos
    
    @classmethod
    def fromString(cls, string):
        alpha, beta = [
            float(x) for x in before(string, " (").split(", ")]
        pos = [
            int(x) for x in between(string, " (", ")").split(", ")]
        
        return cls(alpha, beta, pos)

    def __str__(self):
        return "{0}, {1} ({2}, {3})".format(
            self.alpha,
            self.beta,
            self.pos[0],
            self.pos[1]
        )
    
    def mean(self):
        return self.alpha / (self.alpha + self.beta)
    
    def update(self, datum, n):
        return Prior(self.alpha + datum, self.beta + n - datum, self.pos)

    def __eq__(self, other):
        return self.alpha == other.alpha and self.beta == other.beta and self.pos == other.pos

class Learner:
    maxIntensity = 5
    whenToPlaySmart = 3 * 10 ** 4
    saveInterval = 10 ** 2
    priorsFile = "priors.txt"

    def __init__(self):
        self.encodingToPriors = self.readPriors()
        self.amountOfData = self.readAmountOfData()
        self.movesMade = []

    def printPriors(self):
        for encoding, priors in self.encodingToPriors.items():
            print()

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
        13072: 0.5, 0.5; 0.2, 0.7; 1.2, 0.3
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
    
    def writePriors(self):
        with open(Learner.priorsFile, "w") as f:
            f.write(str(self.amountOfData) + "\n")
            f.write(self.priorsToString())

    def bestPrior(self, priors):
        bestPrior = priors[0]
        for prior in priors[1 : ]:
            if prior.mean() > bestPrior.mean():
                bestPrior = prior

    def choosePositionRandomly(self, board):
        return random.choice(board.availablePositions())

    def choosePosition(self, board, playerID):
        action = standardisingAction(board.grid)
        stdGrid = actionOnGrid(action, board.grid)
        stdEncoding = encode(stdGrid)

        prior = self.choosePrior(stdGrid, stdEncoding)
        self.movesMade.append(Choice(stdEncoding, prior, playerID))
        pos = motionOnPos(inverseAction(action))(prior.pos)
        return pos

    def addUnbiasedPriors(self, stdGrid, stdEncoding):
        stdPositions = Board(stdGrid).availablePositions()
        priors = []
        for stdPos in stdPositions:
            priors.append(Prior(0.5, 0.5, stdPos))
        self.encodingToPriors[stdEncoding] = priors 

    def choosePrior(self, stdGrid, stdEncoding):
        if stdEncoding not in self.encodingToPriors.keys():
            self.addUnbiasedPriors(stdGrid, stdEncoding)

        if self.amountOfData >= Learner.whenToPlaySmart:
            priors = self.encodingToPriors[stdEncoding]
            return self.bestPrior(self.encodingToPriors[stdEncoding])
        else:
            return random.choice(self.encodingToPriors[stdEncoding])
            
    def learnAfterGame(self, winners):
        for i in range(len(self.movesMade)):
            move = self.movesMade[i]
            datum = 1 if move.playerID in winners else 0
            intensity = ceil(Learner.maxIntensity * i / len(self.movesMade))

            priors = self.encodingToPriors[move.encoding]
            idx = priors.index(move.prior)

            self.encodingToPriors[move.encoding][idx] = priors[idx].update(datum, intensity)
            self.amountOfData += intensity
        self.movesMade = []
    

