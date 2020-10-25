import tensorflow as tf


""" This is the class for the engine which does the calculation for the MiniMax algorithm. It is a parent-class for the
strong- and weak-MiniMax-engine. They only have a different evaluation function."""


class MiniMaxEngine:
    def __init__(self, player):
        self.move = None
        self.player = player
        self.minValue = tf.convert_to_tensor([-1000.0])
        self.maxValue = tf.convert_to_tensor([1000.0])
        self.drawValue = tf.convert_to_tensor([0.0])

    """ This function is called for the MiniMax-algorithm. The first function is needed because it also needs the move
    where the value is the highest."""

    def calculateMiniMax(self, game, movesAhead):
        possibleMoves = game.getEveryPossibleMove()
        maxValue = self.minValue
        for move in possibleMoves:
            infos = game.getInfos()
            row, column = move[0]
            letter = game.board.board[row][column].letter
            game.move(move)
            value = self.calculateMin(game, movesAhead - 1, self.minValue, self.maxValue)
            print(letter, "abcdefgh"[column] + str(8 - row) + "-->" + "abcdefgh"[move[1][1]] + str(8 - move[1][0]),
                  float(value[0]))
            if value >= maxValue:
                maxValue = value
                self.move = move
            game.resetInfos(infos)

    """ These two functions are called back and forth in the algorithm. They work similarly but are doing the opposite. 
    They collect all the values from the forecasted moves and returns the maximum or the minimum of them. But if the
    game is finished it returns the values -100, 0, 100. And if it has reached the search depth it calculates the value
    of the move. But otherwise it will forecast further. If a move is not necessary to calculate then it returns the
    last value. That is called alpha-beta-pruning."""

    def calculateMax(self, game, movesAhead, alpha, beta):
        self.checkPawnReachesEndLine(game)
        game.switchPlayers()
        game.updateBoard()
        possibleMoves = game.getEveryPossibleMove()
        if not game.checkGameFinished():
            if movesAhead != 0:
                value = self.minValue
                for move in possibleMoves:
                    infos = game.getInfos()
                    game.move(move)
                    value = max(value, self.calculateMin(game, movesAhead - 1, alpha, beta))
                    alpha = max(alpha, value)
                    game.resetInfos(infos)
                    if alpha >= beta:
                        return value
                return value
            return self.calculateValueOfMove(game)
        if game.playerWon == self.player:
            return self.maxValue
        elif game.playerWon is not None:
            return self.minValue
        else:
            return self.drawValue

    def calculateMin(self, game, movesAhead, alpha, beta):
        self.checkPawnReachesEndLine(game)
        game.switchPlayers()
        game.updateBoard()
        possibleMoves = game.getEveryPossibleMove()
        if not game.checkGameFinished():
            if movesAhead != 0:
                value = self.maxValue
                for move in possibleMoves:
                    infos = game.getInfos()
                    game.move(move)
                    value = min(value, self.calculateMax(game, movesAhead - 1, alpha, beta))
                    beta = min(beta, value)
                    game.resetInfos(infos)
                    if alpha >= beta:
                        return value
                return value
            return self.calculateValueOfMove(game)
        if game.playerWon == self.player:
            return self.maxValue
        elif game.playerWon is not None:
            return self.minValue
        else:
            return self.drawValue

    """ This function checks if a pawn has reached the back rank."""

    def checkPawnReachesEndLine(self, game):
        info = game.checkPawnReachesEndLine()
        if info is not False:
            piece = self.player.chooseNewPiece(info[1], info[2])
            game.board.setNewPiece(piece, info[1], info[2])

    def calculateValueOfMove(self, game):
        pass
