from collections import Counter
import numpy as np
import util


"""
Model-Free Agent class
"""
class RLAgent(object):

    def __init__(self, Maze, alpha, gamma, epsilon, action_cost, learning):
        self.Maze = Maze
        self.action_cost = action_cost
        self.posCounter, self.qValues = Counter(), Counter()
        # self.prev_state = None
        # self.prev_action = None
        self.alpha, self.gamma, self.epsilon = alpha, gamma, epsilon
        self.learning_mode = learning


    def change_maze(self, maze):
        """
        Changes agent's environment and sets agent position to the new environment's start state
        """
        self.Maze = maze
        self.position = maze.start[0]
        self.orientation = maze.start[1]


    def reset_agent(self):
        """
        Reset Agent's state to start state
        """
        self.position = self.Maze.start[0]
        self.orientation = self.Maze.start[1]
        self.posCounter[self.position] += 1

        for state in self.Maze.exploreVal.keys():
            self.Maze.exploreVal[state] += 1


    def update_agent_state(self, next_state, action):
        """
        Update agent's orientation and state, given an action
        """
        self.position = next_state

        # if 'backwards' action, flip orientation
        if util.is_forwards(self.orientation, action):
            self.orientation = action
        else:
            self.orientation = util.oppositeAction(action)

        self.Maze.exploreVal[self.position] = 0
        self.posCounter[self.position] += 1


    def get_action_cost(self, action):
        return -max(self.action_cost[a] for a in action)


    def finished_maze(self):
        return self.Maze.is_terminal(self.position)


    def reset_Qvalues(self):
        self.qValues = Counter()


    def get_value(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.
        """
        legalActions = self.Maze.get_legal_dirs(state)
        lst = [self.qValues[(state, act)] for act in legalActions]
        return max(lst)


    def take_action(self, action):
        pass


    def get_action(self):
        pass


    def update_Qvalues(self):
        pass


"""
Q-Learning Agent
"""
class QLAgent(RLAgent):

    def take_action(self, action):
        new_state, taken_action = self.Maze.take_action(self.position, action)

        self.update_Qvalues(taken_action, new_state)
        self.update_agent_state(new_state, taken_action)


    def update_Qvalues(self, action, nextPos):
        """
        Update Qvalues based on learning_mode
        """
        currVal = self.qValues[(self.position, action)]
        nextVal = self.get_value(nextPos)

        if self.learning_mode == 1: # std
            reward = self.Maze.get_value(nextPos) + self.get_action_cost(action)
        elif self.learning_mode == 2: # RD
            reward = self.Maze.get_discount_value(nextPos) + self.get_action_cost(action)
        elif self.learning_mode == 3: # ER
            reward = self.Maze.get_value(nextPos) + self.get_action_cost(action) + \
                    self.Maze.get_exploration_bonus(nextPos)
        elif self.learning_mode == 4: # RDER
            reward = self.Maze.get_discount_value(nextPos) + self.get_action_cost(action) + \
                    self.Maze.get_exploration_bonus(nextPos)

        self.qValues[(self.position, action)] = currVal + self.alpha*(reward + nextVal - currVal)


"""
SARSA Agent
"""
class SarsaAgent(RLAgent):

    def __init__(self, Maze, alpha, gamma, epsilon, action_cost, learning):
        super(SarsaAgent, self).__init__(Maze, alpha, gamma, epsilon, action_cost, learning)
        self.prev_state, self.prev_action = None, None


    def reset_agent(self):
        super(SarsaAgent, self).reset_agent()
        self.prev_state, self.prev_action = None, None


    def update_agent_state(self, next_state, action):
        self.prev_state = self.position
        self.prev_action = action
        super(SarsaAgent, self).update_agent_state()


    def take_action(self, action):
        new_state, taken_action = self.Maze.take_action(self.position, action)

        # we don't update until the second move
        if self.prev_state is not None and self.prev_action is not None:
            self.update_Qvalues(self.prev_state, self.prev_action, new_state, taken_action)

        # if we finish the maze, update Q-values assuming next action is "exit"
        if self.Maze.is_terminal(new_state):
            self.update_Qvalues(self.prev_state, self.prev_action, self.position, "exit")

        self.update_agent_state(new_state, taken_action)


    def update_Qvalues(self, s1, a1, s2, a2):
        """
        Update Qvalues based on learning_mode
        """
        currVal = self.qValues[(s1, a1)]

        if (a2 == "exit"):
            nextVal = 0
        else:
            nextVal = self.qValues[(s2, a2)]

        if self.learning_mode == 1:
            reward = self.Maze.get_value(s2) + self.get_action_cost(self.prev_action)
        elif self.learning_mode == 2:
            reward = self.Maze.get_discount_value(s2) + self.get_action_cost(self.prev_action)
        elif self.learning_mode == 3:
            reward = self.Maze.get_value(s2) + self.get_action_cost(self.prev_action) + \
                    self.Maze.get_exploration_bonus(s2)
        elif self.learning_mode == 4:
            reward = self.Maze.get_discount_value(s2) + self.get_action_cost(self.prev_action) +\
                    self.Maze.get_exploration_bonus(s2)

        self.qValues[(s1, d1)] = currVal + self.alpha*(reward + nextVal - currVal)

"""
Epsilon Greedy Agent
"""
class EpsilonGreedyAgent(RLAgent):

    def get_probability(self, action):
        legal_actions = self.Maze.get_legal_dirs(self.position)
        lst = [(self.qValues[(self.position, action)], action) for action in legal_actions]
        best_action = max(lst)[0]

        if action == best_action:
            return 1 - self.epsilon + self.epsilon/len(legal_actions)
        else:
            return self.epsilon/len(legal_actions)


    def get_action(self):
        """
        Compute epsilon greedy move
        """
        legal_actions = self.Maze.get_legal_dirs(self.position)
        if util.rand_bool(self.epsilon):
            return util.rand_choice(legal_actions)

        # get mapping from move to value
        lst = [(self.qValues[(self.position, action)], action) for action in legal_actions]
        best = max(lst)[0]

        tiedMoves = [move for val, move in lst if val == best]
        return util.rand_choice(tiedMoves)


"""
Epsilon Soft Agent (Boltzmann Distribution)
"""
class EpsilonSoftAgent(RLAgent):

    def softmax(self, lst):
        """Compute softmax values for each sets of scores in lst"""
        return np.exp(lst) / np.sum(np.exp(lst), axis=0)


    def get_probability(self, action):
        legal_actions = self.Maze.get_legal_dirs(self.position)
        boltz_values = self.softmax([self.qvalues[(self.pos, a)] for a in legal_actions])
        return boltz_values[legal_actions.index(action)]


    def get_action(self):
        legal_actions = self.Maze.get_legal_dirs(self.position)
        if util.rand_bool(self.epsilon):
            return util.rand_choice(legal_actions)

        boltz_values = self.softmax([self.qvalues[(self.pos, a)] for a in legal_actions])
        return np.random.choice(legal_actions, p=boltz_values)


"""
Epsilon Greedy Q-Learning
"""
class GreedyQLAgent(QLAgent, EpsilonGreedyAgent):

    pass


"""
Epsilon Soft Q-learning
"""
class SoftQLAgent(QLAgent, EpsilonSoftAgent):

    pass


"""
Epsilon Greedy SARSA
"""
class GreedySarsaAgent(SarsaAgent, EpsilonGreedyAgent):

    pass


"""
Epsilon Soft SARSA
"""
class EpsilonSoftSarsaAgent(SarsaAgent, EpsilonSoftAgent):

    pass
