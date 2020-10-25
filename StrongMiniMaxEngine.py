from MiniMaxEngine import *
from NeuralNetwork import *


""" This class is a subclass of the MiniMax-engine. The only difference between the other engine is the
evaluation function. It works with a neuronal network. The network calculates the value of a position. The 
MiniMax-engine calculates every possible move and let the neuronal network evaluate it."""


class StrongMiniMaxEngine(MiniMaxEngine):
    def __init__(self, player, openFile, fileName):
        super().__init__(player)
        self.neuralNetwork = NeuralNetwork(0.01, False)
        if openFile:
            self.neuralNetwork.loadNetwork(fileName)

    def calculateValueOfMove(self, game):
        inputs = game.getPosition(self.player)
        return self.neuralNetwork.run(tf.convert_to_tensor([inputs]))[0]
