import random, time, os
from mathsyStuff import cellNumberToCoord, elSuchThat
from board import Board, cellNumberToCoord
from ai import Learner

ai = Learner()

class Player:
    ai = 0
    human = 1
    random = 2
    def __init__(self, nature, name, id):
        self.nature = nature 
        self.name = name 
        self.id = id
    
    def __str__(self):
        natureString = "(Human)" if self.nature == Player.human else "(AI)"
        return self.name + " (" + Board.idToSymbol[self.id] + ") " + natureString

def moveChoice(player, board, verbose):
    if player.nature == Player.ai:
        if verbose:
            os.system("clear")
            print("\n\n\n")
            board.print()
            print(str(player), "is thinking...")
            time.sleep(1)
            ai.printUncertainties(board, player.id)
            time.sleep(3.5)
            print("\n\n")
        return ai.choosePosition(board, player.id)
    elif player.nature == Player.random:
        return random.choice(board.availableCells())
    elif player.nature == Player.human:
        board.print()
        coord = None
        while coord == None or coord not in board.availableCoords():
            cellNumber = int(input("\n{0} Where would you like to move?\t".format(player))) - 1
            coord = cellNumberToCoord(cellNumber)
        return coord

def winners(player1, player2, verbose = False):
    """
    player1 plays first. assume player1.id == 1, player2.id == 2
    """
    board = Board()
    while True:
        for player in [player1, player2]:
            board.makeMove(moveChoice(player, board, verbose), player.id)
            if board.isWinningBoard():
                if verbose:
                    board.print()
                return [player.id]
            elif board.isFull():
                if verbose:
                    board.print()
                return [1, 2]

def playAIvsAI():
    player1 = Player(Player.ai, "Nick", 1)
    player2 = Player(Player.ai, "James", 2)
    winners(player1, player2)

    gamesPlayed = 0
    while ai.amountOfData < ai.whenToStop:
        ai.learnAfterGame(winners(player1, player2))
        gamesPlayed += 1
        if (gamesPlayed + 1) % Learner.saveInterval == 0:
            ai.writeData()
    
def playAIvsPlayer(verbose = True):
    ai.whenToPlaySmart = 0
    if verbose:
        os.system("clear")
        print("\n\n\nPositions are numbered 1 to 9, starting at the top left and going across. \nE.g. if you wanted to go to the (x) position")
        Board([
            [0, 0, 0],
            [1, 0, 0],
            [0, 0, 0]
        ]).print()
        print("you'd type in 4 when asked.\n\n")
        time.sleep(5)

    humanPlayer = Player(
        Player.human, 
        input("What would you like to be called?\t"), 
        1 if "y" in input("Would you like to go first?\t").lower() else 2
    )

    if verbose:
        os.system("clear")
        print("\n\n\n")

    aiPlayer = Player(Player.ai, "Bayes", 3 - humanPlayer.id)
    players = [humanPlayer, aiPlayer]
    players.sort(key = lambda p:    p.id)

    wins = winners(*players, verbose)
    if verbose:
        if len(wins) == 2:
            print("It's a tie :/")
        else:
            winner = elSuchThat(players, lambda p:  p.id in wins)
            print(str(winner), "has won!")

playAIvsPlayer()
while "n" not in input("Go again? \t").lower():
    playAIvsPlayer()