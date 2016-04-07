import subprocess
import getopt, sys
import os

def makeDir(path, var):
    name = "".join(var)
    name = name.replace(" ", "")
    name = name.replace(".", "")
    out = path + name.strip('-')
    try:
        os.mkdir(out)
    except:
        pass
    return out

agent, maze, output, trials, samples = None, None, None, None, None
prog_call = ["python", "main.py"]
intlist = [x for x in range(10)]
floatList = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]

try:
    opts, args = getopt.getopt(sys.argv[1:], "aegrb", ["agent=", "maze=", "output=", "trials=", "samples="])
except getopt.GetoptError as err:
    print(err)
    sys.exit(2)

for opt, arg in opts:
    if opt in ['--agent', '--maze', '--trials', '--samples']:
        prog_call += [opt + "=" + arg]
    elif opt in ['--output']:
        output = str(arg)
    # elif (opt == "-a"):
    #     variables.append("-a")
    # elif (opt == "-e"):
    #     variables.append("-e")
    # elif (opt == "-g"):
    #     variables.append("-g")
    # elif (opt == "-r"):
    #     variables.append("-r")
    # elif (opt == "-b"):
    #     variables.append("-b")

variables = []
for a in floatList:
    variables.append("-a " + str(a))
    for e in floatList:
        variables.append("-e " + str(e))
        out = makeDir(output, variables)
        subprocess.call(prog_call + [out] + variables)
        variables.pop()
    variables.pop()
print("Script Complete.")
