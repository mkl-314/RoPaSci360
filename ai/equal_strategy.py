from classes.Token import Token
from moves.throw_move import throwable_hexes, throwable_row_range
from math import inf
import random
from gametheory import solve_game
from classes.GameBoard import GameBoard
import numpy as np
from ai.heuristic import *


def actions(state, my_action):
    next_states = []

    if my_action:
        tokens = state.data[state.me]
        token_type = state.me
    else: 
        tokens = state.data[state.opponent]
        token_type = state.opponent


    # Throw moves
    # if state.tokens_in_hand[token_type] > 0:
    #     for hex in throwable_hexes(state, token_type):
    #         for token in ["r", "p", "s"]:
    #             player = Token([token, None, None], token_type == "upper")

    #             new_state = state.apply_action(player, hex, my_action)

    #             #if state.num_tokens != new_state.num_tokens:
    #             next_states.append( [new_state, player, hex])

    # Slide and Swing moves
    for token in tokens:
        player = Token(token, token_type == "upper")
        player_actions = player.viable_actions(state, True)
    
        for player_action in player_actions:
            new_state = state.apply_action(player, player_action, my_action)
            next_states.append( [new_state, player, player_action])


    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states


def defeat_actions(state, my_action):
    next_states = []

    if my_action:
        token_type = state.me
        enemy_token_type = state.opponent
    else: 
        token_type = state.opponent
        enemy_token_type = state.me


    # Throw moves
    if state.tokens_in_hand[token_type] > 0:
        throw_hexes = throwable_hexes(state, token_type)
        for hex, tokens in state.board_dict.items():
            if hex in throw_hexes:
                if (token_type == "upper" and tokens.islower()) or \
                    (token_type == "lower" and tokens.isupper()):

                    enemy_token = Token([tokens[0].lower(), hex[0], hex[1]], token_type != "upper" )
                    player = Token([enemy_token.defeated_by , None, None], token_type == "upper")
                    new_state = state.apply_action(player, hex, my_action)
                    next_states.append( [new_state, player, hex])


    # Slide and Swing moves
    for player_data in state.data[token_type]:
        player = Token(player_data, token_type == "upper")

        new_state = 0
        for enemy_data in state.data[enemy_token_type]:
            enemy = Token(enemy_data, token_type == "upper")
            # Player defeats enemyponenet
            if player.defeats == enemy.symbol: 
                if heuristic_swing(state, player, enemy) == 1:
                    #TODO If my token is also on this hex then isnore this state. 
                    # Should I do this?
                    new_state = state.apply_action(player, [enemy.r, enemy.q], True)
                    next_states.append( [new_state, player, [enemy.r, enemy.q]] )

            # player gets defeated by opponenet
            elif player.defeated_by == enemy.symbol:
                if heuristic_swing(state, enemy, player) == 1:
                    player_actions = player.viable_actions(state, True)
                    for player_action in player_actions:
                        new_state = state.apply_action(player, player_action, my_action)
                        next_states.append( [new_state, player, player_action])
        
        # Check if token can be thrown onto
        if new_state == 0:
            if state.tokens_in_hand[enemy_token_type] > 0:
                if player.r in throwable_row_range(state, enemy_token_type):
                    player_actions = player.viable_actions(state, True)
                    for player_action in player_actions:
                        new_state = state.apply_action(player, player_action, my_action)
                        next_states.append( [new_state, player, player_action])

    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states

def equilibrium_eval(state):

    score_rows = [] # each row our action
    row_actions = [] # action for later use

    my_defeat_actions = defeat_actions(state, True)
    op_defeat_actions = defeat_actions(state, False)
    #my_actions = actions(state, True)


    print("simplified: " + str(len(my_defeat_actions)))
    # print("original: " + str(len(my_actions)))

    for my_action in my_defeat_actions:
        score_row = [] 
        row_actions.append(my_action) # add this action to action array

        for op_action in op_defeat_actions:

            my_token_action = my_action[1].do_action(my_action[2])
            op_token_action = op_action[1].do_action(op_action[2])

            new_state = state.update_copy(my_token_action, op_token_action)

            score = len(new_state.data[state.me]) - len(state.data[state.me])
            score += len(state.data[state.opponent]) - len(new_state.data[state.opponent]) 
            score += 1.5 * (new_state.tokens_in_hand[state.me] -state.tokens_in_hand[state.me])
            score += 0.5 * (state.tokens_in_hand[state.opponent] -new_state.tokens_in_hand[state.opponent])
            score_row.append(score) # add row to matrix

        score_rows.append(score_row)

    # for my_action in my_actions: # for every action we can do (rows in matrix)
    #     score_row = [] # create new empty row
    #     row_actions.append(my_action) # add this action to action array


    #     op_actions = actions(my_action[0], False)

    #     for op_action in op_actions: # for every action enemy can do (column in matrix)
    #         score = len(op_action[0].data[state.me]) - len(state.data[state.me]) # score = how many our token gained (negative if lost)
    #         score += len(state.data[state.opponent]) - len(op_action[0].data[state.opponent]) # score + how many enemy lost (negative if gain)
    #         score_row.append(score) # add row to matrix

    #     score_rows.append(score_row) # add score row to final matrix

    score_rows_output = np.array(score_rows) # convert to numpy
    return score_rows_output, row_actions


