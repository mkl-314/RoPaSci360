import math 
from classes.Token import Token
from moves.throw_move import *
from ai.heuristic import *
_DEFEATS = {"r": "s", "p": "r", "s": "p"}
_DEFEATED_BY = {"r": "p", "p": "s", "s": "r"}

'''
Heursitic algorithm to find hex distance between two tokens
'''
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

def eval(game):
    value = 0

    value += 100 * tokens_on_board(game)
    value += 100 * tokens_in_hand(game)
    #value += token_types(game)
    value += 1 * defeat_token_distance(game)

    if game.tokens_in_hand[game.opponent] > 0:
        value += 1 * token_board_progression(game)

    # value += 1 * invisible_token_types(game)
    value += 10 * eval_tokens_on_board(game)
    return value



def tokens_on_board(game):
    return len(game.data[game.me]) - len(game.data[game.opponent])

def tokens_in_hand(game):
    return ((game.tokens_in_hand[game.me]) - (game.tokens_in_hand[game.opponent]))


# Ensure my token can defeat any of opponents tokens
def token_types(game):


    my_symbols = {"r": 0, "p": 0, "s": 0}
    op_symbols = {"r": 0, "p": 0, "s": 0}
    value = 0
    for my_data in game.data[game.me]:
        my_symbols[my_data[0]] += 1


    for opponent_data in game.data[game.opponent]:
        op_symbols[opponent_data[0]] += 1
    
    for token_type in ["r", "p", "s"]:
        if my_symbols[token_type] > 0 and op_symbols[_DEFEATS[token_type]] > 0:
            value += game.w3
        
        if my_symbols[token_type] > 0 and op_symbols[_DEFEATED_BY[token_type]] > 0:
            value -= game.w4

    return value

def invisible_token_types(game):


    my_symbols = {"r": 0, "p": 0, "s": 0}
    op_symbols = {"r": 0, "p": 0, "s": 0}
    value = 0
    for my_data in game.data[game.me]:
        my_symbols[my_data[0]] += 1


    for opponent_data in game.data[game.opponent]:
        op_symbols[opponent_data[0]] += 1
    
    for token_type in ["r", "p", "s"]:
        if my_symbols[token_type] == 0 and op_symbols[_DEFEATS[token_type]] > 0:
            # enemy has token which cannot be killed
            value -= 1 #game.w3
        
        if my_symbols[token_type] > 0 and op_symbols[_DEFEATED_BY[token_type]] == 0:
            # we have token which can be killed
            value += 1 #game.w3 must be zero sum

    return value


def token_board_progression(game):
    value = 0

    if game.me == "upper":
        my_initial_row = 4
    else:
        my_initial_row = -4

    for my_data in game.data[game.me]: 
        value += 8 - abs(my_initial_row - my_data[1])

    for op_data in game.data[game.opponent]: 
        value -= 8 - abs(-1 * my_initial_row - op_data[1])

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
                    value += 8 - min_distance
            
            return value / len(game.data[enemy])
        
        return value

    return token_distances(game, game.me) - token_distances(game, game.opponent)


# prefers tokens being close together
def eval_tokens_on_board(game_board):
    value = 0

    my_symbols = {"r": 0, "p": 0, "s": 0}
    op_symbols = {"r": 0, "p": 0, "s": 0}

    my_sorted_tokens = sorted(game_board.data[game_board.me])
    # Evaluate placement of tokens
    for i in range(len(my_sorted_tokens)):
        my_data = my_sorted_tokens[i]
        my_token = Token(my_data, game_board.me == "upper")
        value += 0.001 * len(my_token.viable_actions(game_board, True))

        # Avoid putting the same token on each other
        if i > 0 and my_sorted_tokens[i-1] == my_data:
            value -= 1

        my_symbols[my_token.symbol] += 1


    for opponent_data in game_board.data[game_board.opponent]:
        op_token = Token(opponent_data, game_board.me == "upper")
        # value -= 0.001 * len(op_token.viable_actions(game_board, True))

        op_symbols[op_token.symbol] += 1

    

    
    # Evaluate token symbols compared to opponents
    for (symbol, num) in op_symbols.items():
        if num > 0:
            if my_symbols[_DEFEATED_BY[symbol]] > 0:
                value += 0.1
            
            # if my_symbols[_DEFEATS[symbol]] > 0:
            #     value -= 0.1


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

            h_dist = heuristic(my_token, op_token)
            h_defeat_dist.append(h_dist)

        for op_data in op_defeated_by_data:
            op_token = Token(op_data, game_board.opponent)

            h_dist = heuristic(my_token, op_token)
            h_defeated_by_dist.append(h_dist)


        
    if h_defeat_dist != []:
        min_dist = min(h_defeat_dist)
        value += 0.01*(8-min_dist)      
        
    
    if h_defeated_by_dist != []:
        min_dist = min(h_defeated_by_dist)
        value -= 0.01*(8-min_dist)    
    # Evaluate protection by my tokens
    # for my_data in game_board.data[game_board.me]:
    #     my_token = Token(my_data, game_board.me)

        # Protect token that can be taken
        
    return value
