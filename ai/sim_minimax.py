from classes.Token import Token
from moves.throw_move import *
from math import inf
import random
from gametheory import solve_game
from classes.GameBoard import GameBoard
import numpy as np
from ai.equal_strategy import *
from ai.heuristic import *

CUT_OFF_LIMIT = 1
E_CUT_OFF_LIMIT = 1
_DEFEATS = {"r": "s", "p": "r", "s": "p"}
_DEFEATED_BY = {"r": "p", "p": "s", "s": "r"}


def test_solve():
    game_board = GameBoard("upper")
    game_board.update(('THROW', 'r', (4, 0)), ('THROW', 'p', (-4, 2)))
    game_board.update(('THROW', 'r', (0, 0)), ('THROW', 'p', (0, 1)))


def minimax_manager(game):

    value, move = max_value(game, game, -inf, inf)
    #game_board = GameBoard("upper")
    # game_board.update(('THROW', 'r', (0, 0)), ('THROW', 'p', (0, 1)))

    #array, my_moves = create_array(game_board)
    # print(array)

    return move

def max_value(state, game, a, b):
    score_rows_output, row_actions = create_array(state, game)
    probabilities, v_score = solve_game(score_rows_output, maximiser=True, rowplayer=True)
    random_value = random.uniform(0, 1)
    sum = 0
    if probabilities is not None:
        for probindex in range(len(probabilities)):
            sum += list(probabilities)[probindex]
            action_index = probindex
            if sum > random_value:
                break 
    else: 
        action_index = np.random.choice(len(row_actions))
        
    #action = np.random.choice(range(len(row_actions)), prob)
    return 0, row_actions[action_index]



    # if state.turn - game.turn >= CUT_OFF_LIMIT:
    #     return state.eval(), None
    
    # val = -inf 

    # # Apply when tokens are attacking
    # val, my_move = equilibrium_strategy(state, game, val)
    # if my_move != None:

    #     # if my_move[0] == None:
    #     #     # my_move[1] = token runs away
    #     #     run_away_token = my_move[1]
            
    #     #     val = -inf

    #     #     player_actions = run_away_token.viable_actions(state, True)
    #     #     for player_action in player_actions:
    #     #         new_state = state.apply_action(run_away_token, player_action, True)

    #     #         if new_state.eval() > val:
    #     #             my_move = [new_state, run_away_token, player_action]
    #     print("equilibrium")
    #     return val, my_move[1:3]


    # print("minimax")
    # val = -inf
    # best_moves = []
    # #best_eval = -inf
    # for s in actions(state, True):
    #     a_temp, move2 = min_value(s[0], game, a, b)

    #     if a_temp > val:
    #         val, move = a_temp, s[1:3]
    #         a = max(val, a)
    #         best_moves = [move]
    #     elif a_temp == val:
    #         best_moves.append(s[1:3])

    #     if val >= b:
    #         return val, move         

    # #move = random.choice(best_moves)
    # move = best_moves[0]

    # return val, move

'''
return value, action

'''
def min_value(state, game, a, b):
    #state.turn -= 1

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

    # Throw moves
    if state.tokens_in_hand[token_type] > 7:
        for hex in throwable_hexes(state, token_type):
            for token in ["r", "p", "s"]:
                player = Token([token, None, None], token_type == "upper")

                new_state = state.apply_action(player, hex, my_action)
                next_states.append( [new_state, player, hex])

    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states

def create_array(state, game):
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
            if state.turn - game.turn >= 1:
                score = score_func(op_action[0])
            else: 
                score = score_func(op_action[0])
                #matrix_of_action, row_actions = create_array(op_action[0], game)
                #v, score = solve_game(matrix_of_action)
            score_row.append(score) # add row to matrix

        score_rows.append(score_row) # add score row to final matrix

    score_rows_output = np.array(score_rows) # convert to numpy
    return score_rows_output, row_actions

def score_func(state):
    score = len(state.data[state.me]) + state.tokens_in_hand[state.me] - state.tokens_in_hand[state.opponent] - len(state.data[state.opponent])
    return score