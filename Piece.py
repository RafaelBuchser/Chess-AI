""" This is the parent class for all the pieces. It has a color, a shortcut, a letter and a row and a column. Every
piece has its possible and attacking moves. If it is between an attacker and the king it is set to a state where it can
only move in a certain line. """


class Piece:
    def __init__(self, pieceColor, shortCut, letter, row, column):
        self.pieceColor = pieceColor
        self.shortCut = shortCut
        self.letter = letter
        self.row = row
        self.column = column
        self.possibleMoves = []
        self.attackingMoves = []
        self.inBetweenAttackerAndKing = False
        self.possibleMovingLine = None

    def resetMoves(self):
        self.possibleMoves = []
        self.attackingMoves = []

    def checkFieldInBoard(self, row, column):
        return True if 0 <= row <= 7 and 0 <= column <= 7 else False

    """ This checks if there is a piece from the same color on a certain field. """

    def checkEndSameColor(self, row, column, board):
        if board[row][column] is not None:
            if board[row][column].pieceColor == self.pieceColor:
                return True
        return False

    """ This function checks if the ending field has a piece from the same color. If this is false it sets the move to
    the possible moves. And it always sets the move to the attacking moves."""

    def setFieldToLists(self, board, endRow, endColumn, attackingRow, attackingColumn):
        if not self.checkEndSameColor(endRow, endColumn, board):
            self.possibleMoves.append([[self.row, self.column], [endRow, endColumn]])
        self.attackingMoves.append([[self.row, self.column], [endRow, endColumn], [attackingRow, attackingColumn]])

    """Because the queen, the rook and the bishop work similarly they need the same functions. They are only used for 
    them. They iterate through the whole diagonal, row or column until they find a piece in its way. If the piece is
    from the different color it continues iterating until the next piece. If its a the opponents king it will set the
    first piece to a state where it can only move in this row/column/diagonal."""

    def updateRowAndColumn(self, board):
        self.updateDirection(board, 0, -1)
        self.updateDirection(board, 0, 1)
        self.updateDirection(board, -1, 0)
        self.updateDirection(board, 1, 0)

    def updateDiagonals(self, board):
        self.updateDirection(board, -1, -1)
        self.updateDirection(board, -1, 1)
        self.updateDirection(board, 1, -1)
        self.updateDirection(board, 1, 1)

    def updateDirection(self, board, rowDirection, columnDirection):
        endRow = self.row + rowDirection
        endColumn = self.column + columnDirection
        firstPiece = None
        counter = 0
        line = [[self.row, self.column]]
        while self.checkFieldInBoard(endRow, endColumn):
            line.append([endRow, endColumn])
            if counter == 0:
                self.setFieldToLists(board, endRow, endColumn, endRow, endColumn)
            piece = board[endRow][endColumn]
            if piece is not None:
                if counter == 0:
                    firstPiece = piece
                elif counter == 1:
                    self.checkSecondPieceKing(piece, firstPiece, line)
                if piece.pieceColor == self.pieceColor:
                    break
                counter += 1
            if counter == 2:
                break
            endRow += rowDirection
            endColumn += columnDirection

    """ This function checks if a piece is a king and sets the first piece to a state where it can only move to certain
    fields."""

    def checkSecondPieceKing(self, piece, firstPiece, line):
        if (piece.letter == "K") and piece.pieceColor != self.pieceColor:
            firstPiece.setInBetweenAttackerAndKing(line)

    """ This function is called when a piece is between an attacker and the king. Then it can not move away from this
    row/column/diagonal. """

    def updateInBetweenAttackerAndKing(self):
        self.possibleMoves = self.updateMovesInBetween(self.possibleMoves)
        self.attackingMoves = self.updateMovesInBetween(self.attackingMoves)

    """ This function checks if the moves are in the line where the piece can move to. if that is the case it appends
    the move to the list."""

    def updateMovesInBetween(self, moves):
        movesCopy = moves
        moves = []
        for move in movesCopy:
            if move[1] in self.possibleMovingLine:
                moves.append(move)
        return moves

    def setInBetweenAttackerAndKing(self, line):
        self.inBetweenAttackerAndKing = True
        self.possibleMovingLine = line

    def resetInBetweenAttackerAndKing(self):
        self.inBetweenAttackerAndKing = False
        self.possibleMovingLine = []

    def getLetters(self):
        return self.pieceColor[0] + self.letter

    def __str__(self):
        return self.shortCut[1] if self.pieceColor == "black" else self.shortCut[0]
