from ChessGame.Move import Move
class Castle(Move):
	def __init__(self, src, dst, castle):
		super().__init__(src, dst)
		self.castle = castle
		self.fileincs = [0, 1, 2] if ord(self.dst[0]) > ord(self.src[0]) else [0, -1, -2]
