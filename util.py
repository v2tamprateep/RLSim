import sys
import random
import datetime, time
import pandas as pd

"""
Help Message/Error Catching
"""
def help():
    print("-h           help")
    print("-m --maze    select maze")
    print("-A --agent   select agent, default: QLearning")
    print("-n --trials  select number of trials, default 1")
    print("--MDP        select MDP, default: deterministic\n")
    print("-a       alpha, learning rate, default: 0.5")
    print("-g       gamma, discount factor, default: 0.8")
    print("-e       epsilon, default: 0")
    sys.exit(0)


def cmdline_error(arg):
    if arg == 0:
        print("Unsupported maze")
    elif arg == 1:
        print("Unsupported MDP")
    elif arg == 2:
        print("Unsupported Reinforcement Learning Algorithm")
    else:
        print("I don't even know what you did wrong. RIP.")
    sys.exit(2)


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

"""
Functions
"""
def isfloat(value):
    """
    If value is a real number, return that number
    else return False
    """
    try:
        return float(value)
    except ValueError:
        return -1


def rand_bool(p):
    r = random.random()
    return r < p


def rand_choice(lst):
    return random.choice(lst)


"""
Direction: North, East, West, South
Action: Forwards, Left, Right, Backwards
"""
cardinalDir = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
actionLst = ['F', 'FR', 'R', 'BR', 'B', 'BL', 'L', 'FL']
opposite = {'N':'S', 'S':'N', 'W':'E', 'E':'W'}

def oppositeAction(action):
    opAct = ''
    for a in action:
        opAct += opposite[a]
    return opAct


def is_forwards(orientation, action):
    index = cardinalDir.index(orientation)
    return action in [cardinalDir[(index + i)%8] for i in range(-2, 3)]