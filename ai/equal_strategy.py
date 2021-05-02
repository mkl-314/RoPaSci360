from classes.Token import Token
from moves.throw_move import throwable_hexes
from math import inf
import random
from gametheory import solve_game
from classes.GameBoard import GameBoard
import numpy as np

def heuristic(token1, token2):
    # Difference in row (negative)
    x = -token1.r + token2.r
    # Difference in column
    y = token1.q - token2.q
    # Difference of differences
    d = x - y
    # Highest absolute is distance
    return max(abs(x) ,abs(y) ,abs(d))


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
                if len(state.data[state.me]) != len(new_state.data[state.me]):
                    next_states.append( [new_state, player, player_action])


    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states




def create_array(state):
    # Timmy to do
    # A = np.array([
    #     [  -1,  0 ],
    #     [ 0,  -1 ],
    #     [0, 0]
    # ])
    
    # array = solve_game(A, maximiser=True, rowplayer=True)
    # array_round = [round(elem, 2) for elem in array[0]]

    #print("soln:", array)
    # print("soln:", array_round)
    # print(round( array[1], 2))
    score_rows = [] # each row our action
    row_actions = [] # action for later use

    for my_action in actions(state, True): # for every action we can do (rows in matrix)
        score_row = [] # create new empty row
        row_actions.append(my_action) # add this action to action array

        for op_action in actions(my_action[0], False): # for every action enemy can do (column in matrix)
            score = len(op_action[0].data[state.me]) - len(state.data[state.me]) # score = how many our token gained (negative if lost)
            score += len(state.data[state.opponent]) - len(op_action[0].data[state.opponent]) # score + how many enemy lost (negative if gain)
            score_row.append(score) # add row to matrix

        score_rows.append(score_row) # add score row to final matrix

    score_rows_output = np.array(score_rows) # convert to numpy
    return score_rows_output, row_actions


