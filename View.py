import tkinter as tk
from tkinter import *
from tkinter import messagebox

from ChessBoard.Board import Board

from ChessGame.ChessGame import ChessGame
from ChessGame.Human import Human
from ChessGame.AI import AI

from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King

import os

def main():

	# global variable to hold current game being played
	# currentGame = None

	menu = createWindow("Chess AI", "./Icons/icon.ico")

	frame = tk.Frame(menu, bg="gray")
	frame.place(relwidth=0.25, relheight=1)

	humanButton = tk.Button(frame, text="Human vs Human", command=lambda : setupGameWindow(ChessGame(Human(0), Human(1))))
	humanButton.place(relwidth=0.75, relheight=0.05, relx=0.125, rely=0.05)

	aiButton = tk.Button(frame, text="Human vs AI", command=lambda : setupGameWindow(ChessGame(Human(0), AI(1))))
	aiButton.place(relwidth=0.75, relheight=0.05, relx=0.125, rely=0.1)

	menu.mainloop()

# creates and runs a GUI window with the given title and icon
# returns the frame associated with the GUI
def createWindow(title, iconPath):

	root = tk.Tk()
	root.title(title)
	root.iconbitmap(iconPath)

	screenheight = root.winfo_screenheight()
	screenwidth = root.winfo_screenwidth()

	rootheight = int(screenheight // 1.25)
	rootwidth = int(screenheight * 1.25)

	centery = screenheight // 2 - rootheight // 2
	centerx = screenwidth // 2 - rootwidth // 2

	root.geometry(f"{rootwidth}x{rootheight}+{centerx}+{centery}")

	return root

# creates and runs a window representing a chess game
def setupGameWindow(game):
	
	window = createWindow("Play vs Human", "./Icons/icon.ico")

	boardFrame = tk.Frame(window, bg="gray")
	boardFrame.place(relwidth=0.8, relheight=1)

	movesFrame = tk.Frame(window, bg="white")
	movesFrame.place(relwidth=0.2, relheight=1, relx=0.8)

	drawBoard(window, boardFrame, movesFrame, game)

	window.mainloop()

# draws a chess board on the given frame
def drawBoard(window, boardFrame, movesFrame, game):

	buttons = {}
	color = 0
	relx = 0.1
	for file in game.board.files:
		rely = 0.1
		for rank in list(reversed(game.board.ranks)):

			if color % 2 == 0: 
				button = tk.Button(boardFrame, bg="wheat1", activebackground="wheat1", bd=0,
								   command=lambda file=file, rank=rank : selectSquare(window, boardFrame, buttons, game, (file, rank)))
			else: 
				button = tk.Button(boardFrame, bg="burlywood4", activebackground="burlywood4", bd=0,
							       command=lambda file=file, rank=rank : selectSquare(window, boardFrame, buttons, game, (file, rank)))

			buttons[(file, rank)] = button
			button.place(relwidth=0.1, relheight=0.1, relx=relx, rely=rely)

			color += 1
			rely += 0.1

		color += 1
		relx += 0.1

	drawGame(window, boardFrame, buttons, game)

# callback for selecting a square
def selectSquare(window, frame, buttons, game, square): 
	if square in game.availableSquares(): game.pieceMoved(square)
	else: game.pieceSelected(square)
	drawGame(window, frame, buttons, game)

# draws the given game in its current state
def drawGame(window, boardFrame, buttons, game):
	for square in game.board.squares.keys():
		iconpath = iconMatch(game.board.squares[square])
		if iconpath: 
			photo = PhotoImage(master=window, file=iconpath)
			buttons[square].config(image=photo)
			buttons[square].image = photo
		else:
			buttons[square].config(image="")
			buttons[square].image = ""

# matches the type of the given piece to its icon file path
def iconMatch(piece):

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

# run main routine
if __name__ == "__main__": main()