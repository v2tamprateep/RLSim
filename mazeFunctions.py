
import myUtil as util

# read in maze file and store in dictionary
def initMaze(arg, reward):
	infile = open("./Layouts/" + arg + ".lay", "r")
	lst = infile.read().splitlines()

	start = 0
	terminal = []
	dictionary = {}
	cues = {}
	x, y, = 0, 0

	for line in lst[::-1]:
		for char in line:
			if str(char) == "R":
				dictionary[(x, y)] = reward
				terminal.append((x, y))
			elif char != '%':
				dictionary[(x, y)] = 0
			else:
				dictionary[(x, y)] = char

			dirSymbols = ['^', '>', 'v', '<']
			if str(char) in dirSymbols:
				directions = ['N', 'E', 'S', 'W']
				start = ((x, y), directions[dirSymbols.index(str(char))])

			if (str(char).isalpha()):
				cues[(x, y)] = 2 
			x += 1
		x = 0
		y += 1

	infile.close()
	return (dictionary, start, terminal, cues)

class Maze:
	def __init__(self, arg, reward, reset):
		self.reset, self.discount = reset, 1
		self.maze, self.start, self.terminal, self.cues = initMaze(arg, reward)
		self.exploreVal = {state:1 for state in self.maze.keys()}
		self.exploreVal[self.start] = 0

	def getLegalStates(self):
		return [state for state in self.maze.keys() if self.maze[state] != '%']
		
	def getLegalActions(self, position, orientation):
		"""
		returns list of possible moves
		"""
		directions = self.getLegalDirections(position)
		return util.directionToActionLst(orientation, directions)

	def getLegalDirections(self, position):
		"""
		returns list of possible moves
		"""
		directions = []
		x, y = position[0], position[1]

		if self.maze[(x, y + 1)] is not '%': directions.append('N')
		if self.maze[(x + 1, y)] is not '%': directions.append('E')
		if self.maze[(x - 1, y)] is not '%': directions.append('W')
		if self.maze[(x, y - 1)] is not '%': directions.append('S')
		if self.maze[(x - 1, y + 1)] is not '%': directions.append('NW')
		if self.maze[(x - 1, y - 1)] is not '%': directions.append('SW')
		if self.maze[(x + 1, y + 1)] is not '%': directions.append('NE')
		if self.maze[(x + 1, y - 1)] is not '%': directions.append('SE')

		return directions

	def getCues(self, position):
		"""
		return (cueType, position)
		"""
		try:
			return (self.cues[position], position)
		except:
			return None

	def getValue(self, position):
		if (position == "exit"): return 0
		return self.maze[position]

	def getDiscountValue(self, position):
		if util.flipCoin(self.reset): self.discount = 1
		ret = self.maze[position]/self.discount
		self.discount += 1
		return ret

	def updateMaze(self, position, value):
		self.maze[position] = value

	def distToWalls(self, position):
		dic, x, y = {}, position[0], position[1]
		for direction, dx, dy in [('N', 0, 1), ('E', 0, 1), ('W', 0, -1), ('S', -1, 0)]:
			count, i = 0, 0
			while self.getValue((x + dx*i, y + dy*i)) != '%':
				count += 1
				i += 1
			dic[direction] = count
		return dic

	def getExploreVal(self, position):
		return self.exploreVal[position]

	def isTerminal(self, position):
		if position in self.terminal: 
			return True
		return False
