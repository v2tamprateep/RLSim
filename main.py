import sys
import argparse
import mazeFunctions
import reinforcementAlgo
import MDP
import myUtil as util
import os.path
import collections

"""
tri  = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 89, 97, 100, 103, 106]
trap = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 91, 97, 103, 106]
"""

def build_agent(agent, MDP, alpha, gamma, epsilon, learning, action_cost, maze=None):
    if agent.lower() == 'qlearning':
        return reinforcementAlgo.QLearningAgent(maze, MDP, alpha, gamma, epsilon, action_cost, learning)
    elif 'sarsa' in agent.lower():
        return reinforcementAlgo.SarsaAgent(maze, MDP, alpha, gamma, epsilon, action_cost, learning)
    else:
        util.cmdline_error(2)

def build_maze(maze, reward, reset, deadend):
    if not os.path.exists("./Layouts/" + maze + ".lay"):
        util.cmdline_error(0)
    else:
        return mazeFunctions.Maze(maze, reward, reset, deadend)

def build_MDP(mdpIn):
    if not os.path.exists("./TransFuncs/" + mdpIn + ".mdp"):
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
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", help="name of reinforcement algorithm", required=True)
    parser.add_argument("--mazes", help="path to layout file without extension", nargs="*", required=True)
    parser.add_argument("-t", "--trials", help="number of trials", nargs="*", type=int, required=True)
    parser.add_argument("-s", "--samples", help="number of samples", default=30, type=int)
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
    parser.add_argument("-o", "--output", help="path to output file with extension", default=None)
    args = parser.parse_args(argv)

    # Build MDP, Agent objects
    MDP = build_MDP(args.mdp)
    Agent = build_agent(args.algo, MDP, args.alpha, args.gamma, args.epsilon, args.learning,\
                        action_cost={'F':1, 'R':1, 'B':args.back_cost, 'L':1})

    """
    # Determine reset points
    reset_pts = []
    if args.Qreset == 'tri': reset_pts = tri
    elif args.Qreset == 'trap': reset_pts = trap
    elif args.Qreset.isdigit(): reset_pts = range(0, args.trials-1, int(args.Qreset))
    """

    # Run agent through maze for n trials
    current_trial = 0
    for s in range(args.samples):
        paths = []

        for maze, trials in zip(args.mazes, args.trials):
            Maze = build_maze(maze, args.reward, args.reset, args.deadend_cost)
            Agent.change_maze(Maze)

            for i in range(trials):
                if i in reset_pts:
                    Agent.resetQValues()
                paths.append(play_maze(Agent))
                current_trial += 1

        if args.output is not None:
            util.path_csv(s, args.trials, paths, args.output)

        Agent.resetQValues()

if __name__ == "__main__":
    main(sys.argv[1:])
