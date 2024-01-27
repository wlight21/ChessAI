from ChessGame.Move import Move

class Piece:

	def __init__(self, board, color, square):

		self.movecount = 0
		self.board = board
		self.color = color
		self.square = square

		# set of directions, defined by tuples, in which this piece can move
		self.directions = None

		# determines whether this piece can move freely in each of its directions
		self.xray = False

		# the value of this piece
		self.value = 0

	def __str__(self): return "%s %s" % ("W" if self.color == 0 else "B", str(type(self).__name__))

	# returns dictionary of valid moves for this piece
	def validMoves(self): 
		
		moves = {}
		for direction in self.directions:

			dst = (chr(ord(self.file()) + direction[0]), self.rank() + direction[1])

			if self.board.isFree(dst): 
				moves[dst] = Move(self.square, dst)
				if self.xray:
					while self.board.isFree((dst := (chr(ord(dst[0]) + direction[0]), dst[1] + direction[1]))):
						moves[dst] = Move(self.square, dst)
					if self.isContested(dst): 
						moves[dst] = Move(self.square, dst)
			elif self.isContested(dst):
				moves[dst] = Move(self.square, dst)

		return moves

	# returns dictionary of capture moves
	# only overidden in Pawn
	def captureMoves(self): return self.validMoves()

	# returns whether this piece has been modified
	def modified(self): return self.movecount != 0

	# getters for file and rank
	def file(self): return self.square[0]
	def rank(self): return self.square[1]

	# moves this piece to the given square
	def move(self, move):
		self.square = move.dst
		self.movecount += 1

	def unmove(self, move):
		self.square = move.src
		self.movecount -= 1

	# returns whether the given square is contested from the 
	# perspective of this piece
	def isContested(self, square):
		return (square[0] in self.board.files and
				square[1] in self.board.ranks and
				self.board[square] and
				self.board[square].color != self.color)