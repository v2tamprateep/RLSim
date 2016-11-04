import sys
import random
import datetime, time
import pandas as pd


"""
Functions
"""
def isfloat(value):
    """
    If value is a real number, return that number
    else return False
    """
    try:
        return float(value)
    except ValueError:
        return -1


def rand_bool(p):
    r = random.random()
    return r < p


def rand_choice(lst):
    return random.choice(lst)


"""
Direction: North, East, West, South
Action: Forwards, Left, Right, Backwards
"""
cardinalDir = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW']
actionLst = ['F', 'FR', 'R', 'BR', 'B', 'BL', 'L', 'FL']
opposite = {'N':'S', 'S':'N', 'W':'E', 'E':'W'}

def oppositeAction(action):
    opAct = ''
    for a in action:
        opAct += opposite[a]
    return opAct


def is_forwards(orientation, action):
    index = cardinalDir.index(orientation)
    return action in [cardinalDir[(index + i)%8] for i in range(-2, 3)]