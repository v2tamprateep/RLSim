import sys
import argparse
import Maze
import Agents
import MDP
import util
import os.path
import collections


# from research data
tri  = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 89, 97, 100, 103, 106]
trap = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 91, 97, 103, 106]


def build_agent(agent, alpha, gamma, epsilon, learning, action_cost, maze=None):
    if agent.lower() == 'qlearning':
        return Agents.QLearningAgent(maze, alpha, gamma, epsilon, action_cost, learning)
    elif 'sarsa' in agent.lower():
        return Agents.SarsaAgent(maze, alpha, gamma, epsilon, action_cost, learning)
    else:
        util.cmdline_error(2)


def build_maze(maze, MDP, reward, reset, deadend):
    if not os.path.exists("./Layouts/" + maze + ".lay"):
        print("./Layouts/" + maze + ".lay")
        util.cmdline_error(0)
    else:
        return Maze.Maze(maze, MDP, reward, reset, deadend)


def build_MDP(mdpIn):
    if not os.path.exists("./TransFuncs/" + mdpIn + ".mdp"):
        util.cmdline_error(1)
    else:
        return MDP.MDP(mdpIn)


def play_maze(agent):
    path = []
    agent.reset_agent_state()
    while not agent.finished_maze():
        pos = agent.position
        action = agent.get_action()
        agent.take_action(action)
        path.append((pos[0], pos[1], action))
    return path


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", help="name of reinforcement algorithm", required=True)
    parser.add_argument("--mazes", help="name of maze (layout file without extension)", nargs="*", required=True)
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
    Agent = build_agent(args.algo, args.alpha, args.gamma, args.epsilon, args.learning,\
                        action_cost={'N':1, 'E':1, 'S':args.back_cost, 'W':1})

    # Determine reset points (episodes where the Q-values are reset)
    reset_pts = []
    if args.Qreset == 'tri': reset_pts = tri
    elif args.Qreset == 'trap': reset_pts = trap
    elif args.Qreset.isdigit(): reset_pts = range(0, args.trials - 1, int(args.Qreset))

    # Run agent through maze for s samples of n trials
    current_trial = 0
    for s in range(args.samples):
        paths = []

        for maze, trials in zip(args.mazes, args.trials):
            Maze = build_maze(maze, MDP, args.reward, args.reset, args.deadend_cost)
            Agent.change_maze(Maze)

            for i in range(trials):
                if i in reset_pts:
                    Agent.reset_Qvalues()
                paths.append(play_maze(Agent))
                current_trial += 1

        if args.output is not None:
            util.path_csv(s, args.trials, paths, args.output)

        # reset learning for each sample
        Agent.reset_Qvalues()

if __name__ == "__main__":
    main(sys.argv[1:])
