import sys
from util import print_board, print_slide, print_swing
from Token import Token
from GameBoard import GameBoard

'''
bfs function derived from
https://www.redblobgames.com/pathfinding/a-star/introduction.html
'''


def do_turns(data):
    game_board = GameBoard(data)

    game_board.print()

    lower_tokens = data["lower"]
    upper_tokens = data["upper"]
    block_tokens = data["block"]
    
    turn = 1
    
    while len(lower_tokens) > 0 and turn <= 20:

        r_lower_tokens, p_lower_tokens, s_lower_tokens = separate_tokens(lower_tokens) 
        r_upper_tokens, p_upper_tokens, s_upper_tokens = separate_tokens(upper_tokens)

        new_upper_tokens = []
        
        new_r_upper_tokens, s_defeated_tokens = do_tokens_turn(turn, game_board, r_upper_tokens, s_lower_tokens)
        new_p_upper_tokens, r_defeated_tokens = do_tokens_turn(turn, game_board, p_upper_tokens, r_lower_tokens)
        new_s_upper_tokens, p_defeated_tokens = do_tokens_turn(turn, game_board, s_upper_tokens, p_lower_tokens)

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

        game_board = GameBoard(new_data)
        game_board.print()

def do_tokens_turn(turn, game_board, upper_tokens, lower_tokens):
    new_upper_tokens = []
    defeated_token_pos = []

    for upper_token in upper_tokens:
        u_token = Token(upper_token, True)
        if len(lower_tokens) > 0:
            min_distance = -1
            for lower_token in lower_tokens:
                l_token = Token(lower_token, False)
                distance, next_hex = bfs(game_board, u_token, l_token)

                if distance < min_distance or min_distance == -1:
                    num_tokens = 1
                    min_distance = distance
                    min_lower_token = lower_token
                    min_next_hex = next_hex
                # note two of the same tokens on one hex
                elif min_lower_token == lower_token:
                    num_tokens += 1
            
            u_token.do_action(turn, min_next_hex)

            new_upper_tokens.append(u_token.convert_to_list())

            # Remove all deleted tokens
            if min_next_hex == min_lower_token[1:]:
                for i in range(num_tokens):
                    defeated_token_pos.append(min_lower_token)
        else:
            u_token.do_action(turn, [u_token.r, u_token.q])
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
            p_tokens.append(token)
        elif token[0] == "s":
            s_tokens.append(token)  
    
    return r_tokens, p_tokens, s_tokens

def bfs(game_board, upper_token, lower_token):

    queue = []
    queue.append(upper_token)
    flood = {}    

    while len(queue) > 0:
        current = queue.pop()
        
        if current.r == lower_token.r and current.q == lower_token.q:
            break

        for next in current.viable_actions(game_board):
            if not tuple(next) in flood:

                next_token = Token([current.symbol] + next, True)
                queue.insert(0, next_token)
                flood[tuple(next)] = (current.r, current.q)
            
    distance = 0
    path = []

    current_hex = (current.r, current.q)

    while current_hex != (upper_token.r, upper_token.q):
        path.append(current_hex)
        current_hex = flood[current_hex]
        distance += 1
        
    return distance, list(path[-1])


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