from Pieces.Piece import Piece

class Knight(Piece):

	def __init__(self, board, color, square):
		super().__init__(board, color, square)
		self.directions = [(2, 1), (2, -1), (-2, 1), (-2, -1), (1, 2), (1, -2), (-1, 2), (-1, -2)]
		self.xray = False
		self.value = 3