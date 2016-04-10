
import sys, getopt
import mazeFunctions
import reinforcementAlgo
import game
import MDP
import myUtil as util
import os.path
import collections

def buildAgent(agent, maze, MDP, alpha, gamma, epsilon, action_cost):
	if agent.lower() == 'qlearning':
		return reinforcementAlgo.QLearningAgent(maze, MDP, alpha, gamma, epsilon, action_cost)
	elif 'sarsa' in agent.lower():
		return reinforcementAlgo.SarsaAgent(maze, MDP, alpha, gamma, epsilon, action_cost)
	else:
		util.cmdline_error(2)

def buildMDP(maze, mdpIn):
	if mdpIn == '':
		util.cmdline_error(1)
		return MDP.MDP(maze, "deterministic")
	elif mdpIn == 'deterministic':
		return MDP.MDP(maze, "deterministic")
	elif not os.path.exists("./MDP/" + mdpIn + ".mdp"):
		util.cmdline_error(1)
	else:
		return MDP.MDP(maze, MDP.initMDP(mdpIn))

def playMaze(agent, maze):
	path = []
	agent.resetAgentState()
	while not agent.finishedMaze():
		pos, ori = agent.position, agent.orientation
		move = agent.getMove()
		path.append((pos[0], pos[1], util.actionToDirection(ori, move)))
	return path

def main(argv):
	mazeIn = ''
	mdpIn = 'deterministic'
	agentIn = ''
	trials = 114
	sampleSize = 30
	alpha = 0.5
	gamma = 0.8
	epsilon = 0.1
	back_cost = 10
	maze_reset = 0
	maze_reward = 10
	output = ""
	consoleOut = True
	fileOut = True

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:A:n:a:g:e:r:b:", ["maze=", "agent=", "trials=", "samples=", "MDP=", "output=", \
							"consoleOut-Off", "fileOut-Off", "reset=", "reward=", "back_cost="])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:
		if opt == '-h':
			help()
		elif opt == '--MDP':
			mdpIn = arg.lower()
		elif opt in ('-m', '--maze'):
			mazeIn = arg
		elif opt in ('-A', '--agent'):
			agentIn = arg.lower()
		elif opt in ('-n', '--trials'):
			trials = int(arg)
		elif opt in ('--samples'):
			sampleSize = int(arg)
		elif opt in ('-a'):
			alpha = float(arg)
		elif opt in ('-g'):
			gamma = float(arg)
		elif opt in ('-e'):
			epsilon = float(arg)
		elif opt in ('--back_cost', '-b'):
			back_cost = float(arg)
		elif opt in ('--reward', '-r'):
			maze_reward = float(arg)
		elif opt in ('--reset'):
			maze_reset = float(arg)
		elif opt in ("--output"):
			output = arg
		elif opt in("--consoleOut-Off"):
			consoleOut = False
		elif opt in("--fileOut-Off"):
			fileOut = False


	# Build Maze
	if (not os.path.exists("./Layouts/" + mazeIn + ".lay")): util.cmdline_error(0)
	maze = mazeFunctions.Maze(mazeIn, maze_reward, maze_reset)

	# Build MDP
	mdp = buildMDP(maze, mdpIn)

	# Build Agent
	agent = buildAgent(agentIn, maze, mdp, alpha, gamma, epsilon, action_cost={'F':1, 'R':1, 'B':back_cost, 'L':1})

	# Run agent through maze for n trials
	for s in range(sampleSize):
		agent.resetQValues()
		paths = []
		for i in range(trials):
			paths.append(game.playMaze(agent, maze))
		util.path_csv(s, trials, paths, output)
		# util.print_path_data_to_file(output, s, paths, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon)

	# print output
	agent.posCounter.normalize()
	posDist = collections.OrderedDict(sorted(agent.posCounter.items()))

	# for printing position distributions -- not currently used
	"""
	# print to console
	if (consoleOut):
		util.print_path_data_to_file(posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon)

	# print to file
	if (fileOut):
		util.printPathToFile(paths, posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon)
		util.print_posdist_to_file(output, posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon)
	"""
	sys.exit()


#maze = None
#mdp = None
#agent = None

if __name__ == "__main__":
    main(sys.argv[1:])

