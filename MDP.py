
import sys
import random
import util
# import mazeFunctions

def initMDP(arg):
	move = ["F", "R", "L", "B"]
	MDP = {}

	infile = open("./TransFuncs/" + arg + ".mdp", "r")
	lst = infile.read().splitlines()

	for line in lst:
		i = 0
		MDP[line[0]] = {}
		# print(MDP)	
		for word in line.split():
			isfloat = util.isfloat(word[:-1])
			# print("Current word: " + word[:-1] + " isfloat: " + str(isfloat))
			if isfloat != -1:
				MDP[line[0]][move[i]] = isfloat
				# print(MDP)
				i += 1
	# print(MDP)
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
