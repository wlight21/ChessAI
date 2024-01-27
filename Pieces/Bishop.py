from Pieces.Piece import Piece

class Bishop(Piece):

	def __init__(self, board, color, square):
		super().__init__(board, color, square)
		self.directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
		self.xray = True
		self.value = 3