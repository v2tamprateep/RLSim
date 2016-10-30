Project: RLSim
Author:  Virin Tamprateep
###############

Overview:
RLSim is a reinforcement learning simulator, created specifically for comparing
agent behaviors to animal behaviors. For this reason, the simulator features a
variety of parameters.


Features:
Automated Q-value resets on indicated episodes
  - episodes can be manually specified
  - Q-values can be reset every n episodes where n is a parameter.

Maze swapping
  - user can specify a series of mazes (domains) for the agent to
    act in along with the number of episodes the agent will spend in each maze.

Update functions
  - the simulator supports four variations on the Q-values update
    functions, taking into account exploration bonuses and diminishing rewards.

Agent orientation
  - the simulator tracks the agent's orientation, this allows for
    the option of penalizing backward movement more than forward movement (for 
    simulating difficulty in different movements).


Supported Algorithms:
  - Qlearning (epsilon-greedy action selection)
  - SARSA     (epsilon-greedy action selection)


Simulator Parameters/Flags:
  --algo,             specify name of RL algorithm
  --mazes,            list of mazes for agent to act in
  -t, --trials,       list of trials lengths (for each maze)
  -s, --samples,      number of samples
  --mdp,              name of .mdp file
  -a, --alpha,        learning rate
  -g, --gamma,        discount value
  -e, --epsilon,      epsilon-greedy parameter
  -l, --learning,     agent's update function
  -b, --back_cost,    penalization for backward movement
  -R, --reward,       reward for finishing maze
  -d, --deadend_cost, penalty for reaching a deadend
  -q, --Qreset,       interval at which qvalues are reset
  -o, --output,       output file

