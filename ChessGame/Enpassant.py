from ChessGame.Move import Move
class Enpassant(Move):
	def __init__(self, src, dst, enpassant):
		super().__init__(src, dst)
		self.enpassant = enpassant