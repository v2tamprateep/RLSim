
import mazeFunctions
import reinforcementAlgo

def playMaze(agent, maze):
	path = []

	while not agent.finishedMaze():
		#print(agent.position)
		move = agent.getMove(agent.position)
		path.append(move)
		#print(agent.position)

	agent.resetPosition(maze.start)
	return path
