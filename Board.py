from King import *
from Queen import Queen
from Bishop import Bishop
from Knight import Knight
from Rook import Rook
from Pawn import Pawn


""" This is the class for the chessboard. It has a 8x8 list with all the pieces on their position. Whites back rank is
row = 7 and blacks is row = 0. If a field is empty it holds None. It has two lists with the pieces which are captured.
"""


class Board:
    def __init__(self):
        self.board = []
        self.whiteOutPieces = []
        self.blackOutPieces = []
        self.createBoard()
        self.createPieces()

    """ This moves a piece from a starting position to an ending position."""

    def movePiece(self, startRow, startColumn, endRow, endColumn):
        self.board[endRow][endColumn] = self.board[startRow][startColumn]
        self.board[startRow][startColumn] = None
        self.board[endRow][endColumn].makeMove(endRow, endColumn)

    """ This function removes the pieces from the board and adds it to the lists with the removed pieces. """

    def removePiece(self, row, column):
        piece = self.board[row][column]
        self.whiteOutPieces.append(piece) if piece.pieceColor == "white" else self.blackOutPieces.append(piece)
        self.board[row][column] = None

    """ This function sets a new piece. It is used when the Pawn reaches the back rank."""

    def setNewPiece(self, piece, row, column):
        self.board[row][column] = piece

    """ This function creates a 8x8 board."""

    def createBoard(self):
        for row in range(8):
            self.board.append([])
            for column in range(8):
                self.board[row].append(None)

    """ This function creates all the pieces and sets them on their starting position. """

    def createPieces(self):
        self.createBlack()
        self.createWhite()

    def createWhite(self):
        for n in range(8):
            self.board[6][n] = Pawn("white", 6, n)
        for n in [0, 7]:
            self.board[7][n] = Rook("white", 7, n)
        for n in [1, 6]:
            self.board[7][n] = Knight("white", 7, n)
        for n in [2, 5]:
            self.board[7][n] = Bishop("white", 7, n)
        self.board[7][3] = Queen("white", 7, 3)
        self.board[7][4] = King("white", 7, 4)

    def createBlack(self):
        for n in range(8):
            self.board[1][n] = Pawn("black", 1, n)
        for n in [0, 7]:
            self.board[0][n] = Rook("black", 0, n)
        for n in [1, 6]:
            self.board[0][n] = Knight("black", 0, n)
        for n in [2, 5]:
            self.board[0][n] = Bishop("black", 0, n)
        self.board[0][3] = Queen("black", 0, 3)
        self.board[0][4] = King("black", 0, 4)

    def __str__(self):
        boardString = "\n    "
        for piece in self.blackOutPieces:
            boardString += str(piece) + " "
        boardString += "\n      a    b    c    d    e    f    g    h"
        for row in range(8):
            boardString += "\n   +----+----+----+----+----+----+----+----+\n" + str(8 - row) + " "
            for column in range(8):
                if isinstance(self.board[row][column], Piece):
                    boardString += " | " + str(self.board[row][column])
                else:
                    boardString += " |   "
            boardString += " |  " + str(8 - row)
        boardString += "\n" \
                       "   +----+----+----+----+----+----+----+----+\n" \
                       "      a    b    c    d    e    f    g    h\n" \
                       "    "
        for piece in self.whiteOutPieces:
            boardString += str(piece) + " "
        boardString += "\n"
        return boardString
