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

        # TODO tokens need to talk to each other
        upper_tokens = do_tokens_turn(turn, game_board, upper_tokens, lower_tokens)

        new_data = {}
        new_data["upper"] = upper_tokens
        new_data["lower"] = lower_tokens
        new_data["block"] = block_tokens

        game_board = GameBoard(new_data)
        game_board.print()

        turn += 1

def do_tokens_turn(turn, game_board, upper_tokens, lower_tokens):
    new_upper_tokens = []

    r_lower_tokens, p_lower_tokens, s_lower_tokens = separate_tokens(lower_tokens) 
    upper_defeats = {"r": s_lower_tokens, "s": p_lower_tokens, "p": r_lower_tokens}

    for upper in upper_tokens:
        upper_token = Token(upper, True)
        
        new_upper_token, defeated_tokens = do_token_turn(turn, upper_token, upper_defeats[upper_token.symbol], game_board)

        new_upper_tokens.append(new_upper_token)

        for defeated_token in defeated_tokens:
            lower_tokens.remove(defeated_token)

    return new_upper_tokens

def do_token_turn(turn, upper_token, lower_tokens, game_board):
    defeated_tokens = []

    if len(lower_tokens) > 0:
        min_distance = -1
        for lower_token in lower_tokens:
            l_token = Token(lower_token, False)
            distance, path = bfs(game_board, upper_token, l_token)

            if distance < min_distance or min_distance == -1:
                num_tokens = 1
                min_distance = distance
                min_lower_token = lower_token
                new_hex = list(path[0])
            # note two of the same tokens on one hex
            elif min_lower_token == lower_token:
                num_tokens += 1

        # Remove all deleted tokens
        if new_hex == min_lower_token[1:]:
            for i in range(num_tokens):
                defeated_tokens.append(min_lower_token)
    else:
        # TODO Find other hexes to swing move
        new_hex = [upper_token.r, upper_token.q]

    upper_token.do_action(turn, new_hex)
    game_board.upper_occupied_hexes.append(new_hex)

    return upper_token.convert_to_list(), defeated_tokens

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
    next_action = True

    while len(queue) > 0:
        current = queue.pop()
        
        if current.r == lower_token.r and current.q == lower_token.q:
            break

        for next in current.viable_actions(game_board, next_action):
            if tuple(next) not in flood:

                next_token = Token([current.symbol] + next, True)
                queue.insert(0, next_token)
                flood[tuple(next)] = (current.r, current.q)
        
        next_action = False
            
    distance = 0
    path = []
    current_hex = (current.r, current.q)

    while current_hex != (upper_token.r, upper_token.q):
        path.append(current_hex)
        current_hex = flood[current_hex]
        distance += 1
    path.reverse()

    return distance, path


