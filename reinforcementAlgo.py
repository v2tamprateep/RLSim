
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
		return -max(self.action_cost[a] for a in action)

	def getMove(self):
		pass

	def finishedMaze(self):
		return self.Maze.isTerminal(self.position)

# Q-Learning
class QLearningAgent(RLAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon, action_cost, learning):
		super(QLearningAgent, self).__init__(Maze, MDP, action_cost)
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.qValues = {}
		self.learning_mode = learning

		self.resetQValues()

	def resetQValues(self):
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

		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = util.randomMove(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		direction = util.actionToDirection(self.orientation, mdpMove)

		self.updateQValue(maxQMove)
		self.updateAgentState(mdpMove)
		return mdpMove

	def updateQValue(self, action):
		nextPos = self.nextPosition(self.position, action, self.orientation)
		currVal = self.qValues[(self.position, util.actionToDirection(self.orientation, action))]
		nextVal = self.computeValueFromQValues(nextPos)

		if self.learning_mode == 1: # std
			reward = self.Maze.getValue(nextPos) + self.getActionCost(action)
		elif self.learning_mode == 2: # RD
			reward = self.Maze.getDiscountValue(nextPos) + self.getActionCost(action)
		elif self.learning_mode == 3: # ER
			reward = self.Maze.getValue(nextPos) + self.getActionCost(action) + self.Maze.getExploreVal(nextPos)
		elif self.learning_mode == 4: # RDER
			reward = self.Maze.getDiscountValue(nextPos) + self.getActionCost(action) + self.Maze.getExploreVal(nextPos)

		self.qValues[(self.position, util.actionToDirection(self.orientation, action))] = currVal + self.alpha*(reward + nextVal - currVal)

# SARSA
class SarsaAgent(QLearningAgent):
	def __init__(self, Maze, MDP, alpha, gamma, epsilon, action_cost, learning):
		super(SarsaAgent, self).__init__(Maze, MDP, alpha, gamma, epsilon, action_cost, learning)
		self.prev_state, self.prev_action, self.prev_dir = None, None, None

	def finishedMaze(self):
		"""
		We need to overload finishedMaze function to update the Q-value of the state leading to the terminal state;
		we also need to reset the previous state
		"""
		if self.Maze.isTerminal(self.position):
			self.updateQValue(self.prev_state, self.prev_dir, self.position, "exit")
			self.prev_state, self.prev_action, self.prev_dir = None, None, None
			return True
			
		return False

	def getMove(self):
		"""
		wrapper function for getting the next move and updating Q-values
		"""
		if (self.prev_action is None):
			return self.find_move()
		else:
			return self.find_and_update_move()

	def find_move(self):
		"""
		first move by sarsa agent; selects a mvoe but doesn't update
		"""
		moves = self.Maze.getLegalActions(self.position, self.orientation)
		if util.flipCoin(self.epsilon): moves = [util.randomMove(moves)]

		if (len(moves) == 1):
			# update "previous" moves
			self.prev_state = self.position
			self.prev_dir = util.actionToDirection(self.orientation, moves[0])
			self.prev_action = moves[0]

			# update agent state
			self.updateAgentState(moves[0])
			return moves[0]

		lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]

		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = util.randomMove(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		# update "previous" moves
		self.prev_state = self.position
		self.prev_dir = util.actionToDirection(self.orientation, mdpMove)
		self.prev_action = mdpMove

		# update agent state
		self.updateAgentState(mdpMove)
		return mdpMove

	def find_and_update_move(self):
		"""
		Subsequent moves by sarsa agent; gets move and upadtes Q-values
		"""
		moves = self.Maze.getLegalActions(self.position, self.orientation)
		if util.flipCoin(self.epsilon): moves = [util.randomMove(moves)]

		# if only one move, just take that one
		if (len(moves) == 1):
			direction = util.actionToDirection(self.orientation, moves[0])
			self.updateQValue(self.prev_state, self.prev_dir, self.position, direction)

			# update "previous" moves
			self.prev_state = self.position
			self.prev_dir = direction
			self.prev_action = moves[0]

			# update agent state
			self.updateAgentState(moves[0])
			return moves[0]

		# otherwise, find best move
		lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]

		best = max(lst)[0]
	
		tiedMoves = [move for val, move in lst if val == best]
		maxQMove = util.randomMove(tiedMoves)
		mdpMove = self.MDP.getMDPMove(self.position, maxQMove, moves)

		direction = util.actionToDirection(self.orientation, mdpMove)
		# update Q-values
		self.updateQValue(self.prev_state, self.prev_dir, self.position, direction)

		# update "previous" moves
		self.prev_state = self.position
		self.prev_dir = direction
		self.prev_action = mdpMove

		# update agent state
		self.updateAgentState(mdpMove)
		return mdpMove

	def updateQValue(self, s1, d1, s2, d2):
		# print("---------- NEW ITERATION ----------")
		# print("s1: {0}; d1: {1}; s2: {2}; d2: {3}".format(s1, d1, s2, d2))
		currVal = self.qValues[(s1, d1)]

		if d2 == "exit":
			nextVal = 0
		else:
			nextVal = self.qValues[(s2, d2)]

		if self.learning_mode == 1:
			reward = self.Maze.getValue(s2) + self.getActionCost(self.prev_action)
		elif self.learning_mode == 2:
			reward = self.Maze.getDiscountValue(s2) + self.getActionCost(self.prev_action)
		elif self.learning_mode == 3:
			reward = self.Maze.getValue(s2) + self.getActionCost(self.prev_action) + self.Maze.getExploreVal(s2)
		elif self.learning_mode == 4:
			reward = self.Maze.getDiscountValue(s2) + self.getActionCost(self.prev_action) + self.Maze.getExploreVal(s2)
		# print("Before: {0} = {1}".format((s1, d1), self.qValues[(s1, d1)]))
		self.qValues[(s1, d1)] = currVal + self.alpha*(reward + nextVal - currVal)
		# print("After:  {0} = {1}".format((s1, d1), self.qValues[(s1, d1)]))
		# print("-----------------------------------")


"""
Filter-Based Agents
"""
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
