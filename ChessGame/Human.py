from ChessGame.Player import Player
from ChessGame.Move import Move

class Human(Player):

	def __init__(self, color):
		super().__init__(color)
		self.src = None

	def squareSelected(self, square):
		if square in self.game.rules.pieces(self.color):
			self.src = square
		elif self.src and square in (validMoves := self.game.rules.validMoves(self.src)):
			self.sig_played(validMoves[square])
			self.src = None

