import getopt, sys
import subprocess
import os
import operator

try:
	opts, args = getopt.getopt(sys.argv[1:], "", ["fileA=", "folderB=", "output="])
except getopt.GetoptError:
	print("Commandline error")
	sys.exit(2)

fileA = None
folderB = None
output = None

for opt, arg in opts:
	if (opt in ("--fileA=")):
		fileA = arg
	if (opt in ("--folderB=")):
		folderB = arg
	if (opt in ("--output=")):
		output = arg

if (fileA is None or folderB is None or output is None):
	print("One or more missing arguments")
	sys.exit(2)

output = open(output, "w")
output.write("Compare contents of " + folderB + " against " + fileA + ":\n\n")
output.flush

dic = {}
for path, dirs, files in os.walk(folderB):
	for name in sorted(files):
		out = subprocess.check_output(["python" ,"scripts/compare.py", "--fileA=" + fileA, "--fileB=" + os.path.join(path, name)])
		dic[name] = out

ordered = sorted(dic.items(), key=operator.itemgetter(1))

for tup in ordered:
	output.write(str(tup[0]) + " " + str(tup[1]))
	output.flush()

output.close()
print("Script Complete")
