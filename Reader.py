from Game import Game
from ArtificialPlayer import ArtificialPlayer
from Controller import Controller
from Observer import Observer
from Pawn import Pawn
from Queen import Queen
from Rook import Rook
from Bishop import Bishop
from Knight import Knight
import random


""" This class reads pgn data and writes it as suiting inputs for the network. The pgn data needs to be saved as
'ficsgamesdb_' + a year + '.pgn'. The first year needs to be saved in self.year as an integer. It then iterates through
the years until it can't find the next year. The writeFile is the file where the data is saved."""


class Reader:
    def __init__(self):
        self.player1 = ReaderPlayer()
        self.player2 = ReaderPlayer()
        self.writeFile = open("TrainingData/trainingData.txt", "w")
        self.gameCounter = 0
        self.year = 2000
        self.read()
        self.writeFile.close()

    """ This function is the main function of the reader. It opens every correctly named file until it can't find one.
    Then it stops the reading process."""

    def read(self):
        while True:
            try:
                self.path = "TrainingData/PGN-data/ficsgamesdb_" + str(self.year) + ".pgn"
                print("year:", self.year)
                readFile = open(self.path, "r")
                self.lines = readFile.readlines()
                self.readFile()
                self.year += 1
                readFile.close()
            except:
                break
        print(self.gameCounter)

    """ This function reads one file. For every game in the file, it replays the game. This is necessary because the pgn
    data alone does not always say which piece was moved. Therefore you need all possible moves. After every percent of
    the file it prints the percent. Every game requires a ReaderObserver and a ReaderController and two ReaderPlayers.
    """

    def readFile(self):
        index = self.findNextLine(0)
        percent = len(self.lines)/100
        printCounter = percent
        while True:
            if index > printCounter:
                print(str(self.findPercentage(index, len(self.lines))) + "%")
                printCounter += percent
            game = Game(self.player1, self.player2)
            self.gameCounter += 1
            observer = ReaderObserver(game, self.writeFile)
            sequence = self.readLine(index)
            ReaderController(game, sequence, observer)
            try:
                index = self.findNextLine(index)
            except:
                break

    """ This function finds the next line index where the game is saved. The distance of these lines are not always the
    same. That's because it starts with 15 lines between and adds always one until it finds the line."""

    def findNextLine(self, index):
            index += 15
            while self.lines[index][0] != "1":
                index += 1
            return index

    """ This function reads a line and converts it into an array. It does not include the numbers of the moves as well
    as characters like '.' or '{' (and everything that is written after that)."""

    def readLine(self, index):
        sequence = []
        array = self.lines[index].split()
        moveCount = 1
        for notation in array:
            if notation != str(moveCount) + ".":
                if "{" in notation:
                    break
                else:
                    sequence.append(notation)
            else:
                moveCount += 1
        return sequence

    def findPercentage(self, index, maxIndex):
        return index/maxIndex * 100


""" This is the player which is needed to read the data. When it is on the move it gets the string and the game as an
input. It then interprets the string and converts it to a move which is saved as 
[[startRow, startColumn], [endRow, endColumn]]. The game is necessary because the moving piece is not always clear. If
that is the case it looks at all the legal moves to get the correct one."""


