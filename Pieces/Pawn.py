from Pieces.Piece import Piece
from Pieces.Queen import Queen
from ChessGame.Move import Move
from ChessGame.Promotion import Promotion
from ChessGame.Enpassant import Enpassant

class Pawn(Piece):

	def __init__(self, board, color, square):
		super().__init__(board, color, square)
		if self.color == 0: 
			self.directions = [(0, 1)]
			self.promotionRank = max(self.board.ranks)
		else: 
			self.directions = [(0, -1)]
			self.promotionRank = min(self.board.ranks)

		self.value = 1

		# the move on which this pawn utilized it's double open move
		self.doubleOpen = -1

	def move(self, move):
		if self.square[1] + self.directions[0][1]*2 == move.dst[1]: self.doubleOpen = self.board.movecount
		super().move(move)

	def unmove(self, move):
		if self.square[1] - self.directions[0][1]*2 == move.src[1]: self.doubleOpen = self.board.movecount
		super().unmove(move)

	def validMoves(self): 
		moves = self.stdMoves()
		moves.update(self.captureMoves())
		return moves

	def stdMoves(self):
		moves = {}
		if (self.board.isFree((dst := (self.file(), self.rank() + self.directions[0][1])))):
			if dst[1] == self.promotionRank:
				moves[dst] = Promotion(self.square, dst,
								  	   Queen(self.board, self.color, dst))
			else:
				moves[dst] = Move(self.square, dst)

			if (self.board.isFree((dst := (self.file(), self.rank() + self.directions[0][1]*2))) and
				not self.modified()):
				moves[dst] = Move(self.square, dst)

		return moves

	def captureMoves(self):
		moves = {}
		if self.isContested((dst := (chr(ord(self.file()) + 1), self.rank() + self.directions[0][1]))):
			if dst[1] == self.promotionRank:
				moves[dst] = Promotion(self.square, dst,
								  	   Queen(self.board, self.color, dst))
			else:
				moves[dst] = Move(self.square, dst)
		elif (self.isContested((enpassant := (chr(ord(self.file()) + 1), self.rank()))) and
			  isinstance((pawn := self.board[enpassant]), Pawn) and
			  pawn.color != self.color and
			  pawn.movecount == 1 and
			  pawn.doubleOpen == self.board.movecount):
			moves[dst] = Enpassant(self.square, dst, enpassant)

		if self.isContested((dst := (chr(ord(self.file()) - 1), self.rank() + self.directions[0][1]))):
			if dst[1] == self.promotionRank:
				moves[dst] = Promotion(self.square, dst,
								  	   Queen(self.board, self.color, dst))
			else:
				moves[dst] = Move(self.square, dst)
		elif (self.isContested((enpassant := (chr(ord(self.file()) - 1), self.rank()))) and
			  isinstance((pawn := self.board[enpassant]), Pawn) and
			  pawn.color != self.color and
			  pawn.movecount == 1 and
			  pawn.doubleOpen == self.board.movecount):
			moves[dst] = Enpassant(self.square, dst, enpassant)

		return moves
		