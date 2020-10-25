from Controller import Controller
import threading


""" This is a child-class of the Controller. The reason for it not to be a child-class from the AppController is because
it you don't need to interact with the GUI. So it does not need any of the functions from the AppController. It works
basically like the ConsoleController but it starts its game loop in a new thread. That is necessary for the app not to
freeze."""


class ArtificialVsArtificialAppController(Controller):
    def __init__(self, game, app):
        super().__init__(game)
        self.app = app
        threading.Thread(target=self.play).start()
        self.app.root.mainloop()

    """ This is the game loop function. It is in a while loop which ends when the game is over. It asks the player for
    the move and executes it. Then it completes the move with a function from the parent-class."""

    def play(self):
        while not self.game.gameOver:
            playerOnMove = self.game.playerOnMove
            move = playerOnMove.makeMove(self.game)
            self.game.move(move)
            self.completeMove()
