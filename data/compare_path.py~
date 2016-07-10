#!/user/bin/python
import os
import getopt, sys
from alignment.alignment import *
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# read in paths and store as list
def read_data(lines):
    lst = []
    for line in lines:
        lst.append(line[2:-2].split("), ("))
    return lst

try:
    opts, args = getopt.getopt(sys.argv[1:], "haegrb", ["control=", "data=", "output=", "start=", "trials=", "samples="])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

control = "mouse_hexShort.csv"
dataDir = None
output = None
start, num_trials, samples = 0, 114, 30
variables = ['needle']

for opt, arg in opts:
    if (opt == "--control"):
        control = str(arg)
    if (opt == "--data"):
        dataDir = str(arg)
    if (opt == "--output"):
        output = str(arg)
    if (opt == "--start"):
        start = int(arg)
    if (opt == "--trials"):
        num_trials = int(arg)
    if (opt == "--samples"):
        samples = int(arg)
    if (opt == "-a"):
        variables.append("alpha")
    if (opt == "-e"):
        variables.append("epsilon")
    if (opt == "-g"):
        variables.append("gamma")
    if (opt == "-r"):
        variables.append("reward")
    if (opt == "-b"):
        variables.append("back")

folder = dataDir.split('/')[-1]

control_df = pd.read_csv(control, index_col='trials')
control_df['paths'] = read_data(control_df['paths'])

complete_summary = {key:[] for key in variables}
for dir in os.listdir(dataDir):
    dir_split = dir.split('-')
    a, e, g, r, b = 0, 0, 0, 0, 0
    # extract parameters and normalize
    for split in dir_split:
        if split[0] == 'a': complete_summary['alpha'].append(float(split[1:])/10)
        elif split[0] == 'e': complete_summary['epsilon'].append(float(split[1:])/10)
        elif split[0] == 'r': complete_summary['reward'].append(float(split[1:]))
        elif split[0] == 'b': complete_summary['back'].append(float(split[1:]))

    sample_score = {}
    for sample in range(samples):
        currentfolder = dataDir + dir + '/'
        data_df = pd.read_csv(currentfolder + 'sample' + str(sample) + '.csv', index_col='trials')
        data_df['paths'] = read_data(data_df['paths'])
        sample_score[sample] = {}
        for i in range(num_trials):
            index = start + i
            # comparing subsequence of control to initial traces of data
            sample_score[sample][i] = needle(control_df['paths'][index], data_df['paths'][i])

    scores = []
    for trial in range(num_trials):
        total = 0
        for sample in range(samples):
            total += sample_score[sample][trial]
        scores.append(total/samples)
    # complete_summary[dir] = sum(scores)/114
    complete_summary['needle'].append(sum(scores)/num_trials)

overall_summary_df = pd.DataFrame(complete_summary)
overall_summary_df.set_index(variables[1:], inplace = True)
overall_summary_df.to_csv(output)

print("Script Complete")
