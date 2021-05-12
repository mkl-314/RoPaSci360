from classes.Token import Token
from math import inf
import random
from gametheory import solve_game
from classes.GameBoard import GameBoard
import numpy as np
from ai.equal_strategy import equilibrium_strategy
from ai.helper_functions import *
from ai.eval import minimax_eval, equilibrium_eval

CUT_OFF_LIMIT = 1
_DEFEATS = {"r": "s", "p": "r", "s": "p"}
_DEFEATED_BY = {"r": "p", "p": "s", "s": "r"}


def minimax_manager(game):

    value, move = max_value(game, game, -inf, inf)

    return move

def max_value(state, game, a, b):
    if state.turn - game.turn >= CUT_OFF_LIMIT:
        return minimax_eval(state), None
    
    val = -inf 

    # Apply when tokens are attacking
    val, my_move = equilibrium_strategy(state, game, val)
    if my_move != None:
        if my_move[1] != None:

            return val, my_move[1:3]


    #print("minimax")
    val = -inf
    best_moves = []
    #best_eval = -inf
    for s in actions(state, True):
        a_temp, move2 = min_value(s[0], game, a, b)

        if a_temp > val:
            val, move = a_temp, s[1:3]
            a = max(val, a)
            best_moves = [move]
        elif val - a_temp < 0.05:
            best_moves.append(s[1:3])

        if val >= b:
            return val, move         

    move = random.choice(best_moves)
    #move = best_moves[0]

    return val, move

'''
return value, action

'''
def min_value(state, game, a, b):

    if state.turn - game.turn >= CUT_OFF_LIMIT:
        return minimax_eval(state), None
    
    val = inf
    best_moves = [] 
    for s in actions(state, False):
        b_temp, move2 = max_value(s[0], game, a, b)

        if b_temp < val:
            val, move = b_temp, s[1:3]
            b = min(val, b)
            best_moves.append(move)

        if val >= a:
            return val, move 

    move = random.choice(best_moves)
    return val, move


