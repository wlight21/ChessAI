class Move:
	def __init__(self, src, dst):
		self.src = src
		self.dst = dst
	def __str__(self): return "%s, %s" % (str(self.src), str(self.dst))
