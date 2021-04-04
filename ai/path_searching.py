# import math 
from classes.Token import Token


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


def eval_tokens_on_board(game_board):
    value = 0

    my_symbols = {"r": 0, "p": 0, "s": 0}
    op_symbols = {"r": 0, "p": 0, "s": 0}

    # Evaluate placement of tokens
    for my_data in game_board.data[game_board.me]:
        my_token = Token(my_data, game_board.me == "upper")
        value += 0.001 * len(my_token.viable_actions(game_board, True))

        my_symbols[my_token.symbol] += 1


    for opponent_data in game_board.data[game_board.opponent]:
        op_token = Token(opponent_data, game_board.me == "upper")
        value -= 0.001 * len(op_token.viable_actions(game_board, True))

        op_symbols[op_token.symbol] += 1

    
    # Evaluate token symbols compared to opponents
    for (symbol, num) in op_symbols.items():
        if num > 0:
            if my_symbols[_DEFEATED_BY[symbol]] > 0:
                value += 0.1
            
            # if my_symbols[_DEFEATS[symbol]] > 0:
            #     value -= 0.1


    game_board.split_token_symbols()
    heuristic_dist = []


    # Evaluate heuristic distance and actual distance of opponents 
    for my_data in game_board.data[game_board.me]:
        my_token = Token(my_data, game_board.me)
        op_defeat_data = game_board.op_tokens[my_token.defeats]

        for op_data in op_defeat_data:
            op_token = Token(op_data, game_board.opponent)

            h_dist = heuristic(my_token, op_token)
            heuristic_dist.append(h_dist)
        
    if heuristic_dist != []:
        min_dist = min(heuristic_dist)
        value += 1/(min_dist+1)      
        


    return value
