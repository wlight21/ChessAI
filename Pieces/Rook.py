from Pieces.Piece import Piece

class Rook(Piece):

	def __init__(self, board, color, square):
		super().__init__(board, color, square)
		self.directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
		self.xray = True
		self.value = 5