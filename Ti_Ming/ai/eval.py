import math 
from Ti_Ming.classes.Token import Token
from Ti_Ming.ai.helper_functions import *
_DEFEATS = {"r": "s", "p": "r", "s": "p"}
_DEFEATED_BY = {"r": "p", "p": "s", "s": "r"}

def minimax_eval(game):
    value = 0

    value += 1 * tokens_on_board(game)
    value += 1.2 * tokens_in_hand(game)
    if game.turn >= 5:
        value += 0.45 * min_attacking_distance(game)
    value += 0.05 * token_board_progression(game)
    value += 0.16 * num_viable_actions(game)
    return value


def equilibrium_eval(new_state):
    
    # Eval based on next state
    score = 1 * tokens_on_board(new_state)
    score += 1.3 * tokens_in_hand(new_state)
    score += 0.45 * min_attacking_distance(new_state)
    score += 0.16 * num_viable_actions(new_state)
    score += 10 * invincible_state(new_state)
    score += 100 * win_state(new_state)

    return score


def tokens_on_board(game):
    return len(game.data[game.me]) - len(game.data[game.opponent])

def tokens_in_hand(game):
    return ((game.tokens_in_hand[game.me]) - (game.tokens_in_hand[game.opponent]))

# Prioritises tokens being closer to initial row
def token_board_progression(game):

    if game.tokens_in_hand[game.opponent] <= 1:
        return 0

    value = 0

    if game.me == "upper":
        my_initial_row = 4
    else:
        my_initial_row = -4

    no_attacking_token = True
    for my_data in game.data[game.me]: 
        distance = abs(my_initial_row - my_data[1])
        if distance < 5:
            value += 8 - distance
        elif no_attacking_token and distance  >= 5:
            no_attacking_token = False
            value += 8
        elif not no_attacking_token and distance >= 5:
            value += 1

    return value / (len(game.data[game.me]) + len(game.data[game.opponent]))


def defeat_token_distance(game):

    def token_distances(game, player):
        value = 0
        if player == game.me:
            enemy = game.opponent
        else:
            enemy = game.me

        if len(game.data[enemy]) > 0:
            for enemy_data in game.data[enemy]:
                enemy_token = Token(enemy_data, enemy == "upper")
                
                min_distance = math.inf

                for player_data in game.data[player]:
                    player_token = Token(player_data, player == "upper")

                    if enemy_token.defeated_by == player_token.symbol:

                        distance = heuristic_swing(game, player_token, enemy_token)
                        # Find min distance
                        if distance < min_distance:
                            min_distance = distance

                if min_distance != math.inf:
                    if min_distance == 1:
                        value += 10
                    else:
                        value += 8-min_distance
            
            return value / len(game.data[enemy])
        
        return value

    return token_distances(game, game.me) - token_distances(game, game.opponent)


# prefers tokens being close together
def num_viable_actions(game_board):
    value = 0

    my_symbols = {"r": 0, "p": 0, "s": 0}
    op_symbols = {"r": 0, "p": 0, "s": 0}

    my_sorted_tokens = sorted(game_board.data[game_board.me])
    # Evaluate placement of tokens - priorities tokens to have greatest # of moves possible
    for i in range(len(my_sorted_tokens)):
        my_data = my_sorted_tokens[i]
        my_token = Token(my_data, game_board.me == "upper")
        value += 0.01 * len(my_token.viable_actions(game_board, True))

        # Avoid putting the same token on each other
        if i > 0 and my_sorted_tokens[i-1] == my_data:
            value -= 1

        my_symbols[my_token.symbol] += 1
        
    return value


'''
Equilibrium strategy eval
'''
def min_attacking_distance(game_board):
    value = 0
    game_board.split_token_symbols()
    h_defeat_dist = []
    h_defeated_by_dist = []

    # Evaluate heuristic distance and actual distance of opponents 
    for my_data in game_board.data[game_board.me]:
        my_token = Token(my_data, game_board.me)
        op_defeat_data = game_board.op_tokens[my_token.defeats]
        op_defeated_by_data = game_board.op_tokens[my_token.defeated_by]

        for op_data in op_defeat_data:
            op_token = Token(op_data, game_board.opponent)

            h_dist = heuristic_swing(game_board, my_token, op_token)
            h_defeat_dist.append(h_dist)

        for op_data in op_defeated_by_data:
            op_token = Token(op_data, game_board.opponent)

            h_dist = heuristic_swing(game_board, op_token, my_token)
            h_defeated_by_dist.append(h_dist)


        
    if h_defeat_dist != []:
        min_dist = min(h_defeat_dist)
        if min_dist == 1:
            value += 1
        else:
            value += 0.1 * (8-min_dist)
        
    
    if h_defeated_by_dist != []:
        min_dist = min(h_defeated_by_dist)
        if min_dist == 1:
            value -= 1
        else:
            value -= 0.1 * (8-min_dist)

    return value


def invincible_state(state):

    if state.tokens_in_hand[state.opponent] == 0 or state.tokens_in_hand[state.me] == 0:
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
                if (state.tokens_in_hand[state.me] == 0):
                    invincible = -1
            
            if my_symbols[token_type] > 0 and op_symbols[_DEFEATED_BY[token_type]] == 0:
                # we have token which cannot be killed
                if (state.tokens_in_hand[state.opponent] == 0):
                    invincible = 1
                
        return invincible
    return 0

    
def win_state(state):
    if (state.tokens_in_hand[state.me] + len(state.data[state.me])) <= 1:

        win = 0
        if (state.tokens_in_hand[state.me] == 0) & (state.data[state.me] == 0):
            if (state.tokens_in_hand[state.opponent] > 0) or (state.data[state.opponent] > 0):
                # we have nothing opponent has something
                win = -1
            # else draw
        elif (state.tokens_in_hand[state.opponent] == 0) & (state.data[state.opponent] == 0):
            # we have something but opponent has nothing
            win = 1
        elif invincible_state(state) == -1 and state.tokens_in_hand[state.me] + len(state.data[state.me]) == 1:
            win = -1
        elif invincible_state(state) == 1 and state.tokens_in_hand[state.opponent] + len(state.data[state.opponent]) == 1:
            win = 1
        return win
    
    return 0