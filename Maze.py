import utilities
import random


"""
Maze Object; used as Agent's environment
"""
class Maze(object):

    def __init__(self, arg, mdp, reward, reset, deadend_penalty):
        self.MDP = mdp
        self.reset, self.discount = reset, 1
        self.maze, self.start, self.terminal, self.cues = self.load_maze(arg, reward, deadend_penalty)
        self.exploreVal = {state:1 for state in self.maze.keys()}
        self.exploreVal[self.start] = 0


    def load_maze(self, arg, reward, deadend_penalty):
        """
        Read in .lay(out) file and save in dictionary
        """
        infile = open("./Layouts/" + arg + ".lay", "r")
        lst = infile.read().splitlines()

        start = 0
        terminal = []
        dictionary = {}
        cues = {}
        x, y, = 0, 0

        for line in lst[::-1]:
            for char in line:
                # determine terminal states and borders
                if str(char) == "R": # terminal state
                    dictionary[(x, y)] = reward
                    terminal.append((x, y))
                elif str(char) == "d": # deadend
                    dictionary[(x, y)] = -(deadend_penalty)
                elif char != '%': # not a wall; valid states
                    dictionary[(x, y)] = 0
                else:
                    dictionary[(x, y)] = char

                # determine initial orientation
                dirSymbols = ['^', '>', 'v', '<']
                if str(char) in dirSymbols:
                    actions = ['N', 'E', 'S', 'W']
                    start = ((x, y), actions[dirSymbols.index(str(char))])

                if (str(char).isalpha()):
                    cues[(x, y)] = 2
                x += 1
            x = 0
            y += 1

        infile.close()
        return (dictionary, start, terminal, cues)


    def get_legal_states(self):
        return [state for state in self.maze.keys() if self.maze[state] != '%']

    def get_legal_actions(self, position, orientation):
        """
        returns list of possible actions (forward, backwards, left, right)
        """
        actions = self.get_legal_dirs(position)
        return utilities.directionToActionLst(orientation, actions)

    def get_legal_dirs(self, position):
        """
        returns list of possible actions to move in (N, E, W, S)
        """
        actions = []
        x, y = position[0], position[1]

        if self.maze[(x, y + 1)] is not '%': actions.append('N')
        if self.maze[(x + 1, y)] is not '%': actions.append('E')
        if self.maze[(x - 1, y)] is not '%': actions.append('W')
        if self.maze[(x, y - 1)] is not '%': actions.append('S')
        if self.maze[(x - 1, y + 1)] is not '%': actions.append('NW')
        if self.maze[(x - 1, y - 1)] is not '%': actions.append('SW')
        if self.maze[(x + 1, y + 1)] is not '%': actions.append('NE')
        if self.maze[(x + 1, y - 1)] is not '%': actions.append('SE')

        return actions


    def next_state(self, position, action):
        """
        Return next state, given state-action pair and current orientation
        """
        x, y = position[0], position[1]

        for a in action:
            if a is 'N': y += 1
            if a is 'E': x += 1
            if a is 'W': x -= 1
            if a is 'S': y -= 1
        return (x, y)


    def get_value(self, position):
        """ Return value of maze position """
        if (position == "exit"): return 0
        return self.maze[position]


    def get_discount_value(self, position):
        """ Return 'discounted' maze value; reward is discounted per visit """
        if (position == "exit"): return 0

        if (random.random() < self.reset): self.discount = 1
        ret = self.maze[position]/self.discount
        self.discount += 1
        return ret


    def get_exploration_bonus(self, position):
        """ Bonus for visiting not recently visited states """
        return self.exploreVal[position]

    def is_terminal(self, position):
        if position in self.terminal:
            return True
        return False

    def take_action(self, position, action):
        """
        returns new state and actual action taken
        """
        # apply transition function to action
        mdp_action = self.MDP.get_MDP_action(position, action, self.get_legal_dirs(position))
        return self.next_state(position, mdp_action), mdp_action
