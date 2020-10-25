from FinalPlayer import *


""" This is a class that trains a model. The path input needs to be for the training data. The saveIndex says how many
optimizations it does before it saves the model. It trains the model with stochastic gradient descent."""


class Trainer:
    def __init__(self, path, learningRate):
        self.path = path
        self.network = NeuralNetwork(learningRate, True)
        self.trainingData = self.openData()
        self.attempt = 3
        self.saveIndex = 250000
        self.train()

    """ This function opens the training data file. It is not saved in an array but it returns a generator. That needs
    to be done because the training data in my case is very big which would overwhelm the memory. With that solution it
    is a bit slower but you can open as much data as you want."""

    def openData(self):
        with open(self.path) as file:
            for strLine in file:
                line = []
                for n in strLine.replace("\n", ""):
                    line.append(int(n))
                yield line

    """ This function is the main training function. It only stops when all the training data is used. But it saves the
    model for every multiple of the save index."""

    def train(self):
        saveIndex = self.saveIndex
        index = 0
        while True:
            try:
                p, q, r = self.getDataSet()
            except:
                break
            self.network.optimize(p, q, r)
            saveIndex = self.saveNetwork(index, saveIndex, p, q, r)
            index += 1
        self.network.saveNetwork(self.attempt, index, "Models/")

    def getDataSet(self):
        p = tf.convert_to_tensor([next(self.trainingData)])
        q = tf.convert_to_tensor([next(self.trainingData)])
        r = tf.convert_to_tensor([next(self.trainingData)])
        return p, q, r

    """ This function shows the outputs of the network for one data set. This is to observe if the model gives correct
    outputs during training."""

    def showResult(self, p, q, r):
        print(self.network.run(p))
        print(self.network.run(q))
        print(self.network.run(r))

    """ This function checks if the index has reached the save index. If that is the case it saves the model."""

    def saveNetwork(self, index, saveIndex, p, q, r):
        if index >= saveIndex:
            print(saveIndex)
            self.network.saveNetwork(self.attempt, saveIndex, "Models/")
            self.showResult(p, q, r)
            saveIndex += self.saveIndex
        return saveIndex
