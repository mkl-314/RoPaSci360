from classes.Token import Token
# from moves.throw_move import throwable_hexes, throwable_row_range
from math import inf
import random
from gametheory import solve_game
from classes.GameBoard import GameBoard
import numpy as np
from ai.helper_functions import *
from ai.eval import *
import copy

E_CUT_OFF_LIMIT = 0

'''
    Find all viable moves
    try sorting to maximise pruning
    return state (game_board)
'''
def actions(state, my_action):
    next_states = []

    if my_action:
        tokens = state.data[state.me]
        token_type = state.me # lower
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

    # Throw moves - reduced
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

    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states

# Returns all actions where a token can defeat or be defeated
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
            enemy = Token(enemy_data, enemy_token_type == "upper")
            # Player defeats enemy
            if player.defeats == enemy.symbol: 
                if heuristic_swing(state, player, enemy) == 1:

                    # player token moves to enemy token
                    new_state = state.apply_action(player, [enemy.r, enemy.q], my_action)
                    next_states.append( [new_state, player, [enemy.r, enemy.q]] )

                    enemy_actions = enemy.viable_actions(state, True)
                    player_actions = player.viable_actions(state, True)
                    viable_hexes_in_common = [hex for hex in enemy_actions if hex in player_actions]
                    for hex in viable_hexes_in_common:
                        new_state = state.apply_action(player, hex, my_action)
                        next_states.append( [new_state, player, hex] )
            # player gets defeated by opponenet
            elif player.defeated_by == enemy.symbol:
                if heuristic_swing(state, enemy, player) == 1:
                    running_states = running_away_actions(player, state, my_action)
                    next_states.extend(running_states)
        
        # Check if token can be thrown onto
        if new_state == 0:
            if state.tokens_in_hand[enemy_token_type] > 0:
                if player.r in throwable_row_range(state, enemy_token_type):
                    running_states = running_away_actions(player, state, my_action)
                    next_states.extend(running_states)

    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states

def running_away_actions(player, state, my_action, get_action=True):
    next_states = []
    player_actions = player.viable_actions(state, True)
    #next_states.append([None, player, player_actions[0]])
    for player_action in player_actions:
        t_hex = (player_action[0], player_action[1]) 
        if t_hex in state.board_dict:
            #if player.symbol.lower() in state.board_dict[t_hex].lower():
            new_state = state.apply_action(player, player_action, my_action)
            next_states.append( [new_state, player, player_action])
                # if get_action:
                #     break
        else:
            new_state = state.apply_action(player, player_action, my_action)
            next_states.append( [new_state, player, player_action])
            # if get_action:
            #     break
    
    return next_states

# Evaluation Function, 
# Returns all moves where a token could be defeated
def payoff_matrix(state):

    score_rows = [] # each row our action
    all_actions = []
    my_defeat_actions = defeat_actions(state, True)
    op_defeat_actions = defeat_actions(state, False)

    # This takes too long
    # if len(my_defeat_actions) == 1 or len(op_defeat_actions) == 1:
    #     my_defeat_actions = actions(state, True)
    #     op_defeat_actions = actions(state, False)


    for my_action in my_defeat_actions:
        score_row = [] 
        row_action = []
        for op_action in op_defeat_actions:

            my_token_action = my_action[1].do_action(my_action[2])
            op_token_action = op_action[1].do_action(op_action[2])

            new_state = state.update_copy(my_token_action, op_token_action)

            score = equilibrium_eval(new_state, state)

            score_row.append(score) # add row to matrix
            row_action.append([new_state] + my_action[1:3])

        score_rows.append(score_row)
        all_actions.append(row_action)

    score_rows_output = np.array(score_rows)
    return score_rows_output, all_actions 


# Recursive Backward Induction Algorithm
def equilibrium_strategy(state, game, value):

    if state.turn - game.turn >= E_CUT_OFF_LIMIT:
        value, move = choose_move(state)
        return value, move
    
    else:

        array, all_moves = payoff_matrix(state)

        if all_moves == [] or array.size == 0:
            return 0, None

        prob_array, value = solve_game(array)

        if value != None:
            prob_array = [round(elem, 2) for elem in prob_array]

            for i in range(len(all_moves)):
                if prob_array[i] > 0:
                    row_moves = all_moves[i]
                    for j in range(len(row_moves)):
                        move = row_moves[j]

                        new_val, new_move = equilibrium_strategy(move[0], game, value)
                        if new_val != None:
                            array[i][j] = new_val


            if state.turn == game.turn:
                return choose_move(state, array, all_moves)
        else:
            # Has to run away
            move_index = random.choices(range(len(all_moves)))
            my_move = all_moves[move_index[0]][0]

            return 0, my_move

        return value, None

def choose_move(state, array=np.array([]), all_moves=[]):

    if array.size == 0:
        array, all_moves = payoff_matrix(state)
        find_move = False
    else:
        find_move = True

    if array.size > 0:
        prob_array, value = solve_game(array)
        # print(array)
        # print(prob_array)
        if value == None:
            print("value = None")

            move_index = random.choices(range(len(all_moves)))
            my_move = all_moves[move_index[0]][0]
            # print(len(all_moves))
            return 0, my_move

        else:

            if E_CUT_OFF_LIMIT == 0 or find_move:

                prob_array = [round(elem, 2) for elem in prob_array]
                print(array)
                print(prob_array)
                
                move_index = random.choices(range(len(all_moves)), weights=prob_array)
                my_move = all_moves[move_index[0]][0]
                return round(value, 5), my_move

            return value, None
    
    return 0, None
