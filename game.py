
import mazeFunctions
import reinforcementAlgo

def playMaze(agent, maze):
	path = []

	while not agent.finishedMaze():
		move = agent.getMove(agent.position)
		path.append(move)
		agent.update(move)

	agent.resetPosition(maze.start)
	return path