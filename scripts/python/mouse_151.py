import argparse
import os, sys
import numpy as np
import subprocess
import zipfile

maze_arg = ["--mazes", "maze_set3/unbias", "maze_set3/unbias", \
            "maze_set3/antibiasL", "maze_set3/antibiasL", \
            "maze_set3/antibiasL", "maze_set3/unbias", "maze_set3/unbias"]

trial_arg = ["--trials", "137", "98", "60", "91", "81", "92", "106"]

parser = argparse.ArgumentParser()
parser.add_argument("-A", "--algo", required=True)
parser.add_argument("-M", "--mazes", nargs="+")
parser.add_argument("-t", "--trials", nargs="+")
parser.add_argument("-r", "--reset", default="")
cmd_args = parser.parse_args(sys.argv[1:])

func_call = ["python", "main.py"] + sys.argv[1:]

if "--maze" not in func_call: func_call += maze_arg
if "--trial" not in func_call: func_call += trial_arg

l_map = {1:"_std", 2:"_RD", 3:"_ER", 4:"_RDER"}

folder = None
for l in range(1, 5):
    func_call += ["-l", str(l)]
    folder = cmd_args.algo + l_map[l] + cmd_args.reset
    if not os.path.exists(folder):
        os.mkdir(folder)

    for a in np.arange(0.1, 1.1, 0.1):
        args_a = ["-a", str(a)]
        for e in np.arange(0, 1.0, 0.1):
            args_e = ["-e", str(e)]
            for R in range(1, 11, 1): # reward
                args_R = ["-R", str(R)]
                for b in range(1, 11, 1):
                    args_b = ["-b", str(b)]
                    args = args_a + args_e + args_R + args_b
                    directory = "".join(args)[1:].replace(".", "")
                    output = os.path.join(folder, directory) + "/"
                    if not os.path.exists(output):
                        os.mkdir(output)

                    func_call += ["--output", output] + args
                    subprocess.call(func_call)
    
    # hopefully this zips the file
    zf = zipfile.ZipFile(folder + ".zip", "w")
    for dirname, subdirs, files in os.walk(folder):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

# only on linux
subprocess.call("mail -s \"UPDATE: $(hostname) complete\" v2tamprateep@gmail.com < /dev/null".split())