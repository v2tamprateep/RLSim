
import getopt, sys
import operator

class Counter(dict):
	def __missing__(self, key):
		return 0

def getParams(path, fileIn):
	fileIn = open(path + fileIn)

	# skip first two lines in file
	fileIn.readline()
	fileIn.readline()

	words = fileIn.readline().split()
	params = (float(words[1]), float(words[3]), float(words[5]))
	fileIn.close()
	return params

longSum = False

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["file=", "long"])
except getopt.GetoptError:
	print("Commandline error")
	sys.exit(2)

fileIn = None

for opt, arg in opts:
	if (opt in ("--file=")):
		fileIn = arg
	elif (opt in ("--long")):
		longSum = True

if (fileIn is None):
	print("Commandline error")
	sys.exit(2)

dataFile = open(fileIn)
filename = fileIn.split("/")[-1]
pathToData = dataFile.readline().split()[3]

# Counter for summarized data
summary = Counter()
summaryAG = Counter()
summaryEA = Counter()
summaryGE = Counter()
count = Counter()
# skip blank line
dataFile.readline()
for line in dataFile:
	words = line.split()
	params = getParams(pathToData, words[0])
	value = float(words[1])

	summary[('alpha', params[0])] += value
	count[('alpha', params[0])] += 1

	summary[('gamma', params[1])] += value
	count[('gamma', params[1])] += 1
	
	summary[('epsilon', params[2])] += value
	count[('epsilon', params[2])] += 1

	if (longSum):
		summaryAG[('alpha', params[0], 'gamma', params[1])] += value
		count[('alpha', params[0], 'gamma', params[1])] += 1

		summaryEA[('epsilon', params[2], 'alpha', params[0])] += value
		count[('epsilon', params[2], 'alpha', params[0])] += 1

		summaryGE[('gamma', params[1], 'epsilon', params[2])] += value
		count[('gamma', params[1], 'epsilon', params[2])] += 1

ordered = sorted(summary.keys(), key=operator.itemgetter(0, 1))
if (longSum):
	orderedAG = sorted(summaryAG.items(), key=operator.itemgetter(1))
	orderedEA = sorted(summaryEA.items(), key=operator.itemgetter(1))
	orderedGE = sorted(summaryGE.items(), key=operator.itemgetter(1))

output = open(fileIn + "_Summary", "w")
output.write("Summary of " + filename)
output.flush

current = None
for param, value in ordered:
	if (param != current):
		current = param
		output.write("\n--" + str(current) + "--\n")

	output.write(current[0] + str(value) + ": " + str(summary[(param, value)]/count[(param, value)]) + "\n")

output.flush()

if (longSum):
	output.write("\n--alpha, gamma--\n")
	for key, value in orderedAG:
		param0, value0, param1, value1 = key
		output.write(param0[0] + str(value0) + "-" + param1[0] + str(value1) + ": " + str(value/count[key]) + "\n")

	output.flush()

	output.write("\n--epsilon, alpha--\n")
	for key, value in orderedEA:
		param0, value0, param1, value1 = key
		output.write(param0[0] + str(value0) + "-" + param1[0] + str(value1) + ": " + str(value/count[key]) + "\n")

	output.flush()

	output.write("\n--gamma, epsilon--\n")
	for key, value in orderedGE:
		param0, value0, param1, value1 = key
		output.write(param0[0] + str(value0) + "-" + param1[0] + str(value1) + ": " + str(value/count[key]) + "\n")

	output.flush()

output.close()
print("Script Complete")
