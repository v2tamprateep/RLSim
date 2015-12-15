RLSim
Virin Tamprateep
###############

To use:
The simulator can be run through main.py. You must specify, at least, the agent
(algorithm) to be used and what maze the agent is to run on. To run Q-learning 
on some maze, A, user the following command:

    python main.py --agent=qlearning --maze=A

This simulator outputs the distribution of state-visit-counts (the percentage of
times an agent visited some state). The output is, by default, printed to a file.
This feature can be toggled on or off.

Flags/Parameters:
The follow is a list of supported flags and their behavior:

--help		Help. Display list of flags and uses. OUTDATED.

--agent=	Specify the algorithm to be used. currently supporting Qlearning
		and SARSA. Required.

--maze=		Specify the maze for the agent to learn. Supported mazes are in 
		the Layouts folder. Required.

-a, --alpha	Specify the learning rate of the algorithm (Qlearning and SARSA).
		This value defaults to 0.5 if unspecified.

-g, --gamma	Specify the discount factor of the algorithm (Qlearning and SARSA).
		Defaults to 0.8.

-e, --epsilon	Specify the agent's probability of random movement (exploration).
		Defaults to 1.0.

--mdp		Specify the Markov decision process to be used for the transition
		function. Supported MDP's are located in the MDP folder. Defaults 
		to a deterministic transition function if unspecified.

--trials	Specify the number of runs (through the maze) the agent has to learn.
		Defaults to 1.

--sampleSize	Specify the number of times an agent will learn the maze. The output
		distribution is the average distribution of all the samples. Defaults
		to 1.

--output	Specify an output destination (directories in path must exist). If 
		unspecified, the simulator will generate a file in the current working
		directory with the filename "agent-a$Alpha-g$Gamma-e$Epsilon." For
		example, if I run the the Qlearning agent with default parameters, the
		output file will be called "qlearning-a0.5-g0.8-e0.0".

--consoleOut-Off
		This flag will disable output to the screen. However, the simulator will 
		still output to a file.

--fileOut-Off	This flag will disable output to a file. However, the simulator will still
		output to console/screen.

Mazes:
Mazes use 4 types of symbols. Walls are represented with the percent character ('%'), open
areas use spaces (' '), starting position uses an 'S', and terminal positions use any non-
zero, single digit value, generally 1.

Markov Decision Processes/Transition Function:
