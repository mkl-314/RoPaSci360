# import math 
from classes.Token import Token


_DEFEATS = {"r": "s", "p": "r", "s": "p"}
_DEFEATED_BY = {"r": "p", "p": "s", "s": "r"}


# 0.5 if piece is next to enemy piece

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

def eval(game):
    value = 0

    value += 1 * tokens_on_board(game)
    value += 1 * ((game.tokens_in_hand[game.me]) - (game.tokens_in_hand[game.opponent]))
    #value += token_types(game)
    value += eval_tokens_on_board(game)
    return value

def tokens_on_board(game):
    return len(game.data[game.me]) - len(game.data[game.opponent])


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
