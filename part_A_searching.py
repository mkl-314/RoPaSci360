import sys
from util import print_board, print_slide, print_swing

def format_file(data):
    board_dict = {}
    for (token, positions) in data.items():
        for pos in positions:
            if token == "upper":
                board_dict[( pos[1], pos[2])] = pos[0].upper()
            elif token == "lower":
                board_dict[( pos[1], pos[2])] = pos[0].lower()
            else:
                board_dict[( pos[1], pos[2])] = "B"
            
    return board_dict

def do_turns(data):
    lower_tokens = data["lower"]
    upper_tokens = data["upper"]
    block_tokens = data["block"]
    
    turn = 1
    
    while len(lower_tokens) > 0 and turn <= 360:

        r_lower_tokens, p_lower_tokens, s_lower_tokens = separate_tokens(lower_tokens) 
        r_upper_tokens, p_upper_tokens, s_upper_tokens = separate_tokens(upper_tokens)

        new_upper_tokens = []
        
        new_r_upper_tokens, s_defeated_tokens = do_tokens_turn(turn, r_upper_tokens, s_lower_tokens)
        new_p_upper_tokens, r_defeated_tokens = do_tokens_turn(turn, p_upper_tokens, r_lower_tokens)
        new_s_upper_tokens, p_defeated_tokens = do_tokens_turn(turn, s_upper_tokens, p_lower_tokens)

        new_upper_tokens = new_r_upper_tokens + new_p_upper_tokens + new_s_upper_tokens
        defeated_tokens = s_defeated_tokens + r_defeated_tokens + p_defeated_tokens

        for defeated_token in defeated_tokens:
            lower_tokens.remove(defeated_token)

        turn += 1
        upper_tokens = new_upper_tokens 

        new_data = {}
        new_data["upper"] = upper_tokens
        new_data["lower"] = lower_tokens
        new_data["block"] = block_tokens
        board_dict = format_file(new_data)
        print_board(board_dict)

def do_tokens_turn(turn, upper_tokens, lower_tokens):
    new_upper_tokens = []
    defeated_token_pos = []

    for upper_token in upper_tokens:
        if len(lower_tokens) > 0:
            min_distance = -1
            for lower_token in lower_tokens:
                distance, next_hex = bfs(upper_token, lower_token)
                if distance < min_distance or min_distance == -1:
                    num_tokens = 1
                    min_distance = distance
                    min_lower_token = lower_token
                    min_next_hex = next_hex
                # note two of the same tokens on one hex
                elif min_lower_token == lower_token:
                    num_tokens += 1
            
            do_action(turn, upper_token, min_next_hex)
            new_upper_tokens.append(min_next_hex)

            # Remove all deleted tokens
            if min_next_hex[1:] == min_lower_token[1:]:
                for i in range(num_tokens):
                    #defeated_token_pos = []
                    defeated_token_pos.append(min_lower_token)
        else:
            new_upper_tokens.append(upper_token)

    return new_upper_tokens, defeated_token_pos




def separate_tokens(tokens):
    r_tokens = []
    p_tokens = []
    s_tokens= []

    for token in tokens:
        if token[0] == "r":
            r_tokens.append(token)
        elif token[0] == "p":
            p_tokens.append()
        elif token[0] == "s":
            s_tokens.append(token)  
    
    return r_tokens, p_tokens, s_tokens

def bfs(upper_token, lower_token):
    new_hex = upper_token.copy()

    if upper_token[1] < lower_token[1]:
        new_hex[1] += 1
    elif upper_token[1] > lower_token[1]:
        new_hex[1] -= 1
    elif upper_token[2] < lower_token[2]:
        new_hex[2] += 1 
    elif upper_token[2] > lower_token[2]:
        new_hex[2] -= 1

    return 4, new_hex

def do_action(turn, upper_token, new_upper_token):

    if is_hex_next_to():
        print_slide(turn, upper_token[1], upper_token[2], new_upper_token[1], new_upper_token[2])
    else:
        print_swing(turn, upper_token[1], upper_token[2], new_upper_token[1], new_upper_token[2])

def is_hex_next_to():
    return True

def adjacent_hexes(token):
    pass


def viable_moves(token):
    pass