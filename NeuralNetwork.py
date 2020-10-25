import tensorflow as tf


""" This is a neural Network, which is specifically built for the AI to play chess. It has three dense layers with
1024 neurons each. These neurons have the ReLu activation-function. For the output it has an additional layer with one 
neuron with the tanh activation-function. The optimizer is Adagrad. The whole network is built with tensorflow."""


class NeuralNetwork:
    def __init__(self, learningRate, training):
        self.l1 = tf.keras.layers.Dense(1024, activation="relu", input_shape=(None, 770))
        self.l2 = tf.keras.layers.Dense(1024, activation="relu")
        self.l3 = tf.keras.layers.Dense(1024, activation="relu")
        self.output = tf.keras.layers.Dense(1, activation="tanh")
        self.optimizer = tf.keras.optimizers.Adagrad(learning_rate=learningRate)
        self.training = training
        if not training:
            self.output.activation = None

    """ This function saves the network in a file. It is for example saved as 'attempt1move0014250000'."""

    def saveNetwork(self, attempt, gamesPlayed, path):
        path += "attempt" + str(attempt) + "move" + self.addZeros(10, str(gamesPlayed))
        tf.keras.Sequential([self.l1, self.l2, self.l3, self.output]).save(path, False)

    """ This function adds the zeros to the string which is used to name the saved models. """

    def addZeros(self, digits, number):
        string = ""
        while len(string) + len(number) < digits:
            string += "0"
        return string + number

    """ This function loads a saved neural networks. It overwrites the already existing model. """

    def loadNetwork(self, path):
        model = tf.keras.models.load_model(path)
        self.l1 = model.layers[0]
        self.l2 = model.layers[1]
        self.l3 = model.layers[2]
        self.output = model.layers[3]
        if not self.training:
            self.output.activation = None

    """ This function returns the output of the model. The input has to a two-dimensional Tensor with 770 inputs. The
    output is a one-dimensional Tensor with dtype 'float32'."""

    def run(self, input):
        x1 = self.l1(input)
        x2 = self.l2(x1)
        x3 = self.l3(x2)
        return self.output(x3)

    """ This function optimizes the network. It just takes one step. The inputs need to be fitting for the 'run' 
    function. 'p' needs to be the starting position observed from the opposite player. 'q' needs to be the position
    after the observed move from the training data. 'r' is the position after a random move made from 'p'. 'q' and 'r'
    are both observed from the own player."""

    def optimize(self, p, q, r):
        grads = self.gradients(p, q, r)
        self.optimizer.apply_gradients(zip(grads, [self.l1.variables[0], self.l1.variables[1], self.l2.variables[0],
                                              self.l2.variables[1], self.l3.variables[0], self.l3.variables[1],
                                              self.output.variables[0], self.output.variables[1]]))

    """ This function returns the gradients of the neural network. It uses the GradientTape from Tensorflow. """

    def gradients(self, p, q, r):
        with tf.GradientTape() as tape:
            tape.watch(self.l1.variables)
            tape.watch(self.l2.variables)
            tape.watch(self.l3.variables)
            tape.watch(self.output.variables)
            loss = self.lossErik(p, q, r)
            #loss = self.lossSelf(p, q, r)
            grads = tape.gradient(loss, [self.l1.variables[0], self.l1.variables[1], self.l2.variables[0],
                                              self.l2.variables[1], self.l3.variables[0], self.l3.variables[1],
                                              self.output.variables[0], self.output.variables[1]])
        return grads

    """ This is my own loss-function. The basic principals for the function to work are that run(p) = - run(q) and
        run(r) < run(q)"""

    def lossSelf(self, p, q, r):
        predP = self.run(p)
        predQ = self.run(q)
        predR = self.run(r)
        qrDif = predR - predQ
        pqDif = predP + predQ
        v1 = tf.math.square(pqDif)
        v2 = qrDif * abs(qrDif)
        return tf.convert_to_tensor(v1 + v2)

    """ This is the loss-function from Erik Bernhardsson. The basic principals for the function to work are that
    run(p) = - f(q) and run(r) < run(q). """

    def lossErik(self, p, q, r):
        predP = self.run(p)
        predQ = self.run(q)
        predR = self.run(r)
        qrDif = predR - predQ
        pqDif = (predQ + predP)
        v1 = tf.math.log_sigmoid(qrDif)
        v2 = - tf.math.log_sigmoid(pqDif)
        v3 = - tf.math.log_sigmoid(-pqDif)
        return v1 + v2 + v3