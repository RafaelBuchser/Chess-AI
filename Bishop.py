from Piece import Piece


""" This is the class for the bishop. It is a subclass of the Piece-class. When it updates it only checks the diagonals.
Its minimax value is 3 and it is on position 2 in the inputs for the neural networks."""


class Bishop(Piece):
    def __init__(self, pieceColor, row, column):
        super().__init__(pieceColor, ["\u2657", "\u265d"], "B", row, column)
        self.inputPosition = 2
        self.miniMaxValue = 3

    def makeMove(self, row, column):
        self.row = row
        self.column = column

    def updatePossibleMoves(self, board):
        self.resetMoves()
        self.updateDiagonals(board)
