from MiniMaxEngine import MiniMaxEngine
from King import King


""" This class is a subclass of the MiniMax-engine. The only difference between the other engine is the
evaluation function. To evaluate a position it just adds up the values of the pieces. The more pieces from the opposite
player are missing the higher evaluated it gets and the more piece from the own player are missing the lower the value
gets."""


class WeakMiniMaxEngine(MiniMaxEngine):
    def __init__(self, player):
        super().__init__(player)

    def calculateValueOfMove(self, game):
        gameValue = 0
        for row in range(8):
            for column in range(8):
                piece = game.board.board[row][column]
                if piece is not None:
                    if not isinstance(piece, King):
                        gameValue += self.getValueOfPiece(piece)
        return gameValue

    def getValueOfPiece(self, piece):
        value = piece.miniMaxValue
        return value if piece.pieceColor == self.player.playerColor else -value
