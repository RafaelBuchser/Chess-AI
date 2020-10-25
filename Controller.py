""" This is the parent class for all controllers. The only variable is the game itself. The job of a controller is to
handle the inputs and to hand them of to the game. The game can not be played without a controller."""


class Controller:
    def __init__(self, game):
        self.game = game

    """ This function finishes the move. It is used in the ConsoleController and in the 
    ArtificialVsArtificialAppController."""

    def completeMove(self):
        info = self.game.checkPawnReachesEndLine()
        if info is not False:
            piece = info[0].chooseNewPiece(info[1], info[2])
            self.game.board.setNewPiece(piece, info[1], info[2])
        self.game.switchPlayers()
        self.game.updateBoard()
