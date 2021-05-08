from classes.Token import Token
from moves.throw_move import throwable_hexes, throwable_row_range
from math import inf
import random
from gametheory import solve_game
from classes.GameBoard import GameBoard
import numpy as np
from ai.heuristic import *
import copy
_DEFEATS = {"r": "s", "p": "r", "s": "p"}
_DEFEATED_BY = {"r": "p", "p": "s", "s": "r"}

E_CUT_OFF_LIMIT = 0

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
                    #TODO If my token is also on this hex then isnore this state. 
                    # Should I do this?
                    # running_states = running_away_actions(player, state, my_action)
                    # next_states.extend(running_states)
                    new_state = state.apply_action(player, [enemy.r, enemy.q], my_action)
                    next_states.append( [new_state, player, [enemy.r, enemy.q]] )

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
            if player.symbol.lower() in state.board_dict[t_hex].lower():
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
def equilibrium_eval(state):

    score_rows = [] # each row our action
    all_actions = []
    my_defeat_actions = defeat_actions(state, True)
    op_defeat_actions = defeat_actions(state, False)

    # reduce my actions by figuring out running away moves later 
    # print("simplified: " + str(len(my_defeat_actions)))

    for my_action in my_defeat_actions:
        score_row = [] 
        row_action = []
        for op_action in op_defeat_actions:

            my_token_action = my_action[1].do_action(my_action[2])
            op_token_action = op_action[1].do_action(op_action[2])

            new_state = state.update_copy(my_token_action, op_token_action)

            score = calc_score(new_state, state)

            score_row.append(score) # add row to matrix
            row_action.append([new_state] + my_action[1:3])

        score_rows.append(score_row)
        all_actions.append(row_action)

    score_rows_output = np.array(score_rows)
    return score_rows_output, all_actions 

def calc_score(new_state, state):

    # Eval when comparing prev state
    # score = len(new_state.data[state.me]) - len(state.data[state.me])
    # score += len(state.data[state.opponent]) - len(new_state.data[state.opponent]) 
    # score += 1.3 * (new_state.tokens_in_hand[state.me] -state.tokens_in_hand[state.me])
    # score += 1.3 * (state.tokens_in_hand[state.opponent] -new_state.tokens_in_hand[state.opponent])
    
    # Eval based on current state
    score = len(new_state.data[state.me]) - len(new_state.data[state.opponent]) 
    score += 1.3 * (new_state.tokens_in_hand[state.me] - new_state.tokens_in_hand[state.opponent])
    score += invincible_us(state)


    return score

def is_invincible_state(state):

    my_symbols = {"r": 0, "p": 0, "s": 0}
    op_symbols = {"r": 0, "p": 0, "s": 0}
    for my_data in state.data[state.me]:
        my_symbols[my_data[0]] += 1

    for opponent_data in state.data[state.opponent]:
        op_symbols[opponent_data[0]] += 1
    
    invincible = 0
    for token_type in ["r", "p", "s"]:
        if my_symbols[token_type] == 0 and op_symbols[_DEFEATS[token_type]] > 0:
            # enemy has token which cannot be killed
            if (len(my_symbols) <= 1 and state.tokens_in_hand[state.me] == 0):
                invincible = -1
        
        if my_symbols[token_type] > 0 and op_symbols[_DEFEATED_BY[token_type]] == 0:
            # we have token which can be killed
            if (len(op_symbols) <= 1 and state.tokens_in_hand[state.opponent] == 0):
                invincible = 1
            
    return invincible

def is_win_state(state):
    my_symbols = {"r": 0, "p": 0, "s": 0}
    op_symbols = {"r": 0, "p": 0, "s": 0}

    win = 0
    if (state.tokens_in_hand[state.me] == 0) & (state.data[state.me] == 0):
        if (state.tokens_in_hand[state.opponent] > 0) or (state.data[state.opponent] > 0):
            # we have nothing opponent has something
            win = -1
        # else draw
    else (state.tokens_in_hand[state.opponent] == 0) & (state.data[state.opponent] == 0):
        # we have something but opponent has nothing
        win = 1

    return win

# Recursive Backward Induction Algorithm
def equilibrium_strategy(state, game, value):

    if state.turn - game.turn >= E_CUT_OFF_LIMIT:
        value, move = choose_move(state)
        return value, move
    
    else:

        array, all_moves = equilibrium_eval(state)

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

            print("line 183")
            #print(prob_array)
            print(array)

            return 0, my_move

        return value, None

def choose_move(state, array=np.array([]), all_moves=[]):

    if array.size == 0:
        array, all_moves = equilibrium_eval(state)
        find_move = False
    else:
        find_move = True

    if array.size > 0:
        prob_array, value = solve_game(array)
        # print(array)
        # print(prob_array)
        if value == None:
            #prob_array = [round(elem, 2) for elem in prob_array]
            print("line 196")
            #print(prob_array)
            print(array)
            # solution is trivially zero - bc can only run away

            # or only attack
            '''
            if all array > 0
            '''
            #TODO find best run away move !!!!
            # if find_move:
            #     # Get a move
            #     move = all_moves[0][0]
            #     my_token = move[1]
            #     if my_token.r == None:
            #         return 0, move
            #     run_moves = running_away_actions(my_token, state, True, get_action=False)

            #     new_moves = []
            #     value = 0
            #     for run_move in run_moves:
            #         op_token = copy.deepcopy(my_token)
            #         op_token.upper_player = not op_token.upper_player

            #         my_token.update(run_move[2])
            #         # mini eval function:
            #         # Runs far away from token
            #         # moves in a safe token
            #         # moves towards a kill token
            #         if heuristic_swing(state, op_token, my_token) > 1:
            #             # if runs far away or in another token
            #             new_moves.append(run_move)

            #         elif (not run_move[0].board_dict[tuple(run_move[2])].isupper() 
            #             and my_token.upper_player) or \
            #             (not run_move[0].board_dict[tuple(run_move[2])].islower() 
            #             and not my_token.upper_player):
            #             new_moves.append(run_move)

            #     if len(new_moves) > 0:
            #         move_index = random.choices(range(len(new_moves)))
            #         my_move = new_moves[move_index[0]]

            #         return 0.1, my_move
            
            move_index = random.choices(range(len(all_moves)))
            my_move = all_moves[move_index[0]][0]
            # print(len(all_moves))
            return 0, my_move

        else:

            if E_CUT_OFF_LIMIT == 0 or find_move:

                prob_array = [round(elem, 2) for elem in prob_array]
                print(array)
                print(prob_array)
                # print("v: " + str(v))

                move_index = random.choices(range(len(all_moves)), weights=prob_array)
                my_move = all_moves[move_index[0]][0]

                return round(value, 5), my_move

                # print("line 258")
                # prob_array = [round(elem, 2) for elem in prob_array]
                # print(prob_array)
            return value, None
    
    return 0, None
