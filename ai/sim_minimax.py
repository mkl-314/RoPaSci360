from classes.Token import Token
from moves.throw_move import *
from math import inf
import random
from gametheory import solve_game
from classes.GameBoard import GameBoard
import numpy as np
from ai.equal_strategy import *

CUT_OFF_LIMIT = 1
_DEFEATS = {"r": "s", "p": "r", "s": "p"}
_DEFEATED_BY = {"r": "p", "p": "s", "s": "r"}


def heuristic(token1, token2):
    # Difference in row (negative)
    x = -token1.r + token2.r
    # Difference in column
    y = token1.q - token2.q
    # Difference of differences
    d = x - y
    # Highest absolute is distance
    return max(abs(x) ,abs(y) ,abs(d))

# Heuristic distance + the swing distance in the next move
def heuristic_swing(game, token_move, token2):
    h_dist = heuristic(token_move, token2)
    if h_dist == 2:
        if [token2.r, token2.q] in token_move.viable_actions(game, True):
            h_dist = 1

    return h_dist


def test_solve():
    v = []

    game_board = GameBoard("upper")

    game_board.update(('THROW', 'r', (4, 0)), ('THROW', 'p', (-4, 2)))
    game_board.update(('THROW', 'r', (4, 0)), ('THROW', 'p', (-4, 2)))
    game_board.update(('THROW', 'r', (4, 0)), ('THROW', 'p', (-4, 2)))
    game_board.update(('THROW', 'r', (4, 0)), ('THROW', 'p', (-4, 2)))
    game_board.update(('THROW', 'r', (0, 0)), ('THROW', 'p', (0, 1)))


def minimax_manager(game):

    value, move = max_value(game, game, -inf, inf)

    return move

def max_value(state, game, a, b):
    if state.turn - game.turn >= CUT_OFF_LIMIT:
        return state.eval(), None
    
    # Timmy to implement
    # Find best option to take or avoid being taken
    if state.can_defeat():
        array, my_moves = create_array()
        prob_array, v = solve_game(array)
        
        return v, None
    else:
        #MK to implement
        # 

        # op_actions = actions(state, False)
        # op_best_actions = op_actions[0:10]

        val = -inf 
        best_moves = []
        #best_eval = -inf
        for s in actions(state, True):
            a_temp, move2 = min_value(s[0], game, a, b)

            if a_temp > val:
                val, move = a_temp, s[1:3]
                a = max(val, a)
                best_moves = [move]
            elif a_temp == val:
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
        return state.eval(), None
    
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

'''
    Find all viable moves
    try sorting to maximise pruning
    return state (game_board)
'''
def actions(state, my_action):
    next_states = []

    if my_action:
        tokens = state.data[state.me]
        token_type = state.me
    else: 
        tokens = state.data[state.opponent]
        token_type = state.opponent

    # Slide and Swing moves
    for token in tokens:
        player = Token(token, token_type == "upper")
        player_actions = player.viable_actions(state, True)

        for player_action in player_actions:
                new_state = state.apply_action(player, player_action, my_action)
                next_states.append( [new_state, player, player_action])

    # Throw moves
    if state.tokens_in_hand[token_type] > 0:
        for hex in throwable_hexes(state, token_type):
            for token in ["r", "p", "s"]:
                player = Token([token, None, None], token_type == "upper")

                new_state = state.apply_action(player, hex, my_action)
                next_states.append( [new_state, player, hex])

    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states


