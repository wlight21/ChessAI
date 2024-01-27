from ChessBoard.Board import Board
from Event import Event

class Player:

	def __init__(self, color):

		self.color = color
		self.oppColor = (color + 1) % 2

		# decided by the game to which this player belongs
		self.game = None

		self.sig_played = Event()

	def __str__(self): return "White" if self.color == 0 else "Black"

	def play(self): pass

	def squareSelected(self, square): pass

	def validMoves(self):
		validMoves = {}
		for square, piece in self.game.rules.pieces(self.color).items():
			validMoves.update(self.game.rules.validMoves(square))
		return validMoves