from Piece import Piece


""" This is the class for the pawn. It is a subclass of the Piece. Its MiniMax-value is 1 and the input position is 0. A
pawn has three variable more than a normal piece. The direction tells in which direction the pawn is moving. The
onStartingField-variable tells if the pawn has moved yet. And the firstLongMove-variable tells if it has made a long
move in the last move."""


class Pawn(Piece):
    def __init__(self, pieceColor, row, column):
        super().__init__(pieceColor, ["\u2659", "\u265f"], "P", row, column)
        self.direction = -1 if self.pieceColor == "white" else 1
        self.onStartingField = True
        self.firstLongMove = False
        self.inputPosition = 0
        self.miniMaxValue = 1

    """ If it moves it checks if the move is a long move. Then it sets the onStartingField variable to False."""

    def makeMove(self, row, column):
        self.firstLongMove = True if self.row + 2 * self.direction == row and self.onStartingField else False
        self.row = row
        self.column = column
        self.onStartingField = False

    def updatePossibleMoves(self, board):
        self.resetMoves()
        self.checkStraightMove(board)
        self.checkForDiagonalMove(board)

    """ This function checks both straight moves."""

    def checkStraightMove(self, board):
        if board[self.row + self.direction][self.column] is None:
            self.checkShortMove()
            self.checkLongMove(board)

    def checkLongMove(self, board):
        if self.onStartingField:
            if board[self.row + self.direction * 2][self.column] is None:
                self.possibleMoves.append([[self.row, self.column], [self.row + self.direction * 2, self.column]])

    def checkShortMove(self):
        if self.checkFieldInBoard(self.row + self.direction, self.column):
            self.possibleMoves.append([[self.row, self.column], [self.row + self.direction, self.column]])

    """ This function checks both the diagonal moves. These are the normal diagonal move and the en passant."""

    def checkForDiagonalMove(self, board):
        for endColumn in [self.column + 1, self.column - 1]:
            self.checkNormalDiagonalMove(endColumn, board)
            self.checkEnPassant(endColumn, board)

    def checkNormalDiagonalMove(self, endColumn, board):
        if self.checkFieldInBoard(self.row + self.direction, endColumn):
            if board[self.row + self.direction][endColumn] is not None:
                if board[self.row + self.direction][endColumn].pieceColor != self.pieceColor:
                    self.possibleMoves.append([[self.row, self.column], [self.row + self.direction, endColumn]])
            self.attackingMoves.append([[self.row, self.column], [self.row + self.direction, endColumn],
                                        [self.row + self.direction, endColumn]])

    """ This function checks the en passant. This is only possible if there is a opposite pawn on directly next to the
    pawn. This piece had to make a long move on the last move. This is the only move in the game where the ending field
    is not equal to the attacking field."""

    def checkEnPassant(self, endColumn, board):
        if self.checkFieldInBoard(self.row, endColumn) and self.checkFieldInBoard(self.row + self.direction, endColumn):
            if board[self.row][endColumn] is not None:
                if isinstance(board[self.row][endColumn], Pawn):
                    if not self.checkEndSameColor(self.row, endColumn, board):
                        if board[self.row][endColumn].firstLongMove:
                            self.possibleMoves.append([[self.row, self.column], [self.row + self.direction, endColumn]])
                            self.attackingMoves.append([[self.row, self.column], [self.row + self.direction, endColumn],
                                                        [self.row, endColumn]])

    def makeSecondMove(self):
        self.firstLongMove = False
