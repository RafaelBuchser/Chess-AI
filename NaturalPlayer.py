from Player import Player
from Queen import Queen
from Rook import Rook
from Knight import Knight
from Bishop import Bishop


""" This class is a child-class of a player. It is used everytime, when a natural player is playing in a game. All
these functions are only used if the game is played on the console because if it is played on a GUI it gets all the
inputs from that."""


class NaturalPlayer(Player):
    def __init__(self):
        super().__init__(False)

    """ This function gets the move of the player via the input function. If the input is not correct or the move is not
    possible it asks the player again."""

    def makeMove(self, game):
        while True:
            startInput = input("move from ")
            endInput = input("to ")
            try:
                start = self.convertInput(startInput)
                end = self.convertInput(endInput)
                return start, end
            except:
                print("invalid input")

    """ This function converts a string of a field like 'e4' to an array of row and column like [4, 4]."""

    def convertInput(self, input):
        array = [None, None]
        array[0] = 8 - int(input[1])
        array[1] = ord(input[0]) - ord("a")
        return array

    """ This function gets called if the natural player has to choose a new piece. It prints the options and then asks
    the player via the input-function which piece it wants to choose. If the input is not correct the player gets asked
    again."""

    def chooseNewPiece(self, row, column):
        print("type 'Q' for a queen\n"
              "     'R' for a rook\n"
              "     'B' for a bishop\n"
              "     'K' for a knight")
        while True:
            pieceInput = input()
            if pieceInput == "Q" or pieceInput == "q":
                return Queen(self.playerColor, row, column)
            elif pieceInput == "R" or pieceInput == "r":
                return Rook(self.playerColor, row, column)
            elif pieceInput == "B" or pieceInput == "b":
                return Bishop(self.playerColor, row, column)
            elif pieceInput == "K" or pieceInput == "k":
                return Knight(self.playerColor, row, column)
            else:
                print("invalid input")
