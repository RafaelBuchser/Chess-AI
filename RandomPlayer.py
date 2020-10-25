from ArtificialPlayer import ArtificialPlayer
import random


""" This is a child-class of an the ArtificialPlayer. If he has to return a move it returns a random picked one."""


class RandomPlayer(ArtificialPlayer):
    def makeMove(self, game):
        possibleMoves = game.getEveryPossibleMove()
        return random.choice(possibleMoves)
