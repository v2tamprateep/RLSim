
import myUtil as util

class ExactInference:
	def __init__(self, Maze, MDP):
		self.maze = Maze
		self.agentMDP = MDP

		# initialize belief as normal distribution over all legal states
		self.belief = util.Counter()
		actions = self.maze.getLegalMoves(self.maze.start[0], self.maze.start[1])
		for pos in self.maze.getLegalStates():
			for ori in ['N', 'E', 'W', 'S']:
				if (actions == self.maze.getLegalMoves(pos, ori)):
					self.belief[(pos, ori)] += 1
		self.belief.normalize()

	def getPossibleStates(self):
		return [(pos, ori) for pos, ori in self.belief.keys() if self.belief[(pos, ori)] > 0]

	def getProbabilisticQVal(self, qVals, action):
		probQval = 0
		for pos, ori in self.getPossibleStates():
			probQval += self.belief[(pos, ori)] * qVals[(pos, action, ori)]
		return probQval

	def getProbabilisticReward(self, action):
		transFunc = self.agentMDP.MDP[action]
		probR = 0
		for pos, ori in self.getPossibleStates():
			for mdpMove in self.maze.getLegalMoves(pos, ori):
				newPos = self.nextState(pos, mdpMove, ori)[0]
				probR += self.maze.getValue(newPos) * transFunc[mdpMove] * self.belief[(pos, ori)]
		return probR

	def observeLegalActions(self, position, orientation):
		actions = self.maze.getLegalMoves(position, orientation)

		for pos, ori in self.getPossibleStates():
			tempActs = self.maze.getLegalMoves(pos, ori)
			if (actions != tempActs):
				self.belief[(pos, ori)] = 0
		self.belief.normalize()

	def observeCues(self):
		# TODO
		pass

	def elapseTime(self, action):
		newDist = util.Counter()
		transFunc = self.agentMDP.MDP[action]

		for pos, ori in self.getPossibleStates():
			for act in  self.maze.getLegalMoves(pos, ori):
				newDist[self.nextState(pos, act, ori)] += transFunc[act] * self.belief[(pos, ori)]
		newDist.normalize()
		#print(newDist)
		self.belief = newDist
		#TODO double check this function

	def nextState(self, position, action, orientation):
		direction = util.actionToDirection(orientation, action)
		x, y = position[0], position[1]

		if (direction is 'N'): y += 1
		elif (direction is 'E'): x += 1
		elif (direction is 'W'): x -= 1
		elif (direction is 'S'): y -= 1

		if (action == 'B'): direction = util.oppositeAction(direction)
		return ((x, y), direction)

class ParticleFilter(object):
	# Class variables
	particles = util.Counter()
	agentMDP = None

	def __init__():
		self.particles.incrementAll()

