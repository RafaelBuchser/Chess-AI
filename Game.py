from Board import *


""" This is the class for a chess game. It does not play by itself. That is the task of a controller. It has two
players. The first one will be set to white and the second to black. This class holds all the rules of chess in it.
Everytime something has changed the game needs to be updated. This basically calculates all rules for the new position
and notifies the observers. """


class Game:
    def __init__(self, playerWhite, playerBlack):
        self.playerWhite = playerWhite
        self.playerBlack = playerBlack
        self.setColorsToPlayers()
        self.playerOnMove = playerWhite
        self.board = Board()
        self.playerWon = None  # That is the player who won the game. If it is a draw it will stay None.
        self.stateCheck = False  # Says if in a move the player is in check.
        self.fiftyMovesCounter = 0  # That counts the moves for the fifty-moves rule.
        self.pieceRemoved = False  # This is true if a piece was removed from the board in the last move.
        self.observers = []  # The observers get notified after something happened on the board.
        self.gameOver = False

        """ These are lists with all moves. They are updated after every move. A possible move is saved like this: 
        [[startRow, startColumn], [endRow, endColumn]] and a attacking move like [[startRow, startColumn],
        [endRow, endColumn], [attackingRow, attackingColumn]]"""

        self.possibleWhiteMoves = []
        self.possibleBlackMoves = []
        self.possibleWhiteCastlings = []
        self.possibleBlackCastlings = []
        self.attackingWhiteMoves = []
        self.attackingBlackMoves = []

        self.updateBoard()

    """ This function sets the colors to the players."""

    def setColorsToPlayers(self):
        self.playerBlack.setPlayerColor("black")
        self.playerWhite.setPlayerColor("white")

    """ Makes one single move. If the move is not legal it does nothing and returns False. If the it is legal it makes 
    the move and counts the moves for the "fifty-move-rule"."""

    def move(self, move):
        startRow, startColumn = move[0]
        endRow, endColumn = move[1]
        if self.checkMovePossible(startRow, startColumn, endRow, endColumn, self.playerOnMove):
            self.makeNextMoveForEnPassant(str(self.playerOnMove))
            self.movePieces(startRow, startColumn, endRow, endColumn)
            self.countMoves(endRow, endColumn)
            return True
        elif self.checkForCastlingPossible(startRow, startColumn, endRow, endColumn, self.playerOnMove):
            self.makeNextMoveForEnPassant(str(self.playerOnMove))
            self.makeCastling(startRow, startColumn, endColumn)
            self.countMoves(endRow, endColumn)
            return True
        return False

    """ This moves makes a normal move or en passant. It checks if a piece is captured in a normal move and in
    en passant and calls all the functions from the board."""

    def movePieces(self, startRow, startColumn, endRow, endColumn):
        board = self.board.board
        piece = board[startRow][startColumn]
        if board[endRow][endColumn] is not None:  # Removes piece in an normal move.
            self.board.removePiece(endRow, endColumn)
            self.pieceRemoved = True
        elif isinstance(piece, Pawn):  # Removes piece in en passant.
            if board[endRow][endColumn] is None and endColumn != startColumn:
                self.board.removePiece(startRow, endColumn)
                self.pieceRemoved = True
        else:
            self.pieceRemoved = False
        self.board.movePiece(startRow, startColumn, endRow, endColumn)

    """ This moves the pieces in a castling. It calculates the direction of the castling and calls all the functions
    from the board."""

    def makeCastling(self, row, startColumn, endColumn):
        direction = int(abs(endColumn - startColumn) / (endColumn - startColumn))
        self.board.movePiece(row, startColumn, row, endColumn)
        self.board.movePiece(row, 0, row, 3) if direction == -1 else self.board.movePiece(row, 7, row, 5)
        self.pieceRemoved = False

    """ This function switches the moving player."""

    def switchPlayers(self):
        self.playerOnMove = self.playerWhite if self.playerOnMove == self.playerBlack else self.playerBlack

    """ This function updates the game. This means, that the possible and attacking moves and the 
    possible castlings are updated. Also it checks if a player is in check. Then it updates the possible moves again 
    and allows only the moves which get the player out of the check."""

    def updateBoard(self):
        kings = self.updateAllMoves()
        self.updateCastling()
        checkMoves = self.checkKingUnderAttack(str(self.playerOnMove))
        if len(checkMoves) == 0:
            self.stateCheck = False
        else:
            self.stateCheck = True
            self.updateInCheck(self.playerOnMove, checkMoves, kings)
        self.notifyObservers()
        self.checkGameFinished()

    """ This function checks if the game is finished. It could end in a draw or in a win. The only possibility to win is
    to make a checkmate. This happens if the king is under attack and there are no legal moves to get out of it. A draw
    can happen if the moving player has no possible moves left. That's a stalemate. A Draw is also possible if no pawn
    has moved or a piece has been removed from the board in the last 50 moves. That's called the fifty-moves-rule."""

    def checkGameFinished(self):
        if len(self.getEveryPossibleMove()) == 0:
            if self.stateCheck:  # If this is true it is a checkmate; if not it is a stalemate
                self.playerWon = self.playerBlack if self.playerOnMove == self.playerWhite else self.playerWhite
            self.gameOver = True
            self.notifyObserversWin()
            return True
        elif self.fiftyMovesCounter == 100:
            self.gameOver = True
            self.notifyObserversWin()
            return True

    """ This function is called after every move and it counts every move since the last time a piece was captured or a
    pawn was moved."""

    def countMoves(self, endRow, endColumn):
        self.fiftyMovesCounter = 0 if self.checkFiftyMovesReset(endRow, endColumn) else self.fiftyMovesCounter + 1

    """ Checks if the fifty-moves counter is reset. This happens if a piece was removed or a pawn moved in the last 
    move."""

    def checkFiftyMovesReset(self, endRow, endColumn):
        return True if self.checkIfMoveWithPawn(endRow, endColumn) or self.pieceRemoved else False

    """ This checks if the last move was with a pawn. """

    def checkIfMoveWithPawn(self, row, column):
        piece = self.board.board[row][column]
        return True if isinstance(piece, Pawn) else False

    """ This function checks if at the current position a move is possible."""

    def checkMovePossible(self, startRow, startColumn, endRow, endColumn, playerOnMove):
        move = [[startRow, startColumn], [endRow, endColumn]]
        if str(playerOnMove) == "white":
            return True if move in self.possibleWhiteMoves else False
        else:
            return True if move in self.possibleBlackMoves else False

    """ This function checks if at the current position a castling is possible."""

    def checkForCastlingPossible(self, startRow, startColumn, endRow, endColumn, playerOnMove):
        castling = [[startRow, startColumn], [endRow, endColumn]]
        if str(playerOnMove) == "white":
            return True if castling in self.possibleWhiteCastlings else False
        else:
            return True if castling in self.possibleBlackCastlings else False

    """ These functions update the possible and attacking moves of every piece and update the final list of the moves. 
    The kings have to be updated at the end, because their possible moves depend on the other pieces. Then the moves
    from every piece have to be collected. But first it checks if the piece is in between an attacker and the King.
    If this is the case it updates the piece again."""

    """ This function updates all pieces except for the kings. It collects all the kings and returns them."""

    def updateAllMoves(self):
        self.resetMoves("white")
        self.resetMoves("black")
        kings = []
        board = self.board.board
        for row in range(8):
            for column in range(8):
                piece = board[row][column]
                if isinstance(piece, King):
                    kings.append(piece)
                elif piece is not None:
                    piece.updatePossibleMoves(board)
                    self.setMovesToLists(piece)
        self.updateKings(kings)
        self.getMovesFromPieces(board)
        return kings

    """ This function resets all the possible and attacking moves."""

    def resetMoves(self, playerColor):
        if playerColor == "white":
            self.possibleWhiteMoves = []
            self.attackingWhiteMoves = []
        else:
            self.possibleBlackMoves = []
            self.attackingBlackMoves = []

    """ This function updates the kings."""

    def updateKings(self, kings):
        for king in kings:
            if king.pieceColor == "white":
                king.updatePossibleMoves(self.board.board, kings, self.attackingBlackMoves)
            else:
                king.updatePossibleMoves(self.board.board, kings, self.attackingWhiteMoves)

    """ This function collects the possible moves from the pieces and adds them to the total lists. It also checks for
    every piece if it is pinned (between an attacker and the own king). If that is the case it updates it again before
    it collects the moves."""

    def getMovesFromPieces(self, board):
        self.resetMoves("white")
        self.resetMoves("black")
        for row in range(8):
            for column in range(8):
                piece = board[row][column]
                if piece is not None:
                    if piece.inBetweenAttackerAndKing:
                        piece.updateInBetweenAttackerAndKing()
                    piece.resetInBetweenAttackerAndKing()
                    self.setMovesToLists(piece)

    """ This adds all the moves from a piece to the complete lists."""

    def setMovesToLists(self, piece):
        if piece.pieceColor == "white":
            self.possibleWhiteMoves += piece.possibleMoves
            self.attackingWhiteMoves += piece.attackingMoves
        else:
            self.possibleBlackMoves += piece.possibleMoves
            self.attackingBlackMoves += piece.attackingMoves

    """ This checks if the king from a player is under attack. It searches the king and checks if any other piece is 
    attacking it. Then it collects the position of the attackers. """

    def checkKingUnderAttack(self, playerColor):
        king = []
        attackers = []
        moves = []
        board = self.board.board
        for row in range(8):
            for column in range(8):
                piece = board[row][column]
                if isinstance(piece, King):
                    if piece.pieceColor == playerColor:
                        king = [row, column]
                        attackers = self.findAttackersInCheck(row, column, playerColor)
        for attacker in attackers:
            moves.append([attacker, king])
        return moves

    """ This function checks if any piece is attacking a certain position. It returns the position for all the pieces
    which can. """

    def findAttackersInCheck(self, row, column, playerColor):
        attackers = []
        if playerColor == "black":
            for move in self.attackingWhiteMoves:
                if move[1] == [row, column]:
                    attackers.append(move[0])
        else:
            for move in self.attackingBlackMoves:
                if move[1] == [row, column]:
                    attackers.append(move[0])
        return attackers

    """ This function checks if a pawn has reached the groundline of the opposite player. It is not possible that
    multiple pawns reached it so it returns the player and the position of the pawn if it found one."""

    def checkPawnReachesEndLine(self):
        board = self.board.board
        for n in range(8):
            if isinstance(board[0][n], Pawn):
                return self.playerWhite, 0, n
        for m in range(8):
            if isinstance(board[7][m], Pawn):
                return self.playerBlack, 7, m
        return False

    """ When the king is in check there are only moves allowed which get the player out of the check. There are three
    possibilities. The first one is that the king moves aside. The second one is that another piece blocks the way of
    the attacker. The third one is that another piece gives the attacker. If the king is attacked by more than one
    piece the only possibility is to move the king aside. These functions are only called in a check. First they reset 
    the possible moves and find the moves from the three possibilities. When there are no possible moves it is a 
    checkmate. Of course you could just check if the king is still in check after a move but this way it is a lot
    faster."""

    """ This function is only called if a player is in check. It updates the moves again after it reset them. It checks
    if there is only one attacker or two."""

    def updateInCheck(self, playerInCheck, checkInfo, kings):
        self.resetMoves(str(playerInCheck))
        self.resetCastlings(str(playerInCheck))
        if len(checkInfo) == 1:
            move = checkInfo[0]
            self.updateSingleCheck(playerInCheck, move, kings)
        else:
            self.updateMultipleCheck(checkInfo, kings)

    """ This function updates if the king is attacked by only one piece. It finds the field behind the king. This is the
    only move that is not in the attackingMoves where the king still cant move. It then lets the king update again and
    checks if any piece can block the attacker."""

    def updateSingleCheck(self, playerInCheck, move, kings):
        attacker = self.board.board[move[0][0]][move[0][1]]
        fieldBehind = [self.findFieldBehindKing(move[0][0], move[0][1], move[1][0], move[1][1], attacker)]
        self.updateKingInCheck(move[0][0], move[0][1], move[1][0], move[1][1], fieldBehind, kings)
        self.blockAttackingPieceInCheck(move[0][0], move[0][1], move[1][0], move[1][1], attacker, str(playerInCheck))

    """ This function is called if there are more than one attacker. It first finds the fields behind. Then it lets the
    king update. This is the only possibility to get out of the check if there are more than one attacker."""

    def updateMultipleCheck(self, moves, kings):
        fieldsBehind = []
        move = []
        for move in moves:
            attacker = self.board.board[move[0][0]][move[0][1]]
            fieldsBehind.append(self.findFieldBehindKing(move[0][0], move[0][1], move[1][0], move[1][1], attacker))
        self.updateKingInCheck(move[0][0], move[0][1], move[1][0], move[1][1], fieldsBehind, kings)

    """ This function finds the field behind the king. It is not in the attacked moves but the king still can't move 
    there. But there is only an attacked field behind the king if the attacker is a queen, a bishop or a rook."""

    def findFieldBehindKing(self, attackerRow, attackerColumn, kingRow, kingColumn, attacker):
        if isinstance(attacker, Rook) or isinstance(attacker, Bishop) or isinstance(attacker, Queen):
            return self.getFieldBehind(attackerRow, attackerColumn, kingRow, kingColumn)

    """ This function returns the field behind the king for one attacker. It just checks from where the attacker is
    coming from and the returns the field one behind it."""

    def getFieldBehind(self, attackerRow, attackerColumn, kingRow, kingColumn):
        if attackerRow > kingRow:
            row = kingRow - 1
        elif attackerRow < kingRow:
            row = kingRow + 1
        else:
            row = kingRow
        if attackerColumn > kingColumn:
            column = kingColumn - 1
        elif attackerColumn < kingColumn:
            column = kingColumn + 1
        else:
            column = kingColumn
        return [row, column]

    """ This function updates the king again in a check position. It adds the moves to the field behind. After the
    update it collects the moves from the king."""

    def updateKingInCheck(self, attackerRow, attackerColumn, kingRow, kingColumn, fieldsBehind, kings):
        movesBehindKing = []
        for fieldBehind in fieldsBehind:
            if fieldBehind is not None:
                movesBehindKing.append([[attackerRow, attackerColumn], fieldsBehind, fieldBehind])
        king = self.board.board[kingRow][kingColumn]
        if king.pieceColor == "white":
            king.updatePossibleMoves(self.board.board, kings,
                                     self.attackingBlackMoves + movesBehindKing)
            self.possibleWhiteMoves += king.possibleMoves
        else:
            king.updatePossibleMoves(self.board.board, kings,
                                     self.attackingWhiteMoves + movesBehindKing)
            self.possibleBlackMoves += king.possibleMoves

    """ This finds the fields between the attacker and the king and checks if a piece can move there."""

    def blockAttackingPieceInCheck(self, attackerRow, attackerColumn, kingRow, kingColumn, attacker, playerColor):
        if isinstance(attacker, Queen) or isinstance(attacker, Rook) or isinstance(attacker, Bishop):
            fields = self.getFieldsBetween(attackerRow, attackerColumn, kingRow, kingColumn)
        else:
            fields = [[attackerRow, attackerColumn]]
        self.findPiecesInCheck(fields, [attackerRow, attackerColumn], playerColor)

    def getFieldsBetween(self, attackerRow, attackerColumn, kingRow, kingColumn):
        fields = []
        xDirection = self.findDirection(attackerRow, kingRow)
        yDirection = self.findDirection(attackerColumn, kingColumn)
        length = abs(attackerColumn - kingColumn) if attackerRow == kingRow else abs(attackerRow - kingRow)
        for field in range(0, length, 1):
            row = attackerRow + (field * xDirection)
            column = attackerColumn + (field * yDirection)
            fields.append([row, column])
        return fields

    def findDirection(self, attacker, king):
        return 0 if attacker == king else int(abs(king - attacker) / (king - attacker))

    def findPiecesInCheck(self, fields, attackerField, playerColor):
        for row in range(8):
            for column in range(8):
                self.checkPieceInCheck(self.board.board[row][column], row, column, fields, attackerField, playerColor)

    def checkPieceInCheck(self, piece, row, column, fields, attackerField, playerColor):
        if piece is not None and not isinstance(piece, King):
            if piece.pieceColor == playerColor:
                self.updatePieceInCheck(self.board.board[row][column], fields, attackerField, playerColor)

    def updatePieceInCheck(self, piece, fields, attackerField, playerColor):
        possibleMoves = piece.possibleMoves
        attackingMoves = piece.attackingMoves
        for move in possibleMoves:
            if move[1] in fields:
                self.possibleWhiteMoves.append(move) if playerColor == "white" else self.possibleBlackMoves.append(move)
        for move in attackingMoves:
            if move[2] == attackerField:
                if playerColor == "white":
                    self.possibleWhiteMoves.append([move[0], move[1]])
                    self.attackingWhiteMoves.append(move)
                else:
                    self.possibleBlackMoves.append([move[0], move[1]])
                    self.attackingBlackMoves.append(move)

    """ This updates the castlings. A castling is only possible, if the rook and the king have not moved yet. Also the 
    fields between the rook and the king have to be empty. And the king can not be under attack. As well as the field 
    next to him and the field he is moving to. The castlings get reset and it calculates them again. A castling is saved
    as [[rowOfKingBefore, columnOfKingBefore], [rowOfKingAfter, columnOfKingAfter]]."""

    def updateCastling(self):
        self.resetCastlings("white")
        self.resetCastlings("black")
        self.findFieldsOfCastling()

    def resetCastlings(self, playerColor):
        if playerColor == "white":
            self.possibleWhiteCastlings = []
        else:
            self.possibleBlackCastlings = []

    """ This function finds all the important fields and pieces for every castling. For every potential castling it
    checks if it is possible."""

    def findFieldsOfCastling(self):
        board = self.board.board
        startColumn = 4
        for row in [0, 7]:
            for endColumn in [2, 6]:
                direction = int(abs(endColumn - startColumn) / (endColumn - startColumn))
                if direction == 1:
                    rook = board[row][7]
                    rookColumn = 7
                else:
                    rook = board[row][0]
                    rookColumn = 0
                king = board[row][startColumn]
                self.checkKingAndRook(king, rook, row, startColumn, endColumn, rookColumn, direction)

    """ This function checks if there is a king and and rook on the correct positions and that they both have not moved
    yet. If this is true it calls the next function."""

    def checkKingAndRook(self, king, rook, row, startColumn, endColumn, rookColumn, direction):
        if isinstance(rook, Rook) and isinstance(king, King):
            if rook.onStartingField and king.onStartingField:
                self.checkCastlingUnderAttack(king, row, startColumn, endColumn, rookColumn, king.pieceColor,
                                              direction)

    """ This function checks if any of the fields where the king moves over are under attack. If that is the case the
    function returns and the castling is not possible. Otherwise it checks if the fields between the rook and king are
    empty. Then it lets the castling set to possible."""

    def checkCastlingUnderAttack(self, king, row, startColumn, endColumn, rookColumn, playerColor, direction):
        for i in [0, 1, 2]:
            if self.checkIfUnderAttack(row, startColumn + direction * i, playerColor):
                return
        if self.checkForOpenRow(row, startColumn, rookColumn, direction):
            self.setCastlingPossible(king, row, startColumn, endColumn)

    """ This function checks if any piece from the opposite player is attacking a certain field."""

    def checkIfUnderAttack(self, endRow, endColumn, playerColor):
        if playerColor == "black":
            for move in self.attackingWhiteMoves:
                if move[2] == [endRow, endColumn]:
                    return True
            return False
        else:
            for move in self.attackingBlackMoves:
                if move[2] == [endRow, endColumn]:
                    return True
            return False

    def checkForOpenRow(self, row, startColumn, rookColumn, direction):
        for n in range(startColumn + direction, rookColumn, direction):
            if self.board.board[row][n] is not None:
                return False
        return True

    def setCastlingPossible(self, king, endRow, startColumn, endColumn):
        if king.pieceColor == "white":
            self.possibleWhiteCastlings.append([[endRow, startColumn], [endRow, endColumn]])
        else:
            self.possibleBlackCastlings.append([[endRow, startColumn], [endRow, endColumn]])

    """ This function makes that en passant is not possible after another move between. It iterates through the board
    and checks if a piece is a pawn from the same color. If that is the case it sets the firstLongMove-variable to
    False."""

    def makeNextMoveForEnPassant(self, playerColor):
        board = self.board.board
        for row in range(8):
            for column in range(8):
                self.checkPieceIsPawn(board[row][column], playerColor)

    def checkPieceIsPawn(self, piece, playerColor):
        if isinstance(piece, Pawn):
            if piece.pieceColor == playerColor:
                if piece.firstLongMove:
                    piece.makeSecondMove()

    def getEveryPossibleMove(self):
        if self.playerOnMove == self.playerWhite:
            return self.possibleWhiteMoves + self.possibleWhiteCastlings
        else:
            return self.possibleBlackMoves + self.possibleBlackCastlings

    """ This function gets all the important variables of the current position. This is used when forecasting the game.
    Then it just safes and then resets everything. It returns an array with length of 16. The last two are also arrays.
    """

    def getInfos(self):
        return [self.possibleWhiteMoves,
                self.possibleBlackMoves,
                self.attackingWhiteMoves,
                self.attackingBlackMoves,
                self.possibleWhiteCastlings,
                self.possibleBlackCastlings,
                self.playerWon,
                self.playerOnMove,
                self.gameOver,
                self.stateCheck,
                self.fiftyMovesCounter,
                self.pieceRemoved,
                self.board.whiteOutPieces,
                self.board.blackOutPieces,
                self.getBoardInfos(),
                self.getPieceInfos()]

    """ This function copies the board and its pieces."""

    def getBoardInfos(self):
        newBoard = []
        board = self.board.board
        for row in range(8):
            newBoard.append([])
            for column in range(8):
                newBoard[row].append(board[row][column])
        return newBoard

    """ This function copies all the important variables of the pawns, kings and rooks. They have different variables
    which say for example if a castling is possible."""

    def getPieceInfos(self):
        pawnInfo = []
        kingAndRookInfo = []
        board = self.board.board
        for row in range(8):
            for column in range(8):
                piece = board[row][column]
                if isinstance(piece, Pawn):
                    pawnInfo.append([row, column, piece.firstLongMove, piece.onStartingField])
                elif isinstance(piece, Rook) or isinstance(piece, King):
                    kingAndRookInfo.append([row, column, piece.onStartingField])
        return [pawnInfo, kingAndRookInfo]

    """ This function resets all the infos from a position."""

    def resetInfos(self, infos):
        self.possibleWhiteMoves = infos[0]
        self.possibleBlackMoves = infos[1]
        self.attackingWhiteMoves = infos[2]
        self.attackingBlackMoves = infos[3]
        self.possibleWhiteCastlings = infos[4]
        self.possibleBlackCastlings = infos[5]
        self.playerWon = infos[6]
        self.playerOnMove = infos[7]
        self.gameOver = infos[8]
        self.stateCheck = infos[9]
        self.fiftyMovesCounter = infos[10]
        self.pieceRemoved = infos[11]
        self.board.whiteOutPieces = infos[12]
        self.board.blackOutPieces = infos[13]
        self.resetBoardInfos(infos[14])
        self.resetPieceInfos(infos[15])

    def resetBoardInfos(self, info):
        board = self.board.board
        for row in range(8):
            for column in range(8):
                piece = info[row][column]
                board[row][column] = piece
                if piece is not None:
                    piece.row = row
                    piece.column = column


    def resetPieceInfos(self, info):
        board = self.board.board
        for pawnInfo in info[0]:
            pawn = board[pawnInfo[0]][pawnInfo[1]]
            pawn.firstLongMove = pawnInfo[2]
            pawn.onStartingField = pawnInfo[3]
        for pieceInfo in info[1]:
            piece = board[pieceInfo[0]][pieceInfo[1]]
            piece.onStartingField = pieceInfo[2]

    """ This function returns the inputs for the neural network. These are 770 inputs. 768 are for the board. For every 
    field there are 12 inputs. There are six pieces and two colors. If there is a piece on a certain field it takes the 
    inputPosition and multiplies it with two. If it is a piece from the opposite color it adds one. This number is the
    position where it will have a 1 in these 12 inputs for a field. This happens for every field. The board gets turned
    around if the black player is observing. The sequence of the fields starts always at the field on the top left from
    where the player would watch it. So for white this is a8 and for black this is h1."""

    def getPosition(self, player):
        position = []
        if player == self.playerWhite:
            a, b, c = (0, 8, 1)
        else:
            a, b, c = (7, -1, -1)
        for row in range(a, b, c):
            for column in range(a, b, c):
                field = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                piece = self.board.board[row][column]
                if piece is not None:
                    if piece.pieceColor == player.playerColor:
                        field[piece.inputPosition * 2] = 1
                    else:
                        field[piece.inputPosition * 2 + 1] = 1
                position += field
        position += self.getCastlingInputs(player)
        return position

    """ This function gets the last two inputs for the neural networks. The first one is 1 when the queenside castling
    is possible and the second one when the kingside castling is possible."""

    def getCastlingInputs(self, player):
        castlings = self.possibleWhiteCastlings if player == self.playerWhite else self.possibleBlackCastlings
        position = [0, 0]
        for n in castlings:
            if player == self.playerWhite:
                if n[1][1] == 2:
                    position[0] = 1
                if n[1][1] == 6:
                    position[1] = 1
            else:
                if n[1][1] == 2:
                    position[1] = 1
                if n[1][1] == 6:
                    position[0] = 1
        return position

    """ These functions handle the observers. They get notified when something has changed or when the game is over."""

    def addObserver(self, observer):
        self.observers.append(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update()

    def notifyObserversWin(self):
        for observer in self.observers:
            observer.printWinner()
