from Pieces.Piece import Piece
from Pieces.Rook import Rook
from ChessGame.Move import Move
from ChessGame.Castle import Castle

class King(Piece):

	def __init__(self, board, color, square):
		super().__init__(board, color, square)

		self.directions = []
		for i in range(-1, 2):
			for j in range(-1, 2):
				if i == 0 and j == 0: continue
				self.directions.append((i, j))

		self.xray = False
		self.value = 0

	def validMoves(self):

		moves = super().validMoves()

		if self.movecount > 0: return moves

		# short castle
		if (self.board.isFree((chr(ord(self.file()) + 1), self.rank()))
			and self.board.isFree((dst := (chr(ord(self.file()) + 2), self.rank())))
			and isinstance((rook := self.board[(chr(ord(self.file()) + 3), self.rank())]), Rook)
			and rook.movecount == 0):
			moves[dst] = Castle(self.square, dst,
							    Move(rook.square, ((chr(ord(rook.square[0]) - 2), self.rank()))))

		# long castle
		if (self.board.isFree((chr(ord(self.file()) - 1), self.rank()))
			and self.board.isFree((dst := (chr(ord(self.file()) - 2), self.rank())))
			and self.board.isFree((chr(ord(self.file()) - 3), self.rank()))
			and isinstance((rook := self.board[(chr(ord(self.file()) - 4)), self.rank()]), Rook)
			and rook.movecount == 0):
			moves[dst] = Castle(self.square, dst,
							    Move(rook.square, ((chr(ord(rook.square[0]) + 3), self.rank()))))

		return moves
