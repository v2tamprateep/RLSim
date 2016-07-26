import pandas as pd
import subprocess

df = pd.read_csv("./scripts/tri_sum.csv")

reset = None
for i in range(len(df['agent'])):
    if 'var' in str(df['agent'][i]):
        continue

    agent = str(df['agent'][i]).split('_')[0]
    alpha = str(df['alpha'][i])
    back = str(df['back'][i])
    epsilon = str(df['epsilon'][i])
    reward = str(df['reward'][i])

    if "RDER" in str(df['agent'][i]):
        learning = '4'
    elif "ER" in str(df['agent'][i]) and "RD" not in str(df['agent'][i]):
        learning = '3'
    elif "RD" in str(df['agent'][i]) and "ER" not in str(df['agent'][i]):
        learning = '2'
    elif "std" in str(df['agent'][i]):
        learning = '1'

    if "4" in str(df['agent'][i]):
        reset = '4'
    elif "16" in str(df['agent'][i]):
        reset = '16'
    elif "6" in str(df['agent'][i]):
        reset = "6"
    elif "8" in str(df['agent'][i]):
        reset = '8'
    elif "12" in str(df['agent'][i]):
        reset = '12'
    elif "19" in str(df['agent'][i]):
        reset = '19'

    print(agent, learning, reset, alpha, epsilon, back, reward)

    if reset == None:
        subprocess.call(['bash', './scripts/run_sim.sh', '-A', agent, '-a', alpha, \
                        '-e', epsilon, '-R', reward, '-b', back, '-l', learning, \
                        '-f', '../sim_data/6_state/epsilon-deadend/tri/'])
    else:
        subprocess.call(['bash', './scripts/run_sim.sh', '-A', agent, '-r', reset, '-a', alpha, \
                        '-e', epsilon, '-R', reward, '-b', back, '-l', learning, \
                        '-f', '../sim_data/6_state/epsilon-deadend/tri/'])
