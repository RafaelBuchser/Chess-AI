import tkinter as tk
import tkinter.font as tkFont
from Observer import Observer


""" This is a child class from the observer. This is the observer with the GUI. It is made with tkinter. In this file
are also all classes which are needed for the GUI."""


class AppObserver(Observer):
    def __init__(self, game):
        super().__init__(game)
        self.root = tk.Tk()
        self.root.title("chess")
        self.root.geometry("900x900")
        self.root.configure(background="white")
        self.pieceFont = tkFont.Font(family="times new roman", size=37)
        self.normalFont = tkFont.Font(family="times new roman", size=29)
        self.grid = []
        self.frame = tk.Frame(bg="white")  # main frame
        self.boardFrame = tk.Frame(self.frame,  # frame with only the board
                                   width=800,
                                   height=800,
                                   borderwidth=0,
                                   highlightbackground="black",
                                   highlightcolor="black",
                                   highlightthickness=5)
        self.designBoard()
        self.update()

    """ This function designs the board. Every button is saved in the grid-list. It lets the color change for every 
    field and every row."""

    def designBoard(self):
        self.boardFrame.grid(row=1, column=1, rowspan=8, columnspan=8)
        color = "#f0d9b9"
        for row in range(8):
            self.grid.append([])
            for column in range(8):
                field = Field(self.boardFrame, color, "", row, column, self.pieceFont)
                self.grid[row].append(field)
                field.grid(row=row, column=column)
                color = self.switchColor(color)
            color = self.switchColor(color)
        self.designInscription()
        self.frame.pack()

    """ This function switches the color from black to white."""

    def switchColor(self, color):
        return "#b58865" if color == "#f0d9b9" else "#f0d9b9"

    """ This function creates the labeling of the board."""

    def designInscription(self):
        for n in range(1, 9, 1):
            label = tk.Label(self.frame, text=9-n, font=self.normalFont, bg="white", width=2)
            label.grid(row=n, column=0)
        for n in range(1, 9, 1):
            label = tk.Label(self.frame, text=9-n, font=self.normalFont, bg="white", width=2)
            label.grid(row=n, column=9)
        for n in range(1, 9, 1):
            label = tk.Label(self.frame, text=chr(96 + n), font=self.normalFont, bg="white")
            label.grid(row=0, column=n)
        for n in range(1, 9, 1):
            label = tk.Label(self.frame, text=chr(96 + n), font=self.normalFont, bg="white")
            label.grid(row=9, column=n)

    """ This functions updates the observer. It iterates through the whole board and shows every piece on the correct
    field."""

    def update(self):
        board = self.game.board.board
        for row in range(8):
            for column in range(8):
                piece = board[row][column]
                field = self.grid[row][column]
                field.updateField(piece) if piece is not None else field.updateField("")

    """ This function selects a field and makes its color to white and every field where the piece is able to move turns
    grey."""

    def selectPiece(self, possibleMoves, pieceRow, pieceColumn):
        self.grid[pieceRow][pieceColumn].selectThis()
        for move in possibleMoves:
            if move[0][0] == pieceRow and move[0][1] == pieceColumn:
                self.grid[move[1][0]][move[1][1]].possibleMove()

    """ This unselects a field. It basically turns every field to default color."""

    def unselectPiece(self):
        for row in range(8):
            for column in range(8):
                self.grid[row][column].resetThis()

    def chooseNewPiece(self, player):
        return ChoosePiecePopUp(player)

    def printWinner(self):
        WinnerPopUp(self.game.playerWon)


""" This is the class for a field in the GUI-Board. When it is selected it changes its color to white. And when the
piece from the selected field is able to move to this field then it turns grey."""


class Field(tk.Button):
    def __init__(self, boardFrame, color, piece, row, column, font):
        super().__init__(boardFrame,
                         height=1,
                         width=3,
                         text=piece,
                         font=font,
                         bg=color,
                         relief="flat")
        self.color = color
        self.row = row
        self.column = column

    def updateField(self, piece):
        self["text"] = piece

    def selectThis(self):
        self["bg"] = "white"

    def possibleMove(self):
        if self.color == "#f0d9b9":
            self["bg"] = "gray64"
        else:
            self["bg"] = "gray48"

    def resetThis(self):
        self["bg"] = self.color


""" This is the class for the popup that appears when a pawn reaches the back rank. It only has some text and four
buttons to choose the piece from."""


class ChoosePiecePopUp:
    def __init__(self, player):
        self.root = tk.Toplevel()
        self.root.title("")
        self.root.configure(background="white")
        self.titleFont = tkFont.Font(family="times new roman", size=20)
        self.pieceFont = tkFont.Font(family="times new roman", size=40)
        self.whitePieces = ["\u2655", "\u2656", "\u2657", "\u2658"]
        self.blackPieces = ["\u265b", "\u265c", "\u265d", "\u265d"]
        self.player = player
        self.grid = []
        self.title = tk.Label(self.root, text=str(self.player) + " chooses new piece", font=self.titleFont, bg="white")
        self.title.pack()
        self.buttonFrame = tk.Frame(self.root)
        pieces = self.getList()
        column = 0
        for piece in pieces:
            self.grid.append(PieceButton(self.buttonFrame, str(piece), self.pieceFont, column))
            self.grid[column].grid(row=0, column=column)
            column += 1
        self.buttonFrame.pack()

    """ returns a list with the possible pieces."""

    def getList(self):
        return self.whitePieces if str(self.player) == "white" else self.blackPieces


""" This is the class for the buttons in the ChoosePiecePopUp. """


class PieceButton(tk.Button):
    def __init__(self, frame, piece, font, column):
        super().__init__(frame,
                         height=1,
                         width=3,
                         text=piece,
                         font=font,
                         bg="white",
                         relief="flat")
        self.column = column


""" This is the popup that appears when the game is finished."""


class WinnerPopUp:
    def __init__(self, winner):
        self.root = tk.Toplevel()
        self.root.title("")
        self.root.configure(background="white")
        self.root.geometry("400x70")
        self.titleFont = tkFont.Font(family="times new roman", size=20)
        self.winner = winner
        self.text = self.getText()
        self.message = tk.Label(self.root,
                                text=self.text,
                                font=self.titleFont,
                                bg="white")
        self.message.pack()

    def getText(self):
        return "Player " + str(self.winner) + " has won!" if self.winner is not None else "It's a draw!"
