from ArtificialPlayer import ArtificialPlayer
from WeakMiniMaxEngine import WeakMiniMaxEngine


""" This class is the player which works with the MiniMax engine. It has the WeakMiniMaxEngine. It calculates the value
of the move with how many pieces it captured and how many pieces it lost."""


class MiniMaxPlayer(ArtificialPlayer):
    def __init__(self):
        super().__init__()
        self.engine = WeakMiniMaxEngine(self)
        self.movesAhead = 4

    """ This function saves the objects that can't or don't need to be copied. Then it lets the engine calculate with
    the game and a copy of the game. Then it resets these objects and returns the calculated move."""

    def makeMove(self, game):
        safe = self.safeNotCalculating(game)
        self.engine.calculateMiniMax(game, self.movesAhead)
        self.resetNotCalculating(game, safe)
        return self.engine.move
