from Pieces.Pawn import Pawn
from Pieces.Rook import Rook
from Pieces.Knight import Knight
from Pieces.Bishop import Bishop
from Pieces.Queen import Queen
from Pieces.King import King
from ChessGame.Castle import Castle
from ChessGame.Enpassant import Enpassant
from ChessGame.Promotion import Promotion

class Board:

	def __init__(self):

		self.squares = {}
		self.files = ["A", "B", "C", "D", "E", "F", "G", "H"]
		self.ranks = range(1, 9)

		for file in self.files:
			for rank in self.ranks:
				self[(file, rank)] = None

		# init white
		for file in self.files: self[(file, 2)] = Pawn(self, 0, (file, 2))
		self[("A", 1)] = Rook(self, 0, ("A", 1))
		self[("H", 1)] = Rook(self, 0, ("H", 1))
		self[("B", 1)] = Knight(self, 0, ("B", 1))
		self[("G", 1)] = Knight(self, 0, ("G", 1))
		self[("C", 1)] = Bishop(self, 0, ("C", 1))
		self[("F", 1)] = Bishop(self, 0, ("F", 1))
		self[("D", 1)] = Queen(self, 0, ("D", 1))
		self[("E", 1)] = King(self, 0, ("E", 1))

		# init black
		for file in self.files: self[(file, 7)] = Pawn(self, 1, (file, 7))
		self[("A", 8)] = Rook(self, 1, ("A", 8))
		self[("H", 8)] = Rook(self, 1, ("H", 8))
		self[("B", 8)] = Knight(self, 1, ("B", 8))
		self[("G", 8)] = Knight(self, 1, ("G", 8))
		self[("C", 8)] = Bishop(self, 1, ("C", 8))
		self[("F", 8)] = Bishop(self, 1, ("F", 8))
		self[("D", 8)] = Queen(self, 1, ("D", 8))
		self[("E", 8)] = King(self, 1, ("E", 8))

		self.movecount = 0
		self.kings = [self[("E", 1)], self[("E", 8)]]
		self.mats = [sum([piece.value for piece in self.pieces(0).values()]),
					 sum([piece.value for piece in self.pieces(1).values()])]

	def __getitem__(self, square): return self.squares[square]
	def __setitem__(self, square, val): self.squares[square] = val

	def __str__(self):
		board = []
		for r in self.ranks:
			file = []
			for f in self.files: file.append(str(self[(f, r)]))
			board.append(file)
		return str(board)

	def __hash__(self): return hash(str(self))
	def __eq__(self, o): return hash(self) == hash(o)

	# returns whether the given square is available on the board
	def isFree(self, square):
		return (square[0] in self.files and
				square[1] in self.ranks and
				not self[square])

	# applies the given move
	def move(self, move):
		piece = self[move.src]
		captured = self[move.dst]
		self[move.src] = None
		self[move.dst] = piece
		if isinstance(move, Castle): self.move(move.castle)
		else:
			self.movecount += 1
			if isinstance(move, Enpassant): 
				captured = self[move.enpassant]
				self[move.enpassant] = None
			elif isinstance(move, Promotion): 
				self[move.dst] = move.promotion
				self.mats[move.promotion.color] += move.promotion.value - 1
		piece.move(move)
		if captured: self.mats[captured.color] -= captured.value
		return captured
		
	# unmoves the given move
	def unmove(self, move, captured=None):
		piece = self[move.dst]
		self[move.dst] = captured
		self[move.src] = piece
		if isinstance(move, Castle): self.unmove(move.castle)
		else:
			self.movecount -= 1
			if isinstance(move, Enpassant): 
				self[move.dst] = None
				self[move.enpassant] = captured
			elif isinstance(move, Promotion): 
				self[move.src] = Pawn(self, move.promotion.color, move.src)
				self.mats[move.promotion.color] -= move.promotion.value - 1
		if captured: self.mats[captured.color] += captured.value
		piece.unmove(move)

	# returns the pieces for the given color
	def pieces(self, color):
		return { square:piece for square,piece in self.squares.items() if piece != None and piece.color == color }

	# returns the sum of material for the given player
	def material(self, color): return self.mats[color]