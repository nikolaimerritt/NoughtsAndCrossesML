import random
from board import Board
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
        natureString = None 
        if self.nature == Player.ai:
            natureString = "(AI)"
        elif self.nature == Player.human:
            natureString = "(Human)"
        elif self.nature == Player.random:
            natureString = "(Random)"
        return self.name + " (" + Board.idToSymbol[self.id] + ") " + natureString

def moveChoice(player, board):
    if player.nature == Player.ai:
        # ai always plays with id = 1
        if player.id != 1:
            board = board.swapIDs()
        return ai.choosePosition(board, player.id)
    elif player.nature == Player.random:
        return random.choice(board.availableCells())
    elif player.nature == Player.human:
        board.print()
        response = input("\n({0}) Where would you like to move? ".format(Board.idToSymbol[player.id]))
        return [int(cell) for cell in response.split(", ")]

def winners(player1, player2):
    """
    player1 plays first. assume player1.id == 1, player2.id == 2
    """
    board = Board()
    while True:
        for player in [player1, player2]:
            board.makeMove(moveChoice(player, board), player.id)
            if board.isFull():
                if player1.nature == Player.human or player2.nature == Player.human:
                    print("full board")
                return [1, 2]
            elif board.isWinningBoard():
                if player1.nature == Player.human or player2.nature == Player.human:
                    print(str(player), "has won")
                return [player.id]

def play():
    player1 = Player(Player.ai, "Nick", 1)
    player2 = Player(Player.ai, "James", 2)
    maxGames = 3 * Learner.whenToPlaySmart
    for i in range(maxGames):
        ai.learnAfterGame(winners(player1, player2))
        if (i + 1) % Learner.saveInterval == 0:
            print(i + 1)
            ai.writePriors()

play()
