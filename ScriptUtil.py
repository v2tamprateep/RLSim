import Maze
import Agents
import MDP
import string
import datetime, time
import pandas as pd
import sys, os


"""
Global Variables
"""
# Reset points from research Data (Fall 2015)
#   tri = triangular choice point discretation
#   trap = trapezoid choice point discretation

tri  = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 89, 97, 100, 103, 106]
trap = [0, 7, 28, 39, 49, 57, 64, 71, 74, 78, 82, 91, 97, 103, 106]


"""
Object Creation
"""
def build_agent(agent, alpha, gamma, epsilon, learning, action_cost, maze=None):
    """
    return agent object
    """
    agent = agent.lower()

    if "greedy" in agent:
        if "qlearning" in agent:
            return Agents.GreedyQLAgent(maze, alpha, gamma, epsilon, action_cost, learning)
        else:
            return Agents.GreedySarsaAgent(maze, alpha, gamma, epsilon, action_cost, learning)
    elif "soft" in agent:
        if "qlearning" in agent:
            return Agents.SoftQLAgent(maze, alpha, gamma, epsilon, action_cost, learning)
        else:
            return Agents.SoftSarsaAgent(maze, alpha, gamma, epsilon, action_cost, learning)
    else:
        print("Unsupported Agent")
        sys.exit()


def build_maze(maze, MDP, reward, reset, deadend):
    """
    return maze object
    """
    if not os.path.exists("./Layouts/" + maze + ".lay"):
        print("Unsupported Maze")
        sys.exit()
    else:
        return Maze.Maze(maze, MDP, reward, reset, deadend)


def build_MDP(mdpIn):
    """
    return MDP object
    """
    if not os.path.exists("./TransFuncs/" + mdpIn + ".mdp"):
        print("Unsupported MDP")
        sys.exit()
    else:
        return MDP.MDP(mdpIn)


"""
Functions
"""
def play_maze(agent):
    """
    simulate one episode through the maze
    return path taken through maze
    """
    path = []
    agent.reset_agent()
    while not agent.finished_maze():
        pos = agent.position
        action = agent.get_action()
        agent.take_action(action)
        path.append((pos[0], pos[1], action))
    return path


def tether(actions, follower):
    """
    simulate one episode through the maze, taking the actions given
    actions: list of actions in one episode
    """
    # print(actions)
    state_actions = string_to_list(actions)
    print(state_actions)
    probabilities = list()

    for state, action in state_actions:
        probabilities.append(follower.get_probability(action))
        follower.take_action(action)

    # return average probability of taking actions in episode
    return sum(probabilities)/len(probabilities)


def string_to_list(s):
    """
    Convert string of form:
        [(x_1, y_1, 'a_1'), (x_2, y_2, 'a_2'), ..., (x_n, y_n, 'a_n')]
    into a list of state-action pairs:
        [((x, y), a), ...]
    """
    # remove punctuation
    table = string.maketrans("","")
    s = s.translate(table, string.punctuation)
    
    # group into action-lst
    state_action_lst = []
    lst = s.split()
    i = 0
    while i < len(lst):
        state = (int(lst[i]), int(lst[i + 1]))
        action = lst[i + 2]
        state_action_lst.append((state, action))
        i += 3

    return state_action_lst


"""
Input
"""
def read_config(config):
    f = open(config)
    mazes, episodes = list(), list()

    for line in f:
        # formatted "maze: num_episodes"
        content = line.split(": ")
        mazes.append(content[0])
        episodes.append(int(content[1]))

    return mazes, episodes


"""
Output
"""
def path_csv(sample, trials, paths, output):
    data = {"trials": range(sum(trials)), "paths": paths}
    df = pd.DataFrame(data)
    df.set_index("trials", inplace = True)
    if output.endswith('/'):
        df.to_csv(output + 'sample' + str(sample) + '.csv')
    else:
        if ".csv" not in output: output += ".csv"
        df.to_csv(output)


def print_path_data_to_file(output, sample, paths, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon):
    dataFile = open(output+'sample' + str(sample), 'w')
    dataFile.write(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S') + "\n")
    dataFile.write("Agent:" + str(agentIn) + "\t\tMaze: "+ str(mazeIn) + "\t\tTrans. Function: " + str(mdpIn) + "\t\tTrials: " + str(trials) + "\n")
    dataFile.write("alpha: " + str(alpha) + "\t\tgamma: " + str(gamma) + "\t\tepsilon: " + str(epsilon) + "\n\n")

    for i in range(trials):
        dataFile.write("Trial: {0}\n".format(i))
        dataFile.write(str(paths[i]) + "\n\n")
    dataFile.close()


def print_posdist_to_file(output, posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon):
    dataFile = open(output, 'w')
    dataFile.write(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S') + "\n")
    dataFile.write("Agent:" + str(agentIn) + "\t\tMaze: "+ str(mazeIn) + "\t\tTrans. Function: " + str(mdpIn) + "\t\tTrials: " + str(trials) + "\n")
    dataFile.write("alpha: " + str(alpha) + "\t\tgamma: " + str(gamma) + "\t\tepsilon: " + str(epsilon) + "\n")
    dataFile.write("Distribution:\n")
    keys = posDist.keys()
    index, perLine = 0, 4
    for key in keys:
        dataFile.write(str(key).replace(" ", "") + ": {0:.15f}".format(posDist[key])),
        if index%perLine == (perLine - 1): dataFile.write("\n")
        else: dataFile.write("\t")
        index += 1
    dataFile.write("\n")
    dataFile.close()


def print_posdist_to_console(posDist, agentIn, mazeIn, mdpIn, trials, alpha, gamma, epsilon):
    print(datetime.datetime.fromtimestamp(time.time()).strftime('%d-%m-%Y %H:%M:%S'))
    print("Agent:" + str(agentIn) + "\t\tMaze: "+ str(mazeIn) + "\t\tTrans. Function: " + str(mdpIn) + "\t\tTrials: " + str(trials))
    print("alpha: " + str(alpha) + "\t\tgamma: " + str(gamma) + "\t\tepsilon: " + str(epsilon))
    print("Distribution:")
    keys = posDist.keys()
    index, perLine = 0, 4
    for key in keys:
        print(str(key) + ": {0:.15f}".format(posDist[key])),
        if index%perLine == (perLine - 1): print("\n")
        index += 1
