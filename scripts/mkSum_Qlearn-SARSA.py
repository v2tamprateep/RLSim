
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

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["file="])
except getopt.GetoptError:
	print("Commandline error")
	sys.exit(2)

fileIn = None

for opt, arg in opts:
	if (opt in ("--file=")):
		fileIn = arg

if (fileIn is None):
	print("Commandline error")
	sys.exit(2)

dataFile = open(fileIn)
filename = fileIn.split("/")[-1]
pathToData = dataFile.readline().split()[3]

# Counter for summarized data
summary = Counter()
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

ordered = sorted(summary.keys(), key=operator.itemgetter(0, 1))

output = open(fileIn + "_summary", "a")
output.write("Summary of " + filename)
output.flush

current = None
# index, perLine = 0, 5
for param, value in ordered:
	if (param != current):
		current = param
		output.write("\n--" + str(current) + "--\n")

	output.write(current[0] + str(value) + ": " + str(summary[(param, value)]/count[(param, value)]) + "\n")

output.flush()
output.close()
print("Script Complete")
