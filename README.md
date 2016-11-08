## Synopsis
RLSim is a reinforcement learning simulator, created specifically for comparing agent behaviors to animal behaviors. The simulator employ RL agents in maze environments. Or, given animal behavior data as input, the simulator will train the agent according to given data.

## Motivation
This project was developed to compare the behavior of learning agents in a maze environment to that of animals, using data from neuroscience research. The simulator attempts to recreate the situation of the animal for the learning agent. For example, neurological equipment can cause certain movements to become more difficult. 

## Features
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

## Parameters
|Flag          |Description
|--------------|----------------------------------------|
| --algo       |specify name of RL algorithm
|  --mazes     |maze config file
|-s, --samples |number of samples (learn.py only)
|--mdp         |name of .mdp file
|-a, --alpha|        learning rate
|-g, --gamma|        discount value
|-e, --epsilon|      epsilon-greedy parameter
|-l, --learning|     agent's update function
|-b, --back_cost|    penalization for backward movement
|-R, --reward|       reward for finishing maze
|-d, --deadend_cost| penalty for reaching a deadend
|-q, --Qreset|       interval at which qvalues are reset (learn.py only)
|-o, --output|       output file

## Installation
`git clone git@github.com:v2tamprateep/RLSim.git`

## Usage Example
To run an agent through a maze, returning the paths taken per episode:
 `python learn.py --algo softqlearning --mazes <maze_file> --output <file_path>`
 
To train an agent using animal behavioral data: 
 `python tether.py --algo softsarsa --mazes RLSim/config/150 --input <file>  --output <file_path>`

Examples of maze layout, MDP, and maze config files can be found in their respective folders. 