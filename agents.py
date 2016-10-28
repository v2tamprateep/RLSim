from collections import Counter
import util

"""
Parent Agent class
"""
class RLAgent(object):

    def __init__(self, Maze, action_cost):
        self.Maze = Maze
        self.action_cost = action_cost
        self.posCounter = Counter()
        self.prev_state = None
        self.prev_action = None


    def change_maze(self, maze):
        """
        Changes agent's environment and sets agent position to the new environment's start state
        """
        self.Maze = maze
        self.position = maze.start[0]
        self.orientation = maze.start[1]


    def reset_agent_state(self):
        """
        Reset Agent's state to start state
        """
        self.position = self.Maze.start[0]
        self.orientation = self.Maze.start[1]
        self.posCounter[self.position] += 1
        self.prev_state, self.prev_action = None, None

        for state in self.Maze.exploreVal.keys():
            self.Maze.exploreVal[state] += 1


    def update_agent_state(self, next_state, action):
        """
        Update agent's orientation and state, given an action
        """
        self.prev_state = self.position
        self.prev_action = action
        self.position = next_state

        # if 'backwards' action, flip orientation
        if (util.is_forwards(self.orientation, action)):
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


    def get_action(self):
        pass


    def take_action(self, action):
        pass


"""
Q-Learning
"""
class QLearningAgent(RLAgent):

    def __init__(self, Maze, alpha, gamma, epsilon, action_cost, learning):
        super(QLearningAgent, self).__init__(Maze, action_cost)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.qValues = Counter()
        self.learning_mode = learning


    def get_value(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.
        """
        legalActions = self.Maze.get_legal_dirs(state)
        lst = [self.qValues[(state, act)] for act in legalActions]
        return max(lst)


    def get_action(self):
        """
        Compute epsilon greedy move
        """
        moves = self.Maze.get_legal_dirs(self.position)
        if (util.rand_bool(self.epsilon)):
            return util.rand_choice(actions)

        # get mapping from move to value
        lst = [(self.qValues[(self.position, move)], move) for move in moves]
        best = max(lst)[0]

        tiedMoves = [move for val, move in lst if val == best]
        maxQMove = util.rand_choice(tiedMoves)
        return maxQMove


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
            reward = self.Maze.get_value(nextPos) + self.get_action_cost(action) + self.Maze.get_exploration_bonus(nextPos)
        elif self.learning_mode == 4: # RDER
            reward = self.Maze.get_discount_value(nextPos) + self.get_action_cost(action) + self.Maze.get_exploration_bonus(nextPos)

        self.qValues[(self.position, action)] = currVal + self.alpha*(reward + nextVal - currVal)


"""
SARSA
"""
class SarsaAgent(QLearningAgent):

    def __init__(self, Maze, alpha, gamma, epsilon, action_cost, learning):
        super(SarsaAgent, self).__init__(Maze, alpha, gamma, epsilon, action_cost, learning)


    def finished_maze(self):
        """
        We need to overload finished_maze function to update the Q-value of the state leading to the terminal state;
        we also need to reset the previous state
        """
        if self.Maze.is_terminal(self.position):
            self.update_Qvalues(self.prev_state, self.prev_action, self.position, "exit")
            self.prev_state, self.prev_action = None, None
            return True
        return False


    def get_action(self):
        """
        first move by sarsa agent; selects a mvoe but doesn't update
        """
        actions = self.Maze.get_legal_dirs(self.position)
        if (util.rand_bool(self.epsilon)):
            return util.rand_choice(actions)

        lst = [(self.qValues[(self.position, action)], action) for action in actions]
        best = max(lst)[0]

        tiedMoves = [move for val, move in lst if val == best]
        maxQMove = util.rand_choice(tiedMoves)
        return maxQMove


    def take_action(self, action):
        new_state, taken_action = self.Maze.take_action(self.position, action)

        if self.prev_state is not None and self.prev_action is not None:
            self.update_Qvalues(self.prev_state, self.prev_action, new_state, taken_action)

        self.update_agent_state(new_state, taken_action)


    def update_Qvalues(self, s1, d1, s2, d2):
        """
        Update Qvalues based on learning_mode
        """
        currVal = self.qValues[(s1, d1)]

        if d2 == "exit":
            nextVal = 0
        else:
            nextVal = self.qValues[(s2, d2)]

        if self.learning_mode == 1:
            reward = self.Maze.get_value(s2) + self.get_action_cost(self.prev_action)
        elif self.learning_mode == 2:
            reward = self.Maze.get_discount_value(s2) + self.get_action_cost(self.prev_action)
        elif self.learning_mode == 3:
            reward = self.Maze.get_value(s2) + self.get_action_cost(self.prev_action) + self.Maze.get_exploration_bonus(s2)
        elif self.learning_mode == 4:
            reward = self.Maze.get_discount_value(s2) + self.get_action_cost(self.prev_action) + self.Maze.get_exploration_bonus(s2)
        self.qValues[(s1, d1)] = currVal + self.alpha*(reward + nextVal - currVal)
