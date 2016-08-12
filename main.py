
import sys, getopt
import mazeFunctions
import reinforcementAlgo
import MDP
import myUtil as util
import os.path
import collections
import argparse

tri  = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 89, 97, 100, 103, 106]
trap = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 91, 97, 103, 106]

def build_agent(agent, maze, MDP, alpha, gamma, epsilon, learning, action_cost):
    if agent.lower() == 'qlearning':
        return reinforcementAlgo.QLearningAgent(maze, MDP, alpha, gamma, epsilon, action_cost, learning)
    elif 'sarsa' in agent.lower():
        return reinforcementAlgo.SarsaAgent(maze, MDP, alpha, gamma, epsilon, action_cost, learning)
    else:
        raise argparse.ArgumentError("algo must be either 'qlearning' or 'sarsa'")

def build_maze(maze, reward, reset, deadend):
    if not os.path.exists("./Layouts/" + maze + ".lay"):
        util.cmdline_error(0)
    else:
        return mazeFunctions.Maze(maze, reward, reset, deadend)

def build_MDP(mdpIn):
    if not os.path.exists("./MDP/" + mdpIn + ".mdp"):
        util.cmdline_error(1)
    else:
        return MDP.MDP(mdpIn)

def play_maze(agent):
    path = []
    agent.resetAgentState()
    while not agent.finishedMaze():
        pos, ori = agent.position, agent.orientation
        move = agent.getMove()
        path.append((pos[0], pos[1], util.actionToDirection(ori, move)))
    return path

def main(argv):
#     mazeIn, mdpIn, agentIn = '', 'deterministic', ''

#     # default agent parameters
#     alpha, gamma, epsilon, learning = 0.5, 0.8, 0, 1

#     # default environment parameters
#     back_cost, maze_reward, maze_reset, deadend_penalty = 10, 10, 0, 0

#     # default misc. simulator parameters
#     Qreset, output = '', None
#     num_samples, num_trials = 30, 114

#     try:
#         opts, args = getopt.getopt(sys.argv[1:], "hm:A:n:a:g:e:r:b:d:", ["maze=", "agent=", "MDP=", \
#                                                     "learning=", \
#                                                     "back_cost=", "reward=", "reset=", "deadend=", \
#                                                     "Qreset=", "output=", "samples=", "trials="])
#     except getopt.GetoptError:
#         help()

#     for opt, arg in opts:
#         if opt == '-h':
#             help()

#         elif opt in ('-m', '--maze'):
#             mazeIn = arg
#         elif opt in ('-A', '--agent'):
#             agentIn = arg.lower()
#         elif opt == '--MDP':
#             mdpIn = arg.lower()

#         elif opt in ('-a'):
#             alpha = float(arg)
#         elif opt in ('-g'):
#             gamma = float(arg)
#         elif opt in ('-e'):
#             epsilon = float(arg)
#         elif opt in ('--learning'):
#             learning = int(arg)

#         elif opt in ('--back_cost', '-b'):
#             back_cost = float(arg)
#         elif opt in ('--reward', '-r'):
#             maze_reward = float(arg)
#         elif opt in ('--reset'):
#             maze_reset = float(arg)
#         elif opt in ('--deadend', '-d'): # as a positive number
#             deadend_penalty = float(arg)

#         elif opt in ('--Qreset'):
#             Qreset = str(arg)
#         elif opt in ('--output'):
#             output = arg
#         elif opt in ('--samples'):
#             num_samples = int(arg)
#         elif opt in ('-n', '--trials'):

    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", help="name of reinforcement algorithm", required=True)
    parser.add_argument("--maze", help="layout file without extension", required=True)
    parser.add_argument("--mdp", help="transition file without extension", default="deterministic", type=str)
    parser.add_argument("-a", "--alpha", help="value of learning rate",default=0.5, type=float)
    parser.add_argument("-g", "--gamma", help="value of discount", default=0.8, type=float)
    parser.add_argument("-e", "--epsilon", help="probability of random action", default=0, type=float)
    parser.add_argument("-l", "--learning", help="agent's update function", default=1, type=int)
    parser.add_argument("-b", "--back_cost", help="difficulty of backward action", default=10, type=float)
    parser.add_argument("-R", "--reward", help="value of reward", default=10, type=float)
    parser.add_argument("-r", "--reset", help="probability of resetting reward", default=0, type=float)
    parser.add_argument("-d", "--deadend_cost", help="penalty at a deadend", default=0, type=float)
    parser.add_argument("-q", "--Qreset", help="interval in which qvalues or reset", default="", type=str)
    parser.add_argument("-s", "--samples", help="number of samples", default=30, type=int)
    parser.add_argument("-t", "--trials", help="number of trials", default=114, type=int)
    parser.add_argument("-o", "--output", help="path to output file with extension", default=None)
    args = parser.parse_args(argv)

    # Build Maze
    print(args)
    Maze = build_maze(args.maze, args.reward, args.reset, args.deadend_cost)

    # Build MDP
    MDP = build_MDP(args.mdp)

    # Build Agent
    Agent = build_agent(args.algo, Maze, MDP, args.alpha, args.gamma, args.epsilon, \
                        args.learning, action_cost={'F':1, 'R':1, 'B':args.back_cost, 'L':1})

    # Determine reset points
    reset_pts = []
    if args.Qreset == 'tri': reset_pts = tri
    elif args.Qreset == 'trap': reset_pts = trap
    elif args.Qreset.isdigit(): reset_pts = range(0, args.trials-1, int(args.Qreset))

    # Run agent through maze for n trials
    for s in range(args.samples):
        Agent.resetQValues()
        paths = []
        for i in range(args.trials):
            if i in reset_pts:
                print(i)
                Agent.resetQValues()
            paths.append(play_maze(Agent))

        if args.output is not None:
            util.path_csv(s, args.trials, paths, args.output)
    """
    # print output
    agent.posCounter.normalize()
    posDist = collections.OrderedDict(sorted(agent.posCounter.items()))

    # for printing position distributions -- not currently used

    # print to console
    if (consoleOut):
        util.print_path_data_to_file(posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon)

    # print to file
    if (fileOut):
        util.printPathToFile(paths, posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon)
        util.print_posdist_to_file(output, posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon)
    """
    # sys.exit()

if __name__ == "__main__":
    main(sys.argv[1:])
