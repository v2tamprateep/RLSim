
import random
import myUtil as util

class RLAgent(object):

	def __init__(self, Maze, MDP, actionCost = -1):
		self.Maze = Maze
		self.position = self.Maze.start[0]
		self.orientation = self.Maze.start[1]
		self.MDP = MDP

		self.posCounter = util.Counter()
		for key in Maze.maze.keys():
			if (self.Maze.maze[key] != "%"):
				self.posCounter[key] = 0

		# Agent is in first position at least once
		self.posCounter[self.position] = 1
		self.actCosts = {'F': actionCost, 'R':actionCost, 'B':actionCost*10, 'L':actionCost}

	def nextPosition(self, position, action, orientation):
		direction = util.actionToDirection(orientation, action)
		x, y = position[0], position[1]

		if direction is 'N': return (x, y + 1)
		if direction is 'E': return (x + 1, y)
		if direction is 'W': return (x - 1, y)
		if direction is 'S': return (x, y - 1)

	def updateAgentState(self, action):
		moves = self.Maze.getLegalActions(self.position, self.orientation)
		self.position = self.nextPosition(self.position, action, self.orientation)
		self.orientation = util.actionToDirection(self.orientation, action)
		if (action == 'B'):
			# if ()
			self.orientation = util.oppositeAction(self.orientation)

		self.posCounter[self.position] += 1

	def getMove(self):
		pass

	def finishedMaze(self):
		return self.Maze.isTerminal(self.position)

	def resetPosition(self, start):
		self.position = self.Maze.start[0]
		self.orientation = self.Maze.start[1]
		for state in self.Maze.exploreVal.keys():
			self.Maze.exploreVal[state] += 1

# Q-Learning
class QLearningAgent(RLAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon):
		super(QLearningAgent, self).__init__(Maze, MDP)
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon

		self.qValues = util.Counter()
		for state in self.Maze.getLegalStates():
			for direction in self.Maze.getLegalDirections(state):
				self.qValues[(state, direction)] = 0
        
	def computeValueFromQValues(self, state):
		"""
		Returns max_action Q(state,action)
		where the max is over legal actions.
		"""
		legalActions = self.Maze.getLegalActions(state, self.orientation)
		lst = [self.qValues[(state, util.actionToDirection(self.orientation, act))] for act in legalActions]
		return max(lst)

	def getMove(self):
		moves = self.Maze.getLegalActions(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]

		# lst = []
		# for (move in moves):
		# 	explorationReward = self.Maze.getExploreVal(self.nextPosition(self.position, action, self.orientation))
		# 	lst.append((self.qValues[(self.position, util.actionToDirection(self.orientation, move))] + explorationReward, move))

		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = random.choice(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		# Qlearning updates according to BEST action
		self.updateQValue(maxQMove)
		self.updateAgentState(mdpMove)
		return mdpMove

	def updateQValue(self, action):
		# print("-----------------------")
		# print(self.qValues)
		nextPos = self.nextPosition(self.position, action, self.orientation)
		currVal = self.qValues[(self.position, util.actionToDirection(self.orientation, action))]
		nextVal = self.computeValueFromQValues(nextPos)

		""" reward = Maze_reward/times_reward_received + cost_of_action + reward_for_exploration """
		reward = self.Maze.getValue(nextPos) + self.actCosts[action]
		# reward = self.Maze.getValue(nextPos)/(1 + self.posCounter[nextPos]) + self.actCosts[action] + self.Maze.getExploreVal(nextPos)
		# reward = self.Maze.getValue(nextPos)/(1 + self.posCounter[nextPos]) + self.actCosts[action]

		self.qValues[(self.position, util.actionToDirection(self.orientation, action))] = currVal + self.alpha*(reward + nextVal - currVal)

# SARSA
class SarsaAgent(QLearningAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon):
		super(SarsaAgent, self).__init__(Maze, MDP, alpha, gamma, epsilon)

	def getMove(self):
		moves = self.Maze.getLegalActions(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]
		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = random.choice(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		# SARSA updates according to action ACTUALLY TAKEN
		self.updateQValue(mdpMove)
		self.updateAgentState(mdpMove)
		return mdpMove

class FilterQLearningAgent(RLAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon, filterType):
		super(FilterQLearningAgent, self).__init__(Maze, MDP)
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.inference = filterType
		self.qValues = util.Counter()

	def resetPosition(self, start):
		self.position = self.Maze.start[0]
		self.orientation = self.Maze.start[1]
		self.inference.initBelief()

	def computeValueFromQValues(self, state):
		"""
		Returns max_action Q(state,action)
		where the max is over legal actions.
		"""
		legalActions = self.Maze.getLegalActions(state, self.orientation)
		lst = [self.qValues[(state, util.actionToDirection(self.orientation, act))] for act in legalActions]
		return max(lst)

	def getMove(self):
		self.inference.observeLegalActions(self.position, self.orientation)
		self.inference.observeCues(self.Maze.getCues(self.position))

		moves = self.Maze.getLegalActions(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			self.inference.elapseTime(moves[0])
			return moves[0]

		lst = [(self.inference.getProbabilisticQVal(self.qValues, move), move) for move in moves]

		# lst = []
		# for (move in moves):
		# 	explorationReward = self.Maze.getExploreVal(self.nextPosition(self.position, action, self.orientation))
		# 	lst.append((self.qValues[(self.position, util.actionToDirection(self.orientation, move))] + explorationReward, move))
		
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
			currVal = self.qValues[(pos, util.actionToDirection(ori, action))]
			nextVal = self.computeValueFromQValues(nextPos)

			""" reward = Maze_reward/times_reward_received + cost_of_action + reward_for_exploration """
			reward = self.Maze.getValue(nextPos)/(1 + self.posCounter[nextPos]) + self.actCosts[action] + self.Maze.getExploreVal(nextPos)
			# reward = self.Maze.getValue(nextPos)/(1 + self.posCounter[nextPos]) + self.actCosts[action]

			self.qValues[(pos, util.actionToDirection(ori, action))] = currVal + self.alpha*(reward + nextVal - currVal)

class FilterSarsaAgent(FilterQLearningAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon, filterType):
		super(FilterSarsaAgent, self).__init__(Maze, MDP, alpha, gamma, epsilon, filterType)

	def getMove(self):
		self.inference.observeLegalActions(self.position, self.orientation)

		moves = self.Maze.getLegalActions(self.position, self.orientation)
		if random.random() < self.epsilon: moves = [random.choice(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			self.inference.elapseTime(moves[0])
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
