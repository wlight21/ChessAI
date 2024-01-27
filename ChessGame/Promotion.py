from ChessGame.Move import Move
class Promotion(Move):
	def __init__(self, src, dst, promotion):
		super().__init__(src, dst)
		self.promotion = promotion