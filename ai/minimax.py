from classes.Token import Token
from moves.throw_move import throwable_hexes
from math import inf
import random

CUT_OFF_LIMIT = 1


def minimax_manager(game):
    #value = max_value(game, game, -inf, inf)

    value, move = max_value(game, game, -inf, inf)
    return move

def max_value(state, game, a, b):
    if state.turn - game.turn >= CUT_OFF_LIMIT:
        return state.eval(), None

    val = -inf 
    best_moves = []

    for s in actions(state, True):
        a_temp, move2 = min_value(s[0], game, a, b)

        if a_temp >= val:
            val, move = a_temp, s[1:3]
            a = max(val, a)
            best_moves.append(move)

        if val >= b:
            return val, move 
    

    move = random.choice(best_moves)
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

        if b_temp <= val:
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
    #next_states.sort(key=lambda x: x[0].eval(), reverse= not my_action)

    return next_states


