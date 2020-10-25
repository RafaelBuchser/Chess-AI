from AppController import AppController
import threading


""" This is a child class from the AppController. It is used when one player is natural and one is artificial. At the
beginning and after every move from the natural player it checks if the artificial player is the moving player now. If
this is the case the controller gets the move from the artificial player and makes it."""


class ArtificialVsNaturalAppController(AppController):
    def __init__(self, game, app):
        super().__init__(game, app)
        self.calculating = False
        self.checkNextMove()
        self.app.root.mainloop()

    """ This is the function that finishes a move with updating the board and switching the player. It then checks if
     the next player is the artificial one. """

    def finishMove(self):
        self.game.switchPlayers()
        self.game.updateBoard()
        self.checkNextMove()

    """ This function gets called when a player has done a move. It checks if the player on move is now the artificial
    one. If that is the case it calls a the function which lets the player calculate. It will start this function in a
    new thread for the app not to freeze while calculating. """

    def checkNextMove(self):
        if self.game.playerOnMove.artificial and (not self.game.gameOver):
            self.selectionPossible = False
            threading.Thread(target=self.letPlayerCalculate).start()

    """ This function handles the move of the artificial player. It asks the player for the move and executes it. Then
    it checks if a pawn has reached the ground line. It then finishes the move."""

    def letPlayerCalculate(self):
        move = self.game.playerOnMove.makeMove(self.game)
        self.game.move(move)
        self.info = self.game.checkPawnReachesEndLine()
        if self.info is not False:
            self.getNewPiece()
        self.game.switchPlayers()
        self.game.updateBoard()
        self.selectionPossible = True

    """ This function sets a new piece for both players. If the player is artificial it just asks him and sets the new
    piece. Otherwise it opens a popup which allows the player to choose a piece."""

    def getNewPiece(self):
        player = self.info[0]
        row = self.info[1]
        column = self.info[2]
        if player.artificial:
            piece = player.chooseNewPiece(row, column)
            self.game.board.setNewPiece(piece, row, column)
        else:
            self.selectionPossible = False
            self.popUp = self.app.chooseNewPiece(player)
            for n in self.popUp.grid:
                n.bind("<Button-1>", self.setNewPiece)
