
import mazeFunctions
import reinforcementAlgo
from myUtil import actionToDirection

def playMaze(agent, maze):
	path = []
	agent.resetAgentState()
	while not agent.finishedMaze():
		pos, ori = agent.position, agent.orientation
		move = agent.getMove()
		path.append((pos[0], pos[1], actionToDirection(ori, move)))
	return path
