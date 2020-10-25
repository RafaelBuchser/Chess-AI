from Piece import Piece


""" This is the class for the king and it is a subclass of the Piece. It has and input position of 5 and has no minimax-
value because it is not necessary. When it updates it checks only the surrounding fields. But these fields cannot be
attacked. It has to be updated at last, because its moves depend on the moves from the other pieces."""


class King(Piece):
    def __init__(self, pieceColor, row, column):
        super().__init__(pieceColor, ["\u2654", "\u265a"], "K", row, column)
        self.onStartingField = True
        self.inputPosition = 5

    def makeMove(self, row, column):
        self.row = row
        self.column = column
        self.onStartingField = False

    def updatePossibleMoves(self, board, moves, kings):
        self.resetMoves()
        self.findField(board, moves, kings)

    """ This function finds all the fields where the king can move to. These are all which are only one field away. Then
    it calls the function which checks if the move to this field is possible."""

    def findField(self, board, kings, moves):
        for endRow in range(self.row - 1, self.row + 2):
            for endColumn in range(self.column - 1, self.column + 2):
                if not (endRow == self.row and endColumn == self.column):
                    self.checkField(endRow, endColumn, board, moves, kings)

    """ This function checks if a move is possible. It checks if the field is under attack and if the other king is not
    in the range of attacking him."""

    def checkField(self, endRow, endColumn, board, moves, kings):
        if self.checkFieldInBoard(endRow, endColumn):
            if not self.checkFieldUnderAttack(endRow, endColumn, moves):
                if not self.checkForOtherKing(endRow, endColumn, kings):
                    self.setFieldToLists(board, endRow, endColumn, endRow, endColumn)

    """ This function checks if a certain field is attacked."""

    def checkFieldUnderAttack(self, row, column, moves):
        for move in moves:
            if move[2][0] == row and move[2][1] == column:
                return True
        return False

    """ This function checks if the other king is only one field away from a certain field."""

    def checkForOtherKing(self, row, column, kings):
        for king in kings:
            if king != self:
                if abs(king.row-row) in [0, 1] and abs(king.column-column) in [0, 1]:
                    return True
        return False
