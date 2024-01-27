from Event import Event
from ChessBoard.Board import Board
from ChessGame.GameRules import GameRules

class Game:

	def __init__(self, white, black):

		self.board = Board()
		self.rules = GameRules(self.board)

		self.sig_pieceMoved = Event()
		self.sig_final = Event()

		self.players = (white, black)
		self.players[0].game = self
		self.players[1].game = self
		self.players[0].sig_played.set(self.pieceMoved)
		self.players[1].sig_played.set(self.pieceMoved)

		self.players[0].play()
		
	def validMoves(self, square):
		if square not in self.rules.pieces(self.board.movecount % 2): return {}
		else: return self.rules.validMoves(square)

	def squareSelected(self, square):
		self.players[self.board.movecount % 2].squareSelected(square)

	def pieceMoved(self, move):  
		self.board.move(move)
		self.sig_pieceMoved()

		if self.rules.over():
			if self.rules.check(self.board.movecount % 2): 
				self.sig_final("%s by Checkmate" % (str(self.players[(self.board.movecount + 1) % 2])))
			else:
				self.sig_final("Draw by Stalemate")
		else:
			self.players[self.board.movecount % 2].play()