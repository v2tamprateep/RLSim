import sys
import argparse
import os.path
import collections
import ScriptUtil as su
import pandas as pd


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--algo", help="name of reinforcement algorithm", required=True)
    parser.add_argument("--mdp", help="transition file without extension", default="deterministic", type=str)
    parser.add_argument("-a", "--alpha", help="value of learning rate",default=0.5, type=float)
    parser.add_argument("-g", "--gamma", help="value of discount", default=0.8, type=float)
    parser.add_argument("-e", "--epsilon", help="probability of random action", default=0, type=float)
    parser.add_argument("-l", "--learning", help="agent's update function", default=1, type=int)
    parser.add_argument("-b", "--back_cost", help="difficulty of backward action", default=10, type=float)
    parser.add_argument("-R", "--reward", help="value of reward", default=10, type=float)
    parser.add_argument("-r", "--reset", help="probability of resetting reward", default=0, type=float)
    parser.add_argument("-d", "--deadend_cost", help="penalty at a deadend", default=0, type=float)
    parser.add_argument("--input", help="file of input actions", required=True, type=str)
    parser.add_argument("-o", "--output", help="path to output file with extension", default=None)
    args = parser.parse_args(argv)

    # Build MDP, Agent objects
    MDP = su.build_MDP(args.mdp)
    Agent = su.build_agent(args.algo, args.alpha, args.gamma, args.epsilon, args.learning,\
                        action_cost={'N':1, 'E':1, 'S':args.back_cost, 'W':1})

    input_file = pd.read_csv(args.input)
    paths = input_file["paths"]
    probabilities = list()

    # loop through episodes/paths
    for path in paths:
        probabilities.append(su.tether(path, Agent))

    # write to .csv file
    if args.output is not None:
        num_trials = len(probabilties)
        data = {"trial": range(num_trials), "probability": probabilities}
        df = pd.DataFrame(data)
        df.set_index("trials", inplace=True)
        df.to_csv(output)


if __name__ == "__main__":
    main(sys.argv[1:])