class ReaderPlayer(ArtificialPlayer):
    def __init__(self):
        super().__init__()

    """ This function is the main function which is called to interpret a string. It basically classifies how the string
    needs to be interpreted. It also sorts out characters like '+', 'x' and '#', because they make no difference to the
    result."""

    def interpretMove(self, string, game):
        string = string.replace("+", "").replace("x", "").replace("#", "")
        if string[0] == "O":
            return [self.interpretCastling(string, game), None]
        if "=" in string:
            return self.interpretUpgrade(string, game)
        if len(string) == 2:
            return [self.interpretPawn(string, game), None]
        if len(string) == 3:
            if ord(string[0]) > 93:
                return [self.interpretUnclearPawn(string, game), None]
            return [self.interpretNormalMove(string, game), None]
        if len(string) == 4:
            return [self.interpretUnclearMove(string, game), None]
        if len(string) == 5:
            return [self.interpretDoubleUnclearMove(string)]

    """ This function is called when the first character of the string is 'O'. It then looks if it is a kingside or
    queenside castling and then returns the move. """

    def interpretCastling(self, string, game):
        if len(string) == 3:
            if self == game.playerWhite:
                return [[7, 4], [7, 6]]
            else:
                return [[0, 4], [0, 6]]
        else:
            if self == game.playerWhite:
                return [[7, 4], [7, 2]]
            else:
                return [[0, 4], [0, 2]]

    """ This function is called when a pawn reaches the end line and gets upgraded."""

    def interpretUpgrade(self, string, game):
        if len(string) == 4:
            return [self.interpretPawn(string[0] + string[1], game), string[3]]
        else:
            return [self.interpretUnclearPawn(string[0:3], game), string[4]]

    """ This function is called when its a move with a pawn, where there is only one option. The string is only the
    destination field. """

    def interpretPawn(self, string, game):
        end = self.convertField(string)
        for possibleMove in game.getEveryPossibleMove():
            if possibleMove[1] == end:
                if isinstance(game.board.board[possibleMove[0][0]][possibleMove[0][1]], Pawn):
                    return possibleMove

    """ This function interprets an move with a pawn, where there are two pawn which can move to the destination field.
    It checks if the helping character is a number or a letter."""

    def interpretUnclearPawn(self, string, game):
        end = self.convertField(string[1] + string[2])
        for possibleMove in game.getEveryPossibleMove():
            if possibleMove[1] == end:
                if isinstance(game.board.board[possibleMove[0][0]][possibleMove[0][1]], Pawn):
                    if ord(string[0]) > 80:
                        column = ord(string[0]) - ord("a")
                        if possibleMove[0][1] == column:
                            return possibleMove
                    else:
                        row = 8 - int(string[0])
                        if possibleMove[0][0] == row:
                            return possibleMove

    """ This function interprets a normal move where the string has three characters. It finds the pieces with legal
    moves to the destination field and then checks if its the correct piece."""

    def interpretNormalMove(self, string, game):
        end = self.convertField(string[1] + string[2])
        for possibleMove in game.getEveryPossibleMove():
            if possibleMove[1] == end:
                if game.board.board[possibleMove[0][0]][possibleMove[0][1]].letter == string[0]:
                    return possibleMove

    """ This function interprets a move with any piece except a pawn when it is unclear which piece is moving. If that
    is the case there is a helping character which clears which piece needs to move. It checks if the helping character
    is a letter or a number and then returns the correct move."""

    def interpretUnclearMove(self, string, game):
        end = self.convertField(string[2] + string[3])
        for possibleMove in game.getEveryPossibleMove():
            if possibleMove[1] == end:
                if game.board.board[possibleMove[0][0]][possibleMove[0][1]].letter == string[0]:
                    if ord(string[1]) > 80:
                        column = ord(string[1]) - ord("a")
                        if possibleMove[0][1] == column:
                            return possibleMove
                    else:
                        row = 8 - int(string[1])
                        if possibleMove[0][0] == row:
                            return possibleMove

    """ This is the function which is called when its needs two helping characters. These two helping characters are
    just the startRow and startColumn."""

    def interpretDoubleUnclearMove(self, string):
        end = self.convertField(string[3] + string[4])
        start = self.convertField(string[1] + string[2])
        return [start, end]

    """ This function turns a string which describes a field to the number of the row and column. For example 'e4' would
    be [4, 4]."""

    def convertField(self, string):
        array = [None, None]
        array[0] = 8 - int(string[1])
        array[1] = ord(string[0]) - ord("a")
        return array

    """ This function returns the correct piece in an upgrade depending on the letter. """

    def interpretNewPiece(self, letter, row, column):
        if letter == "Q":
            return Queen(self.playerColor, row, column)
        if letter == "R":
            return Rook(self.playerColor, row, column)
        if letter == "B":
            return Bishop(self.playerColor, row, column)
        if letter == "N":
            return Knight(self.playerColor, row, column)


""" This is the controller for the reading program. It has the sequence with all the strings and lets the players
interpret them. After that it saves all the positions needed for the training data. Then it tells the game to move."""


class ReaderController(Controller):
    def __init__(self, game, sequence, observer):
        super().__init__(game)
        observer.setController(self)
        self.sequence = sequence
        self.moveCount = len(sequence)
        self.p = None
        self.q = None
        self.r = None
        self.play()

    """ This is the main function of this class. It has the game loop in it. But because there are sometimes errors in
    the pgn data it has to try out if the move is possible. If the move is not possible the player can't interpret it.
    If there is an error the loop stops and it skips to the next game."""

    def play(self):
        moveCount = 0
        while (not self.game.gameOver) and moveCount < self.moveCount:
            move = self.game.playerOnMove.interpretMove(self.sequence[moveCount], self.game)
            try:
                self.makeMoves(move[0])
                info = self.game.checkPawnReachesEndLine()
                if info is not False:
                    piece = self.game.playerOnMove.interpretNewPiece(move[1], info[1], info[2])
                    self.game.board.setNewPiece(piece, info[1], info[2])
                self.game.switchPlayers()
                self.game.updateBoard()
                moveCount += 1
            except:
                break

    """ This is the function which saves the three used positions 'p', 'q' and 'r'. 'p' is not observed from the player
    on the move but from the opposite player. That's why it changes the player on the move before and after the position
    is observed."""

    def makeMoves(self, move):
        infos = self.game.getInfos()
        self.game.switchPlayers()
        self.p = self.game.getPosition(self.game.playerOnMove)
        self.game.switchPlayers()
        self.game.move(random.choice(self.game.getEveryPossibleMove()))
        self.r = self.game.getPosition(self.game.playerOnMove)
        self.game.resetInfos(infos)
        self.game.move(move)
        self.q = self.game.getPosition(self.game.playerOnMove)


""" This class is the observer. In this case it writes the training data in a file when it is notified. It needs the
filepath from the file to write the data in and it needs the controller because it gets the datasets from it."""


class ReaderObserver(Observer):
    def __init__(self, game, file):
        super().__init__(game)
        self.controller = None
        self.file = file

    def setController(self, reader):
        self.controller = reader

    """ This writes the data in the file in this order: p, q, r. They are both a 770 long string with 1's an 0's. There
    are no spaces between them. p, q and r are all written in a new line."""

    def update(self):
        self.file.write("".join(map(str, self.controller.p)) + "\n")
        self.file.write("".join(map(str, self.controller.q)) + "\n")
        self.file.write("".join(map(str, self.controller.r)) + "\n")

    def printWinner(self):
        pass
