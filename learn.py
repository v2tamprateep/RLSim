import sys
import argparse
import os.path
import collections
import ScriptUtil as su


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", help="name of reinforcement algorithm", required=True)
    parser.add_argument("--mazes", help="maze config file", required=True)
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


    # get mazes and trials
    mazes, trials = su.read_config(args.mazes)

    # total trials
    total_trials = sum(trials)

    # Build MDP, Agent objects
    MDP = su.build_MDP(args.mdp)
    Agent = su.build_agent(args.algo, args.alpha, args.gamma, args.epsilon, args.learning,\
                        action_cost={'N':1, 'E':1, 'S':args.back_cost, 'W':1})

    # Determine reset points (episodes where the Q-values are reset)
    reset_pts = []
    if args.Qreset == 'tri':
        reset_pts = su.tri
    elif args.Qreset == 'trap':
        reset_pts = su.trap
    elif args.Qreset.isdigit():
        reset_pts = range(0, total_trials - 1, int(args.Qreset))


    # Run agent through maze for s samples of n trials
    for s in range(args.samples):
        paths = []

        for maze, trial in zip(mazes, trials):
            Maze = su.build_maze(maze, MDP, args.reward, args.reset, args.deadend_cost)
            Agent.change_maze(Maze)

            for i in range(trial):
                if i in reset_pts:
                    Agent.reset_Qvalues()
                paths.append(su.play_maze(Agent))

        if args.output is not None:
            su.path_csv(s, total_trials, paths, args.output)

        # reset learning for each sample
        Agent.reset_Qvalues()

    for path in paths:
        print(path)


if __name__ == "__main__":
    main(sys.argv[1:])
