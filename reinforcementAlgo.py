
# import sys
import random
import util

class RLAgent(object):
	maze = None
	position = None
	terminal = []

	def __init__(self, maze, start, terminal):
		self.maze = maze
		self.position = start
		self.terminal = terminal

	def getMove(self):
		pass

	def finishedMaze(self):
		return self.position in self.terminal

# Q-Learning
class QLearningAgent(RLAgent):
	alpha = 0
	gamma = 0
	qValues = util.Counter()

	def __init__(self, maze, start, terminal, alpha, gamma):
		super(QLearningAgent, self).__init__(maze, start, terminal)
		self.alpha = alpha
		self.gamma = gamma

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
		legalActions = self.maze.getLegalMoves(self.position)
		if len(legalActions) == 0: return 0.0
		
		lst = []
		for act in legalActions:
			lst.append(self.getQValue(state, act))

		return max(lst)

	def getMove(self, position):
		moves = self.maze.getLegalMoves(position)
		lst = []

		for move in moves:
			lst.append((self.qValues[(position, move)], move))

		best = max(lst)[0]
		tiedMoves = []
		for val, move in lst[1:]:
			if val == best: tiedMoves.append((val, move))

		return random.choice(tiedMoves)[1]

	def update(self, move):
		prev = self.position
		self.position = self.updatePosition(move)

		currVal = self.computeValueFromQValues(self.position)
		preVal = self.computeValueFromQValues(prev)
		reward = self.maze.getValue(prev, move)

		self.qValues[(self.position, move)] = preVal + self.alpha*(reward + self.gamma*currVal - preVal)
		# print("position", self.position, "reward: ", reward, "qVal: ", self.qValues[(self.position, move)])

		self.maze.updateMaze(prev, self.qValues[(self.position, move)])

	def updatePosition(self, direction):
		if direction is "N": return (self.position[0], self.position[1] + 1)
		if direction is "E": return (self.position[0] + 1, self.position[1])
		if direction is "W": return (self.position[0] - 1, self.position[1])
		if direction is "S": return (self.position[0], self.position[1] - 1)
		print("Update failed")

	def resetPosition(self, start):
		self.position = start

