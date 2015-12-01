
# import sys
import random
import util

class RLAgent(object):
	maze = None
	position = None
	terminal = None
	MDP = None
	posCounter = util.Counter()

	def __init__(self, maze, start, terminal, MDP):
		self.maze = maze
		self.position = start
		self.terminal = terminal
		self.MDP = MDP

	def getMove(self):
		pass

	def finishedMaze(self):
		return self.position is 'exit'

# Q-Learning
class QLearningAgent(RLAgent):
	alpha = 0
	gamma = 0
	qValues = util.Counter()

	def __init__(self, maze, start, terminal, MDP, alpha, gamma, epsilon):
		super(QLearningAgent, self).__init__(maze, start, terminal, MDP)
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon

	def getQValue(self, state, action):
		"""
          Returns Q(state,action)
          Should return 0.0 if we have never seen a state
          or the Q node value otherwise
		"""
		return self.qValues[(state, action)]
        
	def computeValueFromQValues(self, state):
		"""
		  Returns max_action Q(state,action)
		  where the max is over legal actions.  Note that if
		  there are no legal actions, which is the case at the
		  terminal state, you should return a value of 0.0.
		"""
		legalActions = 'None'
		if state is not 'exit': legalActions = self.maze.getLegalMoves(state)
			
		if len(legalActions) == 0: 
			print("should never be here")
			return 0.0
		
		lst = []
		for act in legalActions:
			lst.append(self.getQValue(state, act))
		return max(lst)

	def getMove(self):
		moves = self.maze.getLegalMoves(self.position)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if len(moves) > 1:
			lst = []
			for move in moves:
				lst.append((self.qValues[(self.position, move)], move))
			best = max(lst)[0]
	
			tiedMoves = []
			for val, move in lst:
				if val == best: tiedMoves.append(move)
			maxQMove = random.choice(tiedMoves)

			self.update(maxQMove)
			mdpMove = self.MDP.getMDPMove(self.position, maxQMove)
			self.position = self.nextPosition(mdpMove)
			return mdpMove

		self.update(moves[0])
		#mdpMove = self.MDP.getMDPMove(self.position, moves[0])
		self.position = self.nextPosition(moves[0])
		return moves[0]

	def update(self, move):
		self.posCounter[self.position] += 1

		nextPos = self.nextPosition(move)
		currVal = self.qValues[(self.position, move)]
		nextVal = self.computeValueFromQValues(nextPos)
		reward = self.maze.getValue(nextPos)

		self.qValues[(self.position, move)] = currVal + self.alpha*(reward + self.gamma*nextVal - currVal)
		
	def nextPosition(self, direction):
		if direction is 'exit': return 'exit'
		if direction is 'N': return (self.position[0], self.position[1] + 1)
		if direction is 'E': return (self.position[0] + 1, self.position[1])
		if direction is 'W': return (self.position[0] - 1, self.position[1])
		if direction is 'S': return (self.position[0], self.position[1] - 1)
		print("Update failed")

	def resetPosition(self, start):
		self.position = start

class SarsaAgent(QLearningAgent):
	def __init__(self, maze, start, terminal, MDP, alpha, gamma, epsilon):
		super(SarsaAgent, self).__init__(maze, start, terminal, MDP, alpha, gamma, epsilon)

	def getMove(self):
		moves = self.maze.getLegalMoves(self.position)
		if random.random() < self.epsilon: move = [random.choice(moves)]

		if len(moves) > 1:
			lst = []
			for move in moves:
				lst.append((self.qValues[(self.position, move)], move))
		
			best = max(lst)[0]
	
			tiedMoves = []
			for val, move in lst:
				if val == best: tiedMoves.append(move)
			maxQMove = random.choice(tiedMoves)

			mdpMove = self.MDP.getMDPMove(self.position, maxQMove)

			# IN SARSA, update happens when move is known
			self.update(mdpMove)
			self.position = self.nextPosition(mdpMove)
			return mdpMove

		self.update(moves[0])
		self.position = self.nextPosition(moves[0])
		return moves[0]
