""" This is the parent-class for all players. It has a color and a variable which says if it is artificial or not."""


class Player:
    def __init__(self, artificial):
        self.playerColor = None
        self.artificial = artificial

    def setPlayerColor(self, playerColor):
        self.playerColor = playerColor

    def __str__(self):
        return self.playerColor
