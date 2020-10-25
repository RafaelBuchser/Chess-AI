""" This is the parent class of all observers. It only has the game in it and adds itself to the game. The job of an
observer is only to make the game visible. The game can even be player without an observer. It just needs the correct
controller."""


class Observer:
    def __init__(self, game):
        self.game = game
        self.game.addObserver(self)
