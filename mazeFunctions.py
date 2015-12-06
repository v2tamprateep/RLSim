
# read in maze file and store in dictionary
def parseMaze(arg):
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
			#if char != '%':
				dictionary[(x, y)] = 0
			else:
				dictionary[(x, y)] = char
			if char.isdigit(): terminal.append((x, y))
			#if char.isdigit(): terminal[(x, y)] = int(char)
			if str(char).lower() == 's': 
				start = (x, y)
			x += 1
		x = 0
		y += 1

#	dictionary['exit'] = 0

	infile.close()
	return (dictionary, start, terminal)

class Maze:
	"""arg in order: maze, start, termianl"""
	def __init__(self, arg):
		self.maze = arg[0]
		self.start = arg[1]
		self.terminal = arg[2]
		
	# returns list of possible moves
	# list in order: N, E, W, S
	def getLegalMoves(self, position):
		if position in self.terminal:
			return ['exit']

		moves = []
		x = position[0]
		y = position[1]
		
		if self.maze[(x, y + 1)] is not '%': moves.append('N')
		if self.maze[(x + 1, y)] is not '%': moves.append('E')
		if self.maze[(x - 1, y)] is not '%': moves.append('W')
		if self.maze[(x, y - 1)] is not '%': moves.append('S')

		return moves

	def getValue(self, position):
		if (position == "exit"): return 0
		return self.maze[position]

	def updateMaze(self, position, value):
		self.maze[position] = value

	def isTerminal(position):
		if position in terminal: 
			return True
		return False
