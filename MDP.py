import sys
import random
import utilities


class MDP:
    """
    MDP is a dictionary of dictionaries. The outer dictionary maps each action to
    an inner dictionary. The inner dictionary maps each action to the probability
    of that action occuring. So, MDP[a][a'] = P(a'|a).
    """

    def __init__(self, mdp):
        self.MDP = self.load_MDP(mdp)


    def load_MDP(self, arg):
        """
        Read in .mdp file and asve information in dictionary
        """
        action = ["N", "E", "W", "S", "NE", "NW", "SE", "SW"]
        MDP = {}
        infile = open(arg, "r")
        lst = infile.read().splitlines()

        for line in lst:
            i = 0
            wordlst = line.split()
            first = wordlst[0][:-1]
            MDP[first] = {}
            for word in wordlst:
                isfloat = utilities.isfloat(word[:-1])
                if isfloat != -1:
                    MDP[first][action[i]] = isfloat
                    i += 1
        return MDP


    def normalize(self, position, action, legal_actions):
        """
        If all four actions are possible form a position, does not change
        MDP. If some actions are illegal, adjusts MDP such that the sum
        of all actions = 1
        """
        total = 0.0
        for act in legal_actions:
            total += self.MDP[action][act]

        newMDP = {}
        for act in legal_actions:
            newMDP[act] = self.MDP[action][act]/total

        return newMDP


    def get_MDP_action(self, position, action, legal_actions):
        if action is 'exit': return action

        rand = random.random()
        newMDP = self.normalize(position, action, legal_actions)
        total = 0

        for act in legal_actions:
            total += newMDP[act]
            if rand <= total: return act

        print("get_MDP_action -- Error: no action returned")
