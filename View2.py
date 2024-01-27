import tkinter as tk
from tkinter import *
from tkinter import messagebox

from ChessBoard.Board import Board

from ChessGame.Game import Game
from ChessGame.Human import Human
from ChessGame.AI import AI

from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King

from Event import Event

import os

# frame wrapper class to display a chess game
# a frame is a placeable container which can hold widgets
class ChessWindow(tk.Tk):

	def __init__(self, game):

		root = tk.Tk()
		root.title("Chess Game")
		root.iconbitmap("./Icons/icon.ico")

		screenheight = root.winfo_screenheight()
		screenwidth = root.winfo_screenwidth()

		rootheight = int(screenheight // 1.25)
		rootwidth = int(screenheight * 1.25)

		centery = screenheight // 2 - rootheight // 2
		centerx = screenwidth // 2 - rootwidth // 2

		root.geometry(f"{rootwidth}x{rootheight}+{centerx}+{centery}")

		self.boardFrame = tk.Frame(root, bg="gray")
		self.movesFrame = tk.Frame(root, bg="white")

		self.boardFrame.place(relwidth=0.8, relheight=1)
		self.movesFrame.place(relwidth=0.2, relheight=1, relx=0.8)

		movesLabel = tk.Label(self.movesFrame, text="Moves:\n", bg="white")
		movesLabel.place(relwidth=1, relheight=1)
		movesLabel.pack(anchor=NW)

		self.game = game
		self.game.sig_pieceMoved.set(self.drawGame)
		self.game.sig_final.set(self.finish)

		self.buttons = {}
		self.drawBoard()

	def finish(self, result): messagebox.showinfo("Game Over", result, master=self.boardFrame)

	def addButton(self, square, button): self.buttons[square] = button

	def squareSelected(self, square): 
		self.drawAvailableSquares(self.game.validMoves(square))
		self.game.squareSelected(square)

	def drawBoard(self):

		relx = 0.1
		for file in self.game.board.files:
			label = tk.Label(self.boardFrame, text=file, bg="gray", font=("Calibri", 14))
			label.place(relwidth=0.1, relheight=0.1, relx=relx, rely=0.9)
			relx += 0.1

		rely = 0.8
		for rank in self.game.board.ranks:
			label = tk.Label(self.boardFrame, text=str(rank), bg="gray", font=("Calibri", 14))
			label.place(relwidth=0.1, relheight=0.1, relx=0, rely=rely)
			rely -= 0.1
		
		color = 1
		relx = 0.1
		for file in self.game.board.files:
			rely = 0.8
			for rank in self.game.board.ranks:
				if color % 2 == 0: 
					self.addButton(
						(file, rank), 
						SquareButton(self, (file, rank), 0, "wheat1", relx, rely)
						)
				else: 
					self.addButton(
						(file, rank), 
						SquareButton(self, (file, rank), 1, "burlywood4", relx, rely)
						)

				color += 1
				rely -= 0.1

			color += 1
			relx += 0.1

		self.drawGame()

	def drawGame(self):
		for square in self.buttons.keys():
			self.buttons[square].addImage(pngMatch(self.game.board[square]))

	def drawAvailableSquares(self, squares):
		for square in self.buttons.keys():
			if square in squares: self.buttons[square].setAvailable()
			else: self.buttons[square].setUnavailable()

# button wrapper class to represent a chess square
class SquareButton(tk.Button):

	def __init__(self, window, square, color, bg, relx, rely):

		self.window = window
		self.square = square
		self.color = color

		super().__init__(window.boardFrame, bg=bg, activebackground=bg, bd=0,
									   command=self.command)
		self.place(relwidth=0.1, relheight=0.1, relx=relx, rely=rely)

	def addImage(self, path):
		if path:
			img = PhotoImage(master=self.window.boardFrame, file=path)
			self.config(image=img)
			self.image = img
		else:
			self.config(image="")
			self.image = ""

	def command(self): self.window.squareSelected(self.square)
	def setAvailable(self): self.config(relief=GROOVE, bd=5)
	def setUnavailable(self): self.config(relief=FLAT, bd=0)

# matches the type of the given piece to its png file path
def pngMatch(piece):

	if not piece: return ""

	if piece.color == 0:
		if isinstance(piece, Pawn): return "./Icons/w_pawn.png"
		if isinstance(piece, Rook): return "./Icons/w_rook.png"
		if isinstance(piece, Knight): return "./Icons/w_knight.png"
		if isinstance(piece, Bishop): return "./Icons/w_bishop.png"
		if isinstance(piece, King): return "./Icons/w_king.png"
		if isinstance(piece, Queen): return "./Icons/w_queen.png"
	else:
		if isinstance(piece, Pawn): return "./Icons/b_pawn.png"
		if isinstance(piece, Rook): return "./Icons/b_rook.png"
		if isinstance(piece, Knight): return "./Icons/b_knight.png"
		if isinstance(piece, Bishop): return "./Icons/b_bishop.png"
		if isinstance(piece, King): return "./Icons/b_king.png"
		if isinstance(piece, Queen): return "./Icons/b_queen.png"

# program entry point
def main():
	
	menu = tk.Tk()
	menu.title("Chess AI")
	menu.iconbitmap("./Icons/icon.ico")

	screenheight = menu.winfo_screenheight()
	screenwidth = menu.winfo_screenwidth()

	rootheight = int(screenheight // 1.25)
	rootwidth = int(screenheight * 1.25)

	centery = screenheight // 2 - rootheight // 2
	centerx = screenwidth // 2 - rootwidth // 2

	menu.geometry(f"{rootwidth}x{rootheight}+{centerx}+{centery}")

	frame = tk.Frame(menu, bg="gray")
	frame.place(relwidth=0.25, relheight=1)

	humanButton = tk.Button(frame, text="Human vs Human", command=lambda : ChessWindow(Game(Human(0), Human(1))))
	humanButton.place(relwidth=0.75, relheight=0.05, relx=0.125, rely=0.05)

	aiButton = tk.Button(frame, text="Human vs AI", command=lambda : ChessWindow(Game(Human(0), AI(1))))
	aiButton.place(relwidth=0.75, relheight=0.05, relx=0.125, rely=0.1)

	menu.mainloop()

if __name__ == "__main__": main()