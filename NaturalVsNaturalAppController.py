from AppController import AppController


""" This is a child class from the AppController. It is used when both players are natural. It does not make any moves
by its own. It only handles the things that you click."""


class NaturalVsNaturalAppController(AppController):
    def __init__(self, game, app):
        super().__init__(game, app)
        self.app.root.mainloop()

    """ This is the function that finishes a move with updating the board and switching the player. Then the next player
    can make its move. """

    def finishMove(self):
        self.game.switchPlayers()
        self.game.updateBoard()

    """ This function lets the app open a popup with all the possible pieces and binds the buttons to the function where
    a piece gets set. """

    def getNewPiece(self):
        self.selectionPossible = False
        player = self.info[0]
        self.popUp = self.app.chooseNewPiece(player)
        for n in self.popUp.grid:
            n.bind("<Button-1>", self.setNewPiece)
