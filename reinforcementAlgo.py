
# import sys
import random
import myUtil as util

class RLAgent(object):
	def __init__(self, maze, MDP):
		self.maze = maze
		self.position = self.maze.start[0]
		self.orientation = self.maze.start[1]
		self.MDP = MDP

		self.posCounter = util.Counter()
		for key in maze.maze.keys():
			if (self.maze.maze[key] != "%"):
				self.posCounter[key] = 0
		# Agent is in first position at least once
		self.posCounter[self.position] = 1

	def nextPosition(self, position, action, orientation):
		direction = util.actionToDirection(orientation, action)
		x, y = position[0], position[1]

		if direction is 'N': return (x, y + 1)
		if direction is 'E': return (x + 1, y)
		if direction is 'W': return (x - 1, y)
		if direction is 'S': return (x, y - 1)

	def updateAgentState(self, action):
		moves = self.maze.getLegalMoves(self.position, self.orientation)
		self.position = self.nextPosition(self.position, action, self.orientation)
		self.orientation = util.actionToDirection(self.orientation, action)
		if (action == 'B'):
			self.orientation = util.oppositeAction(self.orientation)
		#if (action == 'E' or action == 'W'):
		#	self.orientation = util.actionToDirection(self.orientation, action)
		#	if ('B' not in moves):
		self.posCounter[self.position] += 1

	def getMove(self):
		pass

	def finishedMaze(self):
		return self.maze.isTerminal(self.position)

	def resetPosition(self, start):
		self.position = self.maze.start[0]
		self.orientation = self.maze.start[1]

# Q-Learning
class QLearningAgent(RLAgent):
	def __init__(self, maze, MDP, alpha, gamma, epsilon):
		super(QLearningAgent, self).__init__(maze, MDP)
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.qValues = util.Counter()
        
	def computeValueFromQValues(self, state):
		"""
		Returns max_action Q(state,action)
		where the max is over legal actions.
		"""
		legalActions = self.maze.getLegalMoves(state, self.orientation)
		lst = [self.qValues[(state, act, self.orientation)] for act in legalActions]
		return max(lst)

	def getMove(self):
		moves = self.maze.getLegalMoves(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.qValues[(self.position, move)], move) for move in moves]
		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = random.choice(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		# Qlearning updates according to BEST action
		self.updateQValue(maxQMove)
		self.updateAgentState(mdpMove)
		return mdpMove

	def updateQValue(self, action):
		nextPos = self.nextPosition(self.position, action, self.orientation)
		currVal = self.qValues[(self.position, action, self.orientation)]
		nextVal = self.computeValueFromQValues(nextPos)
		rewardOrCost = self.maze.getValue(nextPos)

		if (rewardOrCost == 0):
			rewardOrCost = -1
			if (action == 'B'): rewardOrCost *= 10

		self.qValues[(self.position, action, self.orientation)] = currVal + self.alpha*(rewardOrCost + nextVal - currVal)

# SARSA
class SarsaAgent(QLearningAgent):
	def __init__(self, maze, MDP, alpha, gamma, epsilon):
		super(SarsaAgent, self).__init__(maze, MDP, alpha, gamma, epsilon)

	def getMove(self):
		moves = self.maze.getLegalMoves(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.qValues[(self.position, move)], move) for move in moves]
		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = random.choice(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		# SARSA updates according to action ACTUALLY TAKEN
		self.updateQValue(mdpMove)
		self.updateAgentState(mdpMove)
		return mdpMove

class FilterQLearningAgent(RLAgent):
	def __init__(self, maze, MDP, alpha, gamma, epsilon, filterType):
		super(FilterQLearningAgent, self).__init__(maze, MDP)
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.inference = filterType
		self.qValues = util.Counter()
	
	def computeValueFromQValues(self, state):
		"""
		Returns max_action Q(state,action)
		where the max is over legal actions.
		"""
		legalActions = self.maze.getLegalMoves(state, self.orientation)
		lst = [self.qValues[(state, act, self.orientation)] for act in legalActions]
		return max(lst)

	def getMove(self):
		self.inference.observeLegalActions(self.position, self.orientation)

		moves = self.maze.getLegalMoves(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.inference.getProbabilisticQVal(self.qValues, move), move) for move in moves]
		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = random.choice(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		# Qlearning updates according to BEST action
		self.updateQValue(maxQMove)
		self.updateAgentState(mdpMove)
		self.inference.elapseTime(mdpMove)
		return mdpMove

	def updateQValue(self, action):
		for pos, ori in self.inference.getPossibleStates():
			nextPos = self.nextPosition(pos, action, ori)
			currVal = self.qValues[(pos, action, ori)]
			nextVal = self.computeValueFromQValues(nextPos)
			rewardOrCost = self.maze.getValue(nextPos)

			if (rewardOrCost == 0):
				rewardOrCost = -0.1
				if (action == 'B'): rewardOrCost *= 10

			self.qValues[(pos, action, ori)] = currVal + self.alpha*(rewardOrCost + nextVal - currVal)

class FilterSarsaAgent(FilterQLearningAgent):
	def __init__(self, maze, MDP, alpha, gamma, epsilon, filterType):
		super(FilterSarsaAgent, self).__init__(maze, MDP, alpha, gamma, epsilon, filterType)

	def getMove(self):
		self.inference.observeLegalActions(self.position, self.orientation)

		moves = self.maze.getLegalMoves(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.inference.getProbabilisticQVal(self.qValues, move), move) for move in moves]
		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = random.choice(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		# Qlearning updates according to BEST action
		self.updateQValue(mdpMove)
		self.updateAgentState(mdpMove)
		self.inference.elapseTime(mdpMove)
		return mdpMove
