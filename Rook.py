from Piece import*


""" This is the class for the rook. It is a subclass of the Piece-class. When it updates it only checks the rows and
columns. Its minimax value is 5 and it is on position 3 in the inputs for the neural networks."""


class Rook(Piece):
    def __init__(self, pieceColor, row, column):
        super().__init__(pieceColor, ["\u2656", "\u265c"], "R", row, column)
        self.onStartingField = True
        self.inputPosition = 3
        self.miniMaxValue = 5

    def makeMove(self, row, column):
        self.row = row
        self.column = column
        self.onStartingField = False

    def updatePossibleMoves(self, board):
        self.resetMoves()
        self.updateRowAndColumn(board)
