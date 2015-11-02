
# import sys
import random
import util

class RLAgent(object):
	maze = None
	position = None
	terminal = None
	MDP = None

	def __init__(self, maze, start, terminal, MDP):
		self.maze = maze
		self.position = start
		self.terminal = terminal
		self.MDP = MDP

	def getMove(self):
		pass

	def finishedMaze(self):
		#return self.position in self.terminal
		return self.position is 'exit'

# Q-Learning
class QLearningAgent(RLAgent):
	alpha = 0
	gamma = 0
	qValues = util.Counter()

	def __init__(self, maze, start, terminal, MDP, alpha, gamma):
		super(QLearningAgent, self).__init__(maze, start, terminal, MDP)
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
		legalActions = 'None'
		if state is not 'exit': legalActions = self.maze.getLegalMoves(state)
			
		#print("LegalActions:", legalActions)
		if len(legalActions) == 0: 
			print("should never be here")
			return 0.0
		
		lst = []
		for act in legalActions:
			lst.append(self.getQValue(state, act))
			#print(state, act, self.getQValue(state, act))
		return max(lst)

	def getMove(self, position):
		moves = self.maze.getLegalMoves(position)

		if len(moves) > 1:
			lst = []
			for move in moves:
				lst.append((self.qValues[(position, move)], move))
		
			best = max(lst)[0]
	
			tiedMoves = []
			for val, move in lst:
				if val == best: tiedMoves.append(move)
			maxQMove = random.choice(tiedMoves)

			self.updateQVal(maxQMove)
			mdpMove = self.MDP.getMDPMove(self.position, maxQMove)
			self.position = self.nextPosition(mdpMove)
			return mdpMove

		self.updateQVal(moves[0])
		self.position = self.nextPosition(moves[0])
		#return random.choice(tiedMoves)
		return moves[0]

	def updateQVal(self, move):
		#currPos = self.position
		nextPos = self.nextPosition(move)

		currVal = self.qValues[(self.position, move)]
		nextVal = self.computeValueFromQValues(nextPos)
		reward = self.maze.getValue(self.position)

		self.qValues[(self.position, move)] = currVal + self.alpha*(reward + self.gamma*nextVal - currVal)
		#print("position", self.position, "reward: ", reward, "qVal: ", self.qValues[(self.position, move)])

		#self.maze.updateMaze(self.position, self.qValues[(self.position, move)])
		print("update:", self.position, move, self.qValues[self.position, move])

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
	def __init__(self, maze, start, terminal, MDP, alpha, gamma):
		super(SarsaAgent, self).__init__(maze, start, terminal, MDP, alpha, gamma)

	def getMove(self, position):
		moves = self.maze.getLegalMoves(position)

		if len(moves) > 1:
			lst = []
			for move in moves:
				lst.append((self.qValues[(position, move)], move))
		
			best = max(lst)[0]
	
			tiedMoves = []
			for val, move in lst:
				if val == best: tiedMoves.append(move)
			maxQMove = random.choice(tiedMoves)

			mdpMove = self.MDP.getMDPMove(self.position, maxQMove)

			# IN SARSA, update happens when move is known
			self.updateQVal(mdpMove)
			self.position = self.nextPosition(mdpMove)
			return mdpMove

		self.updateQVal(moves[0])
		self.position = self.nextPosition(moves[0])
		return moves[0]
