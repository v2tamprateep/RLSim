
import myUtil as util

# read in maze file and store in dictionary
def initMaze(arg):
	infile = open("./Layouts/" + arg + ".lay", "r")
	lst = infile.read().splitlines()

	start = 0
	terminal = []
	dictionary = {}
	x, y, = 0, 0

	for line in lst[::-1]:
		for char in line:
			if char.isdigit():
				dictionary[(x, y)] = int(char)*10
			elif char != '%':
				dictionary[(x, y)] = 0
			else:
				dictionary[(x, y)] = char
			if char.isdigit(): terminal.append((x, y))

			dirSymbols = ['^', '>', 'v' '<']
			if str(char) in dirSymbols:
				directions = ['N', 'E', 'S', 'W']
				start = ((x, y), directions[dirSymbols.index(str(char))])
			x += 1
		x = 0
		y += 1

#	dictionary['exit'] = 0
	infile.close()
	return (dictionary, start, terminal)

class Maze:
	"""arg in order: maze, start, termianl"""
	def __init__(self, arg):
		self.maze, self.start, self.terminal = initMaze(arg)
		# self.maze = arg[0]
		# self.start = arg[1]
		# self.terminal = arg[2]

	def getLegalStates(self):
		return [state for state in self.maze.keys() if self.maze[state] != '%']
		
	def getLegalMoves(self, position, orientation):
		"""
		returns list of possible moves
		list in order: N, E, W, S
		"""
		# if position in self.terminal:
		# 	return ['exit']

		directions = []
		x, y = position[0], position[1]

		if self.maze[(x, y + 1)] is not '%': directions.append('N')
		if self.maze[(x + 1, y)] is not '%': directions.append('E')
		if self.maze[(x - 1, y)] is not '%': directions.append('W')
		if self.maze[(x, y - 1)] is not '%': directions.append('S')

		return util.directionToActionLst(orientation, directions)

	def getValue(self, position):
		if (position == "exit"): return 0
		return self.maze[position]

	def updateMaze(self, position, value):
		self.maze[position] = value

	def isTerminal(self, position):
		if position in self.terminal: 
			return True
		return False
