
import mazeFunctions
import reinforcementAlgo

def playMaze(agent, maze):
	path = []
	agent.resetAgentState()
	while not agent.finishedMaze():
		move = agent.getMove()
		path.append(move)
	return path
