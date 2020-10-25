from Player import Player
from Queen import Queen


""" This is the parent class for all artificial players."""


class ArtificialPlayer(Player):
    def __init__(self):
        super().__init__(True)

    """ If any artificial player has to choose a new piece it just chooses a queen because in most cases it's the best
    option. """

    def chooseNewPiece(self, row, column):
        return Queen(self.playerColor, row, column)

    """ This function returns saves of the list with the captured pieces because they are not necessary in the 
    calculations. Also the observers get saved because otherwise they would get notified."""

    def safeNotCalculating(self, game):
        safe = (game.observers, game.board.whiteOutPieces, game.board.blackOutPieces)
        game.observers = []
        game.board.whiteOutPieces = []
        game.board.blackOutPieces = []
        return safe

    """ This resets the copies of the observers and the lists with the captured pieces."""

    def resetNotCalculating(self, game, safe):
        game.observers, game.board.whiteOutPieces, game.board.blackOutPieces = safe
