from ChessGame.Move import Move
from ChessGame.Castle import Castle

class GameRules:

	def __init__(self, board): self.board = board

	def pieces(self, color): return self.board.pieces(color)

	def check(self, color):
		for piece in self.pieces((color + 1) % 2).values():
			if self.board.kings[color].square in piece.captureMoves():
				return True
		return False

	def validMoves(self, square): 
		validMoves = {}
		for dst, move in (moves := self.board[square].validMoves()).items():
			if isinstance(move, Castle):
				check = False
				for i in move.fileincs:
					self.board.move((through := Move(move.src, (chr(ord(move.src[0]) + i), move.dst[1]))))
					if self.check((self.board.movecount + 1) % 2): check = True
					self.board.unmove(through)
				if not check: validMoves[dst] = move
			else:
				captured = self.board.move(move)
				if not self.check((self.board.movecount + 1) % 2): validMoves[dst] = move
				self.board.unmove(move, captured)
		return validMoves

	def allMoves(self):
		allMoves = {}
		for square in self.pieces(self.board.movecount % 2):
			allMoves.update(self.validMoves(square))
		return allMoves

	def material(self, color): return self.board.material(color)

	def over(self): 
		for square in self.pieces(self.board.movecount % 2):
			if self.validMoves(square):
				return False
		return True
