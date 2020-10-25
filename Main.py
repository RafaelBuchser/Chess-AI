from AppObserver import *
from ConsoleObserver import ConsoleObserver
from FileObserver import FileObserver
from ArtificialVsNaturalAppController import ArtificialVsNaturalAppController
from NaturalVsNaturalAppController import NaturalVsNaturalAppController
from ArtificialVsArtificialAppController import ArtificialVsArtificialAppController
from ConsoleController import ConsoleController
from NaturalPlayer import NaturalPlayer
from FinalPlayer import FinalPlayer
from RandomPlayer import RandomPlayer
from MiniMaxPlayer import MiniMaxPlayer
from Reader import *
from Trainer import Trainer


readData = False
trainModel = False
playGame = True

if readData:
    Reader()
if trainModel:
    Trainer("TrainingData/trainingData.txt", 0.01)
if playGame:

    """ 'n' stands for a natural player. That means that you can play manually. For making a move you have to type the 
    field where your piece is located. Then press enter and type the destination of your piece. 'r' stands for a random
    player. He will just randomly pick a move. 'm' stands for a artificial player with MiniMax. He will look a couple
    moves ahead and evaluate based on the pieces on the board. 'f' stands for the final artificial intelligence which is
    the whole point of this program."""


    def getCorrectPlayer(x, name):
        if x == "r":
            return RandomPlayer()
        elif x == "f":
            return FinalPlayer(True, name) if name is not None else FinalPlayer(False, name)
        elif x == "m":
            return MiniMaxPlayer()
        elif x == "n":
            return NaturalPlayer()


    player1State = "f"
    player2State = "r"
    name1 = "Models/attempt2move0014250000"
    name2 = "Models/attempt2move0014250000"

    """ Attempt 2 is the final AI. Attempt 3 is the AI with the own loss-function"""

    player1 = getCorrectPlayer(player1State, name1)
    player2 = getCorrectPlayer(player2State, name2)

    showApp = True
    safeGame = False

    """ This project works with the 'Model-View-Controller-Pattern'. It is used to handle the user interface. It divides
    the tasks into three independent elements. There is the model. In this case this is the game. The game tells the
    view if it has changed. Then there is the controller. It handles the inputs and hands them off to the model. The
    view observes the model. It is not strictly necessary"""

    game = Game(player1, player2)
    if safeGame:
        fileObserver = FileObserver(game, "newGame")
    if showApp:
        app = AppObserver(game)
        if player1.artificial != player2.artificial:
            controller = ArtificialVsNaturalAppController(game, app)
        elif player1.artificial and player2.artificial:
            controller = ArtificialVsArtificialAppController(game, app)
        else:
            controller = NaturalVsNaturalAppController(game, app)
    else:
        observer = ConsoleObserver(game)
        controller = ConsoleController(game)
