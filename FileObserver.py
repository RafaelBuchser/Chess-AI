from Observer import Observer


""" This is a child-class of the observer. It saves the game in a file. That file is saved under the name + '.txt'.
For every move it saves in the board with a similar function of the __str__ function of the board. But the difference is
that the pieces are saves with letters and not with signs. That's because the signs can't be saved in a text file."""


class FileObserver(Observer):
    def __init__(self, game, name):
        super().__init__(game)
        self.name = name
        self.file = open("Games/" + self.name + ".txt", "w")

    def update(self):
        self.file.write(self.toString())

    """ This function returns a string of the board with letters as pieces."""

    def toString(self):
        board = self.game.board
        boardString = "\n    "
        for piece in board.blackOutPieces:
            boardString += piece.getLetters() + " "
        boardString += "\n      a    b    c    d    e    f    g    h"
        for row in range(8):
            boardString += "\n   +----+----+----+----+----+----+----+----+\n" + str(8 - row) + " "
            for column in range(8):
                if board.board[row][column] is not None:
                    boardString += " | " + board.board[row][column].getLetters()
                else:
                    boardString += " |   "
            boardString += " |  " + str(8 - row)
        boardString += "\n" \
                       "   +----+----+----+----+----+----+----+----+\n" \
                       "      a    b    c    d    e    f    g    h\n" \
                       "    "
        for piece in board.whiteOutPieces:
            boardString += piece.getLetters() + " "
        boardString += "\n"
        return boardString

    """ This function writes a message which says how the game as ended. It then closes the file."""

    def printWinner(self):
        winner = self.game.playerWon
        self.file.write("\nPlayer " + str(winner) + " has won!") if winner is not None \
            else self.file.write("\nIt's a draw!")
        self.file.close()
