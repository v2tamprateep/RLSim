
import sys, getopt
import math

def loadData(fileIn):
	while (True):
		line = fileIn.readline()
		if ("Distribution" in line):
			break
	
	data = {}
	for line in fileIn:
		key = None
		for word in line.split():
			if "(" in word and ")" in word:
				key = word[:-1]
			else:
				data[key] = float(word)

	return data

def KLD(dist1, dist2):
	klSum = 0
	for key in dist1.keys():
		if (dist1[key] != 0):
			klSum += dist1[key] * math.log(dist1[key]/dist2[key])

	return klSum

# script

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["fileA=", "fileB="])
except getopt.GetoptError:
	print("Commandline error")
	print("python scripts/pythonCompare.py --fileA= --folderB= --output=")
	sys.exit(2)

fileNameA = None
fileNameB = None

for opt, arg in opts:
	if (opt in ("--fileA=")):
		fileNameA = arg
	if (opt in ("--fileB=")):
		fileNameB = arg

if (fileNameA is None or fileNameB is None):
	print("Error: One or more files are Null")
	sys.exit(2)

# fileA = open("Data/" + str(fileNameA))
# fileB = open("Data/" + str(fileNameB))
fileA = open(str(fileNameA))
fileB = open(str(fileNameB))

dataA = loadData(fileA)
dataB = loadData(fileB)

M = {}
for key in dataA.keys():
	M[key] = (dataA[key] + dataB[key])/2
JSD = KLD(dataA, M)/2 + KLD(dataB, M)/2

print(JSD)

