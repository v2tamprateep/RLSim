
import sys, getopt
import mazeFunctions
import reinforcementAlgo
import MDP
import myUtil as util
import os.path
import collections

def buildAgent(agent, maze, MDP, alpha, gamma, epsilon, learning, action_cost):
	if agent.lower() == 'qlearning':
		return reinforcementAlgo.QLearningAgent(maze, MDP, alpha, gamma, epsilon, action_cost, learning)
	elif 'sarsa' in agent.lower():
		return reinforcementAlgo.SarsaAgent(maze, MDP, alpha, gamma, epsilon, action_cost, learning)
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
	mazeIn, mdpIn, agentIn = '', 'deterministic', ''

	# default agent parameters
	alpha, gamma, epsilon, learning = 0.5, 0.8, 0, 1

	# default environment parameters
	back_cost, maze_reward, maze_reset = 10, 10, 0

	# default misc. simulator parameters
	Qreset, output = None, None
	num_samples, num_trials = 30, 114

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:A:n:a:g:e:r:b:", ["maze=", "agent=", "trials=", "samples=", "MDP=", "output=", \
							"reset=", "reward=", "back_cost=", "learning=", "Qreset="])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:
		if opt == '-h':
			help()

		elif opt in ('-m', '--maze'):
			mazeIn = arg
		elif opt == '--MDP':
			mdpIn = arg.lower()
		elif opt in ('-A', '--agent'):
			agentIn = arg.lower()

		elif opt in ('-a'):
			alpha = float(arg)
		elif opt in ('-g'):
			gamma = float(arg)
		elif opt in ('-e'):
			epsilon = float(arg)
		elif opt in ('--learning'):
			learning = int(arg)

		elif opt in ('--back_cost', '-b'):
			back_cost = float(arg)
		elif opt in ('--reward', '-r'):
			maze_reward = float(arg)
		elif opt in ('--reset'):
			maze_reset = float(arg)

		elif opt in ('--Qreset'):
			Qreset = arg
		elif opt in ('--output'):
			output = arg
		elif opt in ('--samples'):
			num_samples = int(arg)
		elif opt in ('-n', '--trials'):
			num_trials = int(arg)

	# Build Maze
	if (not os.path.exists("./Layouts/" + mazeIn + ".lay")): util.cmdline_error(0)
	maze = mazeFunctions.Maze(mazeIn, maze_reward, maze_reset)

	# Build MDP
	mdp = buildMDP(maze, mdpIn)

	# Build Agent
	agent = buildAgent(agentIn, maze, mdp, alpha, gamma, epsilon, learning, action_cost={'F':1, 'R':1, 'B':back_cost, 'L':1})

	# find reset points
	reset_pts = []
	if Qreset is None:
		pass
	elif Qreset.isdigit():
		reset_pts = range(0, num_trials - 1, int(Qreset))
	else:
		for char in Qreset:
			if char.isdigit(): reset_pts.append(int(char))

	# Run agent through maze for n trials
	for s in range(num_samples):
		agent.resetQValues()
		paths = []
		for i in range(num_trials):
			if i in reset_pts: agent.resetQValues()
			paths.append(playMaze(agent, maze))

		if output is not None:
			util.path_csv(s, num_trials, paths, output)

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

if __name__ == "__main__":
    main(sys.argv[1:])
