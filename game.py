
import mazeFunctions
import reinforcementAlgo

def playMaze(agent, maze):
	path = []

	while not agent.finishedMaze():
		#print(agent.position)
		move = agent.getMove()
		path.append(move)

	agent.resetPosition(maze.start)
	return path
