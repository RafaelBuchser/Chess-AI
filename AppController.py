from Controller import Controller
from Rook import Rook
from Queen import Queen
from Knight import Knight
from Bishop import Bishop


""" This is the parent class for controllers for the GUI and the child class from the controller. The difference between
the normal Controller is that it has the app as a variable. It handles the clicks. When you click on a field with a
piece of the correct color the controller selects the field. When a piece is selected and you click on a correct field
it makes the move and checks if the game is finished. If the game is finished it opens a popup with the
'winner message'. It also opens a popup to choose a new piece if a pawn reaches the back rank."""


class AppController(Controller):
    def __init__(self, game, app):
        super().__init__(game)
        self.app = app
        self.move = [[None, None], [None, None]]
        self.info = None
        self.popUp = None
        self.pieceSelected = False
        self.selectionPossible = True
        self.bindGrid()

    """ This is the function that is called if a button is clicked on the GUI. It checks if the game is not over and
    nothing is calculating. """

    def makeMove(self, event):
        if (not self.game.gameOver) and self.selectionPossible:
            self.setMove(event)

    """ This function handles the click. It checks if the clicked field contains a piece from the same color. If that is
    the case it sets the start of the move and lets the app select this piece. If that is not the case the is checks if
    the start has been set and then calls the setEnd function which handles the ending of a move."""

    def setMove(self, event):
        piece = self.game.board.board[event.widget.row][event.widget.column]
        if self.checkPieceFromSameColor(piece):
            self.move[0][0] = event.widget.row
            self.move[0][1] = event.widget.column
            self.pieceSelected = True
            possibleMoves = self.game.getEveryPossibleMove()
            self.app.unselectPiece()
            self.app.selectPiece(possibleMoves, self.move[0][0], self.move[0][1])
        else:
            if self.pieceSelected:
                self.setEnd(event)

    """ This function checks if a piece is on a field and if it has the same color as the player on the move. """

    def checkPieceFromSameColor(self, piece):
        if piece is not None:
            if piece.pieceColor == str(self.game.playerOnMove):
                return True
        return False

    """ This functions binds the grid of buttons of the app to the function that makes a move."""

    def bindGrid(self):
        grid = self.app.grid
        for row in grid:
            for button in row:
                button.bind("<Button-1>", self.makeMove)

    """ This function sets the end of the move and executes it. It finishes the move if there has no pawn reached the
        back rank. Otherwise it opens popup which will finish the move after the piece was chosen. """

    def setEnd(self, event):
        self.move[1][0] = event.widget.row
        self.move[1][1] = event.widget.column
        if self.game.move(self.move):
            self.move = [[None, None], [None, None]]
            self.info = self.game.checkPawnReachesEndLine()
            self.getNewPiece() if self.info is not False else self.finishMove()
        self.pieceSelected = False
        self.app.unselectPiece()

    """ This function sets a new piece after one was chosen in the pop-up. It then destroys the popup and finishes the
    move. """

    def setNewPiece(self, event):
        if event.widget.column == 0:
            piece = Queen(str(self.game.playerOnMove), self.info[1], self.info[2])
        elif event.widget.column == 1:
            piece = Rook(str(self.game.playerOnMove), self.info[1], self.info[2])
        elif event.widget.column == 2:
            piece = Bishop(str(self.game.playerOnMove), self.info[1], self.info[2])
        else:
            piece = Knight(str(self.game.playerOnMove), self.info[1], self.info[2])
        self.game.board.setNewPiece(piece, self.info[1], self.info[2])
        self.popUp.root.destroy()
        self.selectionPossible = True
        self.finishMove()

    def finishMove(self):
        pass

    def getNewPiece(self):
        pass
