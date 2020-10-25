from Piece import Piece


""" This is the class for the knight and a subclass of the piece. The minimax-value is 3 and the input position is at 1.
When it updates it checks the fields which are 2 fields in one direction and 1 field in the other direction away. It
does not need to have an open way."""


class Knight(Piece):
    def __init__(self, pieceColor, row, column):
        super().__init__(pieceColor, ["\u2658", "\u265e"], "N", row, column)
        self.inputPosition = 1
        self.miniMaxValue = 3

    def makeMove(self, row, column):
        self.row = row
        self.column = column

    def updatePossibleMoves(self, board):
        self.resetMoves()
        self.checkFirstDirection(board)
        self.checkSecondDirection(board)

    def checkFirstDirection(self, board):
        for endRow in [self.row - 2, self. row + 2]:
            for endColumn in [self.column - 1, self.column + 1]:
                self.checkFieldPossible(endRow, endColumn, board)

    def checkSecondDirection(self, board):
        for endRow in [self.row - 1, self. row + 1]:
            for endColumn in [self.column - 2, self.column + 2]:
                self.checkFieldPossible(endRow, endColumn, board)

    def checkFieldPossible(self, endRow, endColumn, board):
        if self.checkFieldInBoard(endRow, endColumn):
            self.setFieldToLists(board, endRow, endColumn, endRow, endColumn)
