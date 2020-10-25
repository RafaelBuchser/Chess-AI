from Observer import Observer


""" This is a child class from the observer. It prints the game in the console."""


class ConsoleObserver(Observer):
    def __init__(self, game):
        super().__init__(game)
        self.update()

    def update(self):
        print(self.game.board)

    def printWinner(self):
        winner = self.game.playerWon
        print("Player " + str(winner) + " has won!") if winner is not None else print("It's a draw!")
