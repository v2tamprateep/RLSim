
import random
import util

"""
Parent Agent class
"""
class RLAgent(object):

    def __init__(self, Maze, action_cost):
        self.Maze = Maze
        # self.MDP = MDP
        self.action_cost = action_cost
        self.posCounter = util.Counter()


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

        for state in self.Maze.exploreVal.keys():
            self.Maze.exploreVal[state] += 1


    def next_position(self, position, action, orientation):
        """
        Return next state, given state-action pair and current orientation
        """
        direction = util.actionToDirection(orientation, action)
        x, y = position[0], position[1]

        for d in direction:
            if d is 'N': y += 1
            if d is 'E': x += 1
            if d is 'W': x -= 1
            if d is 'S': y -= 1
        return (x, y)


    def update_agent_state(self, action):
        """
        Update agent's orientation and state, given an action
        """
        moves = self.Maze.get_legal_actions(self.position, self.orientation)
        self.position = self.next_position(self.position, action, self.orientation)
        self.orientation = util.actionToDirection(self.orientation, action)

        # if 'backwards' action, flip orientation
        if ('B' in action):
            self.orientation = util.oppositeAction(self.orientation)

        self.Maze.exploreVal[self.position] = 0
        self.posCounter[self.position] += 1


    def get_action_cost(self, action):
        return -max(self.action_cost[a] for a in action)


    def finished_maze(self):
        return self.Maze.is_terminal(self.position)


    def reset_Qvalues(self):
        self.qValues.reset()


    def get_action(self):
        pass    


    def take_action(self, action):
        new_position = Maze.apply_action(self.position, action)


"""
Q-Learning
"""
class QLearningAgent(RLAgent):

    def __init__(self, Maze, alpha, gamma, epsilon, action_cost, learning):
        super(QLearningAgent, self).__init__(Maze, action_cost)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.qValues = util.Counter()
        self.learning_mode = learning


    def get_value(self, state):
        """
        Returns max_action Q(state,action)
        where the max is over legal actions.
        """
        legalActions = self.Maze.get_legal_actions(state, self.orientation)
        lst = [self.qValues[(state, util.actionToDirection(self.orientation, act))] for act in legalActions]
        return max(lst)


    def get_action(self):
        """
        Compute epsilon greedy move
        """
        moves = self.Maze.get_legal_actions(self.position, self.orientation)
        if util.flipCoin(self.epsilon): moves = [util.randomMove(moves)]

        lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]
        best = max(lst)[0]

        tiedMoves = [move for val, move in lst if val == best]
        maxQMove = util.randomMove(tiedMoves)
        # mdpMove = self.MDP.get_MDP_move(self.position, maxQMove, moves)

        direction = util.actionToDirection(self.orientation, maxQMove)

        self.update_Qvalues(maxQMove)
        self.update_agent_state(maxQMove)
        return maxQMove


    def update_Qvalues(self, action):
        """
        Update Qvalues based on learning_mode
        """
        nextPos = self.next_position(self.position, action, self.orientation)
        currVal = self.qValues[(self.position, util.actionToDirection(self.orientation, action))]
        nextVal = self.get_value(nextPos)

        if self.learning_mode == 1: # std
            reward = self.Maze.get_value(nextPos) + self.get_action_cost(action)
        elif self.learning_mode == 2: # RD
            reward = self.Maze.get_discount_value(nextPos) + self.get_action_cost(action)
        elif self.learning_mode == 3: # ER
            reward = self.Maze.get_value(nextPos) + self.get_action_cost(action) + self.Maze.get_exploration_bonus(nextPos)
        elif self.learning_mode == 4: # RDER
            reward = self.Maze.get_discount_value(nextPos) + self.get_action_cost(action) + self.Maze.get_exploration_bonus(nextPos)

        self.qValues[(self.position, util.actionToDirection(self.orientation, action))] = currVal + self.alpha*(reward + nextVal - currVal)


"""
SARSA
"""
class SarsaAgent(QLearningAgent):

    def __init__(self, Maze, alpha, gamma, epsilon, action_cost, learning):
        super(SarsaAgent, self).__init__(Maze, alpha, gamma, epsilon, action_cost, learning)
        self.prev_state, self.prev_action, self.prev_dir = None, None, None


    def finished_maze(self):
        """
        We need to overload finished_maze function to update the Q-value of the state leading to the terminal state;
        we also need to reset the previous state
        """
        if self.Maze.is_terminal(self.position):
            self.update_Qvalues(self.prev_state, self.prev_dir, self.position, "exit")
            self.prev_state, self.prev_action, self.prev_dir = None, None, None
            return True
        return False


    def get_action(self):
        """
        first move by sarsa agent; selects a mvoe but doesn't update
        """
        moves = self.Maze.get_legal_actions(self.position, self.orientation)
        if util.flipCoin(self.epsilon): moves = [util.randomMove(moves)]

        lst = [(self.qValues[(self.position, util.actionToDirection(self.orientation, move))], move) for move in moves]
        best = max(lst)[0]

        tiedMoves = [move for val, move in lst if val == best]
        maxQMove = util.randomMove(tiedMoves)
        # mdpMove = self.MDP.get_MDP_move(self.position, maxQMove, moves)

        direction = util.actionToDirection(self.orientation, mdpMove)
        # update Q-values
        if self.prev_state is not None and self.prev_dir is not None:
            self.update_Qvalues(self.prev_state, self.prev_dir, self.position, direction)

        # update "previous" moves
        self.prev_state = self.position
        self.prev_dir = util.actionToDirection(self.orientation, maxQMove)
        self.prev_action = maxQMove

        # update agent state
        self.update_agent_state(maxQMove)
        return maxQMove


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
