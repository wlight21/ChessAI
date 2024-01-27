from ChessGame.Player import Player
from ChessGame.Move import Move
import random

class AI(Player):

	def __init__(self, color):
		super().__init__(color)
		self.MAX_DEPTH = 2

	def play(self): 
		evals = {}
		for move in self.validMoves().values():
			captured = self.game.board.move(move)
			evals[move] = self.eval_r()
			self.game.board.unmove(move, captured)

		for move, value in evals.items(): print("%s: %f" % (move, value))
		print("<------------------------------------------------------>")

		if self.color == 0: self.sig_played(max(evals, key=evals.get))
		else: self.sig_played(min(evals, key=evals.get))

	def eval(self): 
		if self.game.rules.over():
			if self.game.rules.check(0): return float('-inf')
			if self.game.rules.check(1): return float('inf')
			return 0

		return (self.game.rules.material(0) -
				self.game.rules.material(1))

	def eval_r(self, depth=1, alpha=float('-inf'), beta=float('inf'), evals = {}):
		# if self.game.board in evals: return evals[self.game.board]
		if depth == self.MAX_DEPTH * 2: return self.eval()
		if self.game.board.movecount % 2 == 0: return self.max(depth, alpha, beta, evals)
		else: return self.min(depth, alpha, beta, evals)

	def max(self, depth, alpha, beta, evals): 
		value = float('-inf')
		for move in self.game.rules.allMoves().values():
			captured = self.game.board.move(move)
			value = max(value, self.eval_r(depth + 1, alpha, beta, evals))
			self.game.board.unmove(move, captured)
			if value > beta: break
			alpha = max(value, alpha)
		# evals[self.game.board] = value
		return value

	def min(self, depth, alpha, beta, evals): 
		value = float('inf')
		for move in self.game.rules.allMoves().values():
			captured = self.game.board.move(move)
			value = min(value, self.eval_r(depth + 1, alpha, beta, evals))
			self.game.board.unmove(move, captured)
			if value < alpha: break
			beta = min(value, beta)
		# evals[self.game.board] = value
		return value
