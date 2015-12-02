
import sys, getopt
import mazeFunctions
import reinforcementAlgo
import MDP
import game
import util
import os.path
import collections
import datetime, time


def printToFile(output, posDist, agentIn, mazeIn, mdpIn, trials):
	dataFile = open("./Data/" + output, 'w')
	dataFile.write(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S') + "\n")
	dataFile.write("Agent:" + str(agentIn) + "\t\tMaze: "+ str(mazeIn) + "\t\tTrans. Function: " + str(mdpIn) + "\t\tTrials: " + str(trials) + "\n")
	keys = posDist.keys()
	index, perLine = 0, 4
	for key in keys:
		dataFile.write(str(key) + ": {0:.15f}".format(posDist[key])),
		if index%perLine == (perLine - 1): dataFile.write("\n")
		else: dataFile.write("\t")
		index += 1
	dataFile.write("\n")
	dataFile.close()
	
def printToConsole(posDist, agentIn, mazeIn, mdpIn, trials):
	print(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
	print("Agent:" + str(agentIn) + "\t\tMaze: "+ str(mazeIn) + "\t\tTrans. Function: " + str(mdpIn) + "\t\tTrials: " + str(trials) + "\n")
	keys = posDist.keys()
	index, perLine = 0, 4
	for key in keys:
		print(str(key) + ": {0:.15f}".format(posDist[key])),
		if index%perLine == (perLine - 1): print("\n")
		index += 1

def help():
	print("-h			help")
	print("-m --maze	select maze")
	print("-A --agent	select agent, default: QLearning")
	print("-n --trials	select number of trials, default 1")
	print("--MDP		select MDP, default: deterministic\n")
	print("-a 		alpha, learning rate, default: 0.5")
	print("-g 		gamma, discount factor, default: 0.8")
	print("-e		epsilon, default: 0")
	sys.exit(0)

def error(arg):
	if arg == 0:
		print("Unsupported maze")
	elif arg == 1:
		print("Unsupported MDP")
	elif arg == 2: 
		print("Unsupported Reinforcement Learning Algorithm")
	else:
		print("I don't even know what you did wrong. RIP.")
	sys.exit(2)

def buildAgent(agent, maze, MDP, alpha, gamma, epsilon):
	if agent == '':
		error(2)
		return reinforcementAlgo.QLearningAgent(maze, maze.start, maze.terminal, MDP, alpha, gamma, epsilon)
	elif agent.lower() == 'qlearning':
		return reinforcementAlgo.QLearningAgent(maze, maze.start, maze.terminal, MDP, alpha, gamma, epsilon)
	elif 'sarsa' in agent.lower():
		return reinforcementAlgo.SarsaAgent(maze, maze.start, maze.terminal, MDP, alpha, gamma, epsilon)
	else:
		error(2)

def buildMDP(maze, mdpIn):
	if mdpIn == '':
		error(1)
		return MDP.MDP(maze, "deterministic")
	elif mdpIn == 'deterministic':
		return MDP.MDP(maze, "deterministic")
	elif not os.path.exists("./MDP/" + mdpIn + ".mdp"):
		error(1)
	else:
		return MDP.MDP(maze, MDP.initMDP(mdpIn))

def main(argv):
	mazeIn = ''
	mdpIn = 'deterministic'
	agentIn = ''
	trials = 1
	alpha = 0.5
	gamma = 0.8
	epsilon = 0
	output = "defaultOut.txt"

	try:
		opts, args = getopt.getopt(sys.argv[1:], "hm:A:n:a:g:e:", ["maze=", "agent=", "trials=", "MDP=", "output="])
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
		elif opt in ('-e'):
			epsilon = float(arg)
		elif opt in ("--output"):
			output = arg

	# Build Maze
	if (not os.path.exists("./Layouts/" + mazeIn + ".lay")): error(0)
	maze = mazeFunctions.Maze(mazeFunctions.parseMaze(mazeIn))

	# Build MDP
	mdp = buildMDP(maze, mdpIn)

	# Build Agent
	agent = buildAgent(agentIn, maze, mdp, alpha, gamma, epsilon)
	
	# Run agent through maze for n trials 
	for i in range(trials):
		path = game.playMaze(agent, maze)

	#print("final path:")
	#print(path)
	# print output
	agent.posCounter.normalize()
	posDist = collections.OrderedDict(sorted(agent.posCounter.items()))

	# print to console
	printToConsole(posDist, agentIn, mazeIn, mdpIn, trials)

	# print to file
	printToFile(output, posDist, agentIn, mazeIn, mdpIn, trials)
	
	sys.exit()


maze = None
mdp = None
agent = None

if __name__ == "__main__":
    main(sys.argv[1:])

