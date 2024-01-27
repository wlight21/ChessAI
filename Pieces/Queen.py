from Pieces.Piece import Piece
from Pieces.Bishop import Bishop
from Pieces.Rook import Rook

class Queen(Piece):

	def __init__(self, board, color, square):
		super().__init__(board, color, square)
		self.value = 9

	def validMoves(self): 
		moves = Bishop(self.board, self.color, self.square).validMoves()
		moves.update(Rook(self.board, self.color, self.square).validMoves())
		return moves
