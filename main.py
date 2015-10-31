
import sys, getopt
import mazeFunctions
import reinforcementAlgo
import MDP
import game
import util
import os.path

def help():
	print("-h			help")
	print("-m, --maze	select maze")
	print("-A, --agent	select agent, default: QLearning")
	print("-n, --trials	select number of trials, default 1")
	print("--MDP		select MDP, default: deterministic\n")
	print("-a 		alpha, learning rate, default: 0.5")
	print("-g 		gamma, discount factor, default: 0.8")
	sys.exit(0)

def error(arg):
	if arg == 0:
		print("Unsupported maze")
	elif arg == 1:
		print("Unsupported MDP")
	elif arg == 2: 
		print("Unsupported Rl Algorithm")
	else:
		print("I don't even know what you did wrong. RIP.")
	sys.exit(2)

def buildAgent(agent, maze, MDP, alpha, gamma):
	if agent == '':
		return reinforcementAlgo.QLearningAgent(maze, maze.start, maze.terminal, MDP, alpha, gamma)
	elif agent.lower() == 'qlearning':
		return reinforcementAlgo.QLearningAgent(maze, maze.start, maze.terminal, MDP, alpha, gamma)
	elif 'sarsa' in agent.lower():
		return reinforcementAlgo.SarsaAgent(maze, maze.start, maze.terminal, MDP, alpha, gamma)
	else:
		error(2)

def buildMDP(maze, mdpIn):
	if mdpIn == '':
		return MDP.MDP(maze, "deterministic")
	elif mdpIn == 'deterministic':
		return MDP.MDP(maze, "deterministic")
	elif not os.path.exists("./MDP/" + mdpIn + ".mdp"):
		error(1)
	else:
		return MDP.MDP(maze, MDP.initMDP(mdpIn))

def init(mazeIn, mdpIn, agentIn, alpha, gamma):
	if (not os.path.exists("./layouts/" + mazeIn + ".lay")): error(0)
	maze = mazeFunctions.Maze(mazeFunctions.parseMaze(mazeIn))

	if mdpIn == '':
		mdp = MDP.MDP(maze, "deterministic")
	else:
		mdp = MDP.MDP(maze, mdpIn)

def main(argv):
	mazeIn = ''
	mdpIn = ''
	agentIn = ''
	trials = 1
	alpha = 0.5
	gamma = 0.8

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:A:n:a:g:", ["maze=", "agent=", "trials=", "MDP="])
	except getopt.GetoptError:
		help()

	for opt, arg in opts:
		if opt == '-h':
			help()
		elif opt == '--MDP':
			mdpIn = arg
		elif opt in ('-m', '--maze'):
			mazeIn = arg
		elif opt in ('-A', '--agent'):
			agentIn = arg
		elif opt in ('-n', '--trials'):
			trials = int(arg)
		elif opt in ('-a'):
			alpha = float(arg)
		elif opt in ('-g'):
			gamma = float(arg)

	# Build Maze
	if (not os.path.exists("./layouts/" + mazeIn + ".lay")): error(0)
	maze = mazeFunctions.Maze(mazeFunctions.parseMaze(mazeIn))

	# Build MDP
	mdp = buildMDP(maze, mdpIn)

	# Build Agent
	agent = buildAgent(agentIn, maze, mdp, alpha, gamma)

	# Run agent through maze for n trials 
	for i in range(trials):
		path = game.playMaze(agent, maze)

	print("final path:")
	print(path)

	sys.exit()


maze = None
mdp = None
agent = None

if __name__ == "__main__":
    main(sys.argv[1:])








# """ Load Maze """
# maze = mazeFunctions.Maze(mazeFunctions.parseMaze(sys.argv[1]))


# """ Load MDP """
# """ 
# 	If sys.argv[4] is Null, agent is deterministic by default
# """
# if str(sys.argv[4]) == None: MDP = MDP.MDP(maze, "deterministic")
# else: MDP = MDP.MDP(maze, str(sys.argv[4]))


# """ Initialize RL Agent/Algorithm """
# Agent = None

# if str(sys.argv[2]) == 'QLearning':
# 	agent = reinforcementAlgo.QLearningAgent(maze, maze.start, maze.terminal, 0.5, 0.8)
# else:
# 	print("Chosen agent: ", sys.argv[2])
# 	sys.exit()


# """ Run agent through maze for n trials """	
# for i in range(int(sys.argv[3])):
# 	path = game.playMaze(agent, maze)


# print("final path:")
# print(path)

# sys.exit()
