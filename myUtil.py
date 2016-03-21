# util.py
# -------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


import sys
import inspect
import heapq, random
import cStringIO
import datetime, time
import pandas as pd
import random

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
    data = {"trials": range(trials), "paths": paths}
    df = pd.DataFrame(data)
    df.set_index("trials", inplace = True)
    df.to_csv(output + 'sample' + str(sample) + '.csv')

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
class Counter(dict):
    def __getitem__(self, idx):
        self.setdefault(idx, 0)
        return dict.__getitem__(self, idx)

    def incrementAll(self, keys, count):
        """
        Increments all elements of keys by the same count.
        """
        for key in keys:
            self[key] += count

    def argMax(self):
        """
        Returns the key with the highest value.
        """
        if len(self.keys()) == 0: return None
        all = self.items()
        values = [x[1] for x in all]
        maxIndex = values.index(max(values))
        return all[maxIndex][0]

    def sortedKeys(self):
        """
        Returns a list of keys sorted by their values.  Keys
        with the highest values will appear first.
        """
        sortedItems = self.items()
        compare = lambda x, y:  sign(y[1] - x[1])
        sortedItems.sort(cmp=compare)
        return [x[0] for x in sortedItems]

    def totalCount(self):
        """
        Returns the sum of counts for all keys.
        """
        return sum(self.values())

    def normalize(self):
        """
        Edits the counter such that the total count of all
        keys sums to 1.  The ratio of counts for all keys
        will remain the same. Note that normalizing an empty
        Counter will result in an error.
        """
        total = float(self.totalCount())
        if total == 0: return self
        for key in self.keys():
            self[key] = self[key] / total

    def divideAll(self, divisor):
        """
        Divides all counts by divisor
        """
        divisor = float(divisor)
        for key in self:
            self[key] /= divisor

    def copy(self):
        """
        Returns a copy of the counter
        """
        return Counter(dict.copy(self))

    def reset(self):
        for key in self:
            self[key] = 0

    def __mul__(self, y ):
        """
        Multiplying two counters gives the dot product of their vectors where
        each unique label is a vector element.
        """
        sum = 0
        x = self
        if len(x) > len(y):
            x,y = y,x
        for key in x:
            if key not in y:
                continue
            sum += x[key] * y[key]
        return sum

    def __radd__(self, y):
        """
        Adding another counter to a counter increments the current counter
        by the values stored in the second counter.
        """
        for key, value in y.items():
            self[key] += value

    def __add__( self, y ):
        """
        Adding two counters gives a counter with the union of all keys and
        counts of the second added to counts of the first.
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] + y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = y[key]
        return addend

    def __sub__( self, y ):
        """
        Subtracting a counter from another gives a counter with the union of all keys and
        counts of the second subtracted from counts of the first.
        """
        addend = Counter()
        for key in self:
            if key in y:
                addend[key] = self[key] - y[key]
            else:
                addend[key] = self[key]
        for key in y:
            if key in self:
                continue
            addend[key] = -1 * y[key]
        return addend

def isfloat(value):
    """ 
    If value is a real number, return that number
    else return False
    """
    try:
        return float(value)
    except ValueError:
        return -1

def normalize(vectorOrCounter):
    """
    normalize a vector or counter by dividing each value by the sum of all values
    """
    normalizedCounter = Counter()
    if type(vectorOrCounter) == type(normalizedCounter):
        counter = vectorOrCounter
        total = float(counter.totalCount())
        if total == 0: return counter
        for key in counter.keys():
            value = counter[key]
            normalizedCounter[key] = value / total
        return normalizedCounter
    else:
        vector = vectorOrCounter
        s = float(sum(vector))
        if s == 0: return vector
        return [el / s for el in vector]

def nSample(distribution, values, n):
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    rand = [random.random() for i in range(n)]
    rand.sort()
    samples = []
    samplePos, distPos, cdf = 0,0, distribution[0]
    while samplePos < n:
        if rand[samplePos] < cdf:
            samplePos += 1
            samples.append(values[distPos])
        else:
            distPos += 1
            cdf += distribution[distPos]
    return samples

def sample(distribution, values = None):
    if type(distribution) == Counter:
        items = sorted(distribution.items())
        distribution = [i[1] for i in items]
        values = [i[0] for i in items]
    if sum(distribution) != 1:
        distribution = normalize(distribution)
    choice = random.random()
    i, total= 0, distribution[0]
    while choice > total:
        i += 1
        total += distribution[i]
    return values[i]

def sampleFromCounter(ctr):
    items = sorted(ctr.items())
    return sample([v for k,v in items], [k for k,v in items])

def getProbability(value, distribution, values):
    """
      Gives the probability of a value under a discrete distribution
      defined by (distributions, values).
    """
    total = 0.0
    for prob, val in zip(distribution, values):
        if val == value:
            total += prob
    return total

def flipCoin( p ):
    r = random.random()
    return r < p

def randomMove(lst):
    return random.choice(lst)

def chooseFromDistribution( distribution ):
    "Takes either a counter or a list of (prob, key) pairs and samples"
    if type(distribution) == dict or type(distribution) == Counter:
        return sample(distribution)
    r = random.random()
    base = 0.0
    for prob, element in distribution:
        base += prob
        if r <= base: return element

def sign( x ):
    """
    Returns 1 or -1 depending on the sign of x
    """
    if( x >= 0 ):
        return 1
    else:
        return -1

def arrayInvert(array):
    """
    Inverts a matrix stored as a list of lists.
    """
    result = [[] for i in array]
    for outer in array:
        for inner in range(len(outer)):
            result[inner].append(outer[inner])
    return result

def matrixAsList( matrix, value = True ):
    """
    Turns a matrix into a list of coordinates matching the specified value
    """
    rows, cols = len( matrix ), len( matrix[0] )
    cells = []
    for row in range( rows ):
        for col in range( cols ):
            if matrix[row][col] == value:
                cells.append( ( row, col ) )
    return cells

# def lookup(name, namespace):
#     """
#     Get a method or class from any imported module from its name.
#     Usage: lookup(functionName, globals())
#     """
#     dots = name.count('.')
#     if dots > 0:
#         moduleName, objName = '.'.join(name.split('.')[:-1]), name.split('.')[-1]
#         module = __import__(moduleName)
#         return getattr(module, objName)
#     else:
#         modules = [obj for obj in namespace.values() if str(type(obj)) == "<type 'module'>"]
#         options = [getattr(module, name) for module in modules if name in dir(module)]
#         options += [obj[1] for obj in namespace.items() if obj[0] == name ]
#         if len(options) == 1: return options[0]
#         if len(options) > 1: raise Exception, 'Name conflict for %s'
#         raise Exception, '%s not found as a method or class' % name

"""
Direction: North, East, West, South
Action: Forwards, Left, Right, Backwards
"""
cardinalDir = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
actionLst = ['F', 'FR', 'R', 'BR', 'B', 'BL', 'L', 'FL']

def directionToAction(orientation, direction):
    oriIndex = cardinalDir.index(orientation)
    dirIndex = cardinalDir.index(direction)

    if (dirIndex < oriIndex): dirIndex += 8
    diff = dirIndex - oriIndex
    return actionLst[diff]
 
def actionToDirection(orientation, action):
    oriIndex = cardinalDir.index(orientation)
    actIndex = actionLst.index(action)

    return cardinalDir[(oriIndex + actIndex)%8]

def directionToActionLst(orientation, directions):
    lst = []
    for direction in directions:
        lst.append(directionToAction(orientation, direction))
    return lst

opposite = {'N':'S', 'S':'N', 'W':'E', 'E':'W', 'F':'B', 'B':'F', 'L':'R', 'R':'L'}
def oppositeAction(action):
    opAct = ''
    for a in action:
        opAct += opposite[a]
    return opAct
