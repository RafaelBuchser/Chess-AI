from Controller import Controller


""" This is the child class from the controller. It is not a parent class because it can handle everything.
This controller handles the game if you are playing on the console. It is in a while-loop that ends when the game is
over."""


class ConsoleController(Controller):
    def __init__(self, game):
        super().__init__(game)
        self.play()

    """ This is the game loop. It asks the player for a move. If the move is not legal it asks him again. If the move
    was made it completes the move with the function of the parent-class."""

    def play(self):
        while not self.game.gameOver:
            while True:
                move = self.game.playerOnMove.makeMove(self.game)
                if self.game.move(move):
                    break
            self.completeMove()
