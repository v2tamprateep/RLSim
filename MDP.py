
import sys
import random
import util
# import mazeFunctions

def initMDP(arg):
	move = ["F", "R", "L", "B", "FR", "FL", "BR", "BL"]
	MDP = {}

	infile = open("./TransFuncs/" + arg + ".mdp", "r")
	lst = infile.read().splitlines()

	for line in lst:
		i = 0
		wordlst = line.split()
		first = wordlst[0][:-1]
		MDP[first] = {}
		for word in wordlst:
			isfloat = util.isfloat(word[:-1])
			if isfloat != -1:
				MDP[first][move[i]] = isfloat
				i += 1
	return MDP

class MDP:
	"""
	Organization of MDP:
	{N:{N:n, E:e, W:w, S:s},
	 E:{N:n, E:e, W:w, S:s},
	 W:{N:n, E:e, W:w, S:s},
	 S:{N:n, E:e, W:w, S:s}}
	"""
	def __init__(self, maze, arg):
		self.MDP = initMDP(arg)
		self.maze = maze

	def normalize(self, position, move, legalMoves):
		"""
		If all four moves are possible form a position, does not change
		MDP. If some moves are illegal, adjusts MDP such that the sum
		of all moves = 1
		"""
		total = 0.0
		for act in legalMoves:
			total += self.MDP[move][act]

		newMDP = {}
		for act in legalMoves:
			newMDP[act] = self.MDP[move][act]/total

		return newMDP

	def getMDPMove(self, position, move, legalMoves):
		if move is 'exit': return move

		rand = random.random()
		newMDP = self.normalize(position, move, legalMoves)
		total = 0

		for act in legalMoves:
			total += newMDP[act]
			if rand <= total: return act

		print("getMDPMove -- Error: no move returned")
