from Piece import Piece


""" This is the class for the queen. It is a subclass of the Piece-class. When it updates it checks the diagonals, rows
and columns. Its MiniMax value is 9 and it is on position 4 in the inputs for the neural networks."""


class Queen(Piece):
    def __init__(self, pieceColor, row, column):
        super().__init__(pieceColor, ["\u2655", "\u265b"], "Q", row, column)
        self.inputPosition = 4
        self.miniMaxValue = 9

    def makeMove(self, row, column):
        self.row = row
        self.column = column

    def updatePossibleMoves(self, board):
        self.resetMoves()
        self.updateRowAndColumn(board)
        self.updateDiagonals(board)
