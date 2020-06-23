import random
from mathsyStuff import numberToCoord
from board import Board, numberToCoord
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

def moveChoice(player, board):
    if player.nature == Player.ai:
        # pretty
        ai.printUncertainties(board, player.id)
        return ai.choosePosition(board, player.id)
    elif player.nature == Player.random:
        return random.choice(board.availableCells())
    elif player.nature == Player.human:
        board.print()
        coord = None
        while coord == None or coord not in board.availableCoords():
            n = int(input("\n{0} Where would you like to move?\t".format(player))) - 1
            coord = numberToCoord(n)
        return coord

def winners(player1, player2):
    """
    player1 plays first. assume player1.id == 1, player2.id == 2
    """
    board = Board()
    while True:
        for player in [player1, player2]:
            board.makeMove(moveChoice(player, board), player.id)
            if board.isWinningBoard():
                return [player.id]
            elif board.isFull():
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
    
def playAIvsPlayer():
    ai.whenToPlaySmart = 0
    print("Positions are numbered 1 to 9, going across and downwards. \nE.g. if you wanted to go to this position")
    Board([
        [0, 0, 0],
        [1, 0, 0],
        [0, 0, 0]
    ]).print()
    print("you'd type in 4 when asked.\n\n")

    humanPlayer = Player(
        Player.human, 
        input("What would you like to be called?\t"), 
        1 if "y" in input("Would you like to go first?\t").lower() else 2
    )
    aiPlayer = Player(Player.ai, "Mr Robot", 3 - humanPlayer.id)
    players = [humanPlayer, aiPlayer]
    players.sort(key = lambda p:    p.id)

    wins = winners(*players)
    if len(wins) == 2:
        print("It's a tie :/")
    else:
        print(str([p for p in [humanPlayer, aiPlayer] if p.id == wins[0]][0]), "has won!")

playAIvsPlayer()
