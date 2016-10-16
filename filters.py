
import util

class ExactInference:
	def __init__(self, Maze, MDP):
		self.maze = Maze
		self.agentMDP = MDP
		self.belief = util.Counter()
		self.initBelief()

	def initBelief(self):
		actions = self.maze.get_legal_actions(self.maze.start[0], self.maze.start[1])
		for pos in self.maze.get_legal_states():
			for ori in ['N', 'E', 'W', 'S']:
				#print(pos, ori)
				#print(actions, self.maze.get_legal_actions(pos, ori))
				if (sorted(actions) == sorted(self.maze.get_legal_actions(pos, ori))):
					self.belief[(pos, ori)] += 1
		self.belief.normalize()	

	def getPossibleStates(self):
		return [(pos, ori) for pos, ori in self.belief.keys() if self.belief[(pos, ori)] > 0]

	def getProbabilisticQVal(self, qVals, action):
		probQval = 0
		for pos, ori in self.getPossibleStates():
			probQval += self.belief[(pos, ori)] * qVals[(pos, util.actionToDirection(ori, action))]
		return probQval

	def observeLegalActions(self, position, orientation):
		actions = self.maze.get_legal_actions(position, orientation)
		for pos, ori in self.getPossibleStates():
			tempActs = self.maze.get_legal_actions(pos, ori)
			if (sorted(actions) != sorted(tempActs)):
				self.belief[(pos, ori)] = 0
		self.belief.normalize()

	def observeCues(self, cue):
		if (cue is None): return
		# pos is the position the cue was observed
		cueType, pos = cue[0], cue[1]
		likelihood = util.Counter()

		if (cueType == 1):
			likelihood[pos] = 1
		elif (cueType == 2):
			for state, ori in self.getPossibleStates():
				if (self.maze.dist_to_walls(pos) == self.maze.dist_to_walls(state)):
					likelihood[state] = 1
		# likelihood.normalize()
		newBelief = util.Counter()
		for state, ori in self.getPossibleStates():
			prob = self.belief[(state, ori)] * likelihood[pos]
			if (prob != 0): newBelief[(state, ori)] = prob
		newBelief.normalize()
		self.belief = newBelief

	def elapseTime(self, action):
		newDist = util.Counter()
		transFunc = self.agentMDP.MDP[action]

		for pos, ori in self.getPossibleStates():
			for act in self.maze.get_legal_actions(pos, ori):
				 newDist[self.nextState(pos, act, ori)] += transFunc[act] * self.belief[(pos, ori)]
		newDist.normalize()
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

