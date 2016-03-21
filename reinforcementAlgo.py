
import random
import myUtil as util

class RLAgent(object):

	def __init__(self, Maze, MDP, action_cost):
		self.Maze = Maze
		self.position = Maze.start[0]
		self.orientation = Maze.start[1]
		self.MDP = MDP
		self.action_cost = action_cost

		self.posCounter = util.Counter()
		for key in Maze.maze.keys():
			if (self.Maze.maze[key] != "%"):
				self.posCounter[key] = 0

	def resetAgentState(self):
		self.position = self.Maze.start[0]
		self.orientation = self.Maze.start[1]
		self.posCounter[self.position] += 1

		for state in self.Maze.exploreVal.keys():
			self.Maze.exploreVal[state] += 1

	def nextPosition(self, position, action, orientation):
		direction = util.actionToDirection(orientation, action)
		x, y = position[0], position[1]

		for d in direction:
			if d is 'N': y += 1
			if d is 'E': x += 1
			if d is 'W': x -= 1
			if d is 'S': y -= 1
		return (x, y)

	def updateAgentState(self, action):
		moves = self.Maze.getLegalActions(self.position, self.orientation)
		self.position = self.nextPosition(self.position, action, self.orientation)
		self.orientation = util.actionToDirection(self.orientation, action)
		if ('B' in action):
			self.orientation = util.oppositeAction(self.orientation)
		self.Maze.exploreVal[self.position] = 0
		self.posCounter[self.position] += 1

	def getActionCost(self, action):
		#if ('B' in action): return self.action_cost * 10
		#else: return self.action_cost
		# need to negate the value
		return -max(self.action_cost[a] for a in action)

	def getMove(self):
		pass

	def finishedMaze(self):
		return self.Maze.isTerminal(self.position)

# Q-Learning
class QLearningAgent(RLAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon, action_cost):
		super(QLearningAgent, self).__init__(Maze, MDP, action_cost)
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon

		self.qValues = {}
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
		if util.flipCoin(self.epsilon): moves = [util.randomMove(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]

		#lst = []
		#for move in moves:
		#	explorationReward = self.Maze.getExploreVal(self.nextPosition(self.position, move, self.orientation))
		#	lst.append((self.qValues[(self.position, util.actionToDirection(self.orientation, move))] + explorationReward, move))

		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = util.randomMove(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		direction = util.actionToDirection(self.orientation, mdpMove)

		# Qlearning updates according to BEST action
		self.updateQValue(maxQMove)
		self.updateAgentState(mdpMove)
		return mdpMove

	def updateQValue(self, action):
		nextPos = self.nextPosition(self.position, action, self.orientation)
		currVal = self.qValues[(self.position, util.actionToDirection(self.orientation, action))]
		nextVal = self.computeValueFromQValues(nextPos)

		""" reward = Maze_reward/times_reward_received + cost_of_action + reward_for_exploration """
		#reward = self.Maze.getValue(nextPos) + self.getActionCost(action)
		reward = self.Maze.getDiscountValue(nextPos) + self.getActionCost(action) + self.Maze.getExploreVal(nextPos)
		#reward = self.Maze.getDiscountValue(nextPos) + self.getActionCost(action)

		self.qValues[(self.position, util.actionToDirection(self.orientation, action))] = currVal + self.alpha*(reward + nextVal - currVal)

# SARSA
class SarsaAgent(QLearningAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon, action_cost):
		super(SarsaAgent, self).__init__(Maze, MDP, alpha, gamma, epsilon, action_cost)

	def getMove(self):
		moves = self.Maze.getLegalActions(self.position, self.orientation)
		if util.flipCoin(self.epsilon): moves = [util.randomMove(moves)]

		if (len(moves) == 1):
			self.updateQValue(moves[0])
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]

		#lst = []
		#for move in moves:
		#	explorationReward = self.Maze.getExploreVal(self.nextPosition(self.position, move, self.orientation))
		#	lst.append((self.qValues[(self.position, util.actionToDirection(self.orientation, move))] + explorationReward, move))
			
		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = util.randomMove(tiedMoves)
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
		for state in self.Maze.getLegalStates():
			for direction in self.Maze.getLegalDirections(state):
				self.qValues[(state, direction)] = 0

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
