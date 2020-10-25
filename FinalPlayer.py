from ArtificialPlayer import *
from StrongMiniMaxEngine import *


""" This is the player that plays with a neural network. It has the StrongMiniMaxEngine. If openFile is True it opens
the neural network with the fileName. If it is False it creates an untrained network. movesAhead says how many moves it
will calculate ahead."""


class FinalPlayer(ArtificialPlayer):
    def __init__(self, openFile, fileName):
        super().__init__()
        self.engine = StrongMiniMaxEngine(self, openFile, fileName)
        self.movesAhead = 3

    """ This function makes a move. It first saves all the objects which are not needed in the calculations. After the
    calculation it resets them."""

    def makeMove(self, game):
        safe = self.safeNotCalculating(game)
        self.engine.calculateMiniMax(game, self.movesAhead)
        self.resetNotCalculating(game, safe)
        return self.engine.move
