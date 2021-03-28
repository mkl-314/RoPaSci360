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
    turn = 1
    
    while len(game_board.data["lower"]) > 0 and turn <= 360:

        # TODO tokens need to talk to each other
        upper_tokens = do_tokens_turn(turn, game_board)

        new_data = {"upper": upper_tokens, "lower": game_board.data["lower"], "block": game_board.data["block"]}

        game_board = GameBoard(new_data)
        game_board.print()

        turn += 1 

def do_tokens_turn(turn, game_board):
    new_upper_tokens = []
    upper_tokens = game_board.data["upper"]

    for upper in upper_tokens:
        upper_token = Token(upper, True)
        
        new_upper_token = do_token_turn(turn, upper_token, game_board)

        new_upper_tokens.append(new_upper_token)


    return new_upper_tokens

def do_token_turn(turn, upper_token, game_board):
    lower_tokens = game_board.lower_tokens[upper_token.defeats]

    if len(lower_tokens) > 0:
        new_hex = closest_lower_token_path(game_board, upper_token, lower_tokens)
    else:
        viable_actions = upper_token.viable_actions(game_board, True)

        if len(viable_actions) == 0:
        # Token must be defeated if no viable moves
            new_hex = token_defeat(upper_token, game_board)
        else:
            new_hex = closest_lower_token_path(game_board, upper_token, game_board.data["lower"], avoid_token=True)


    upper_token.do_action(turn, new_hex)
    game_board.upper_occupied_hexes.append( [upper_token.symbol] + new_hex)

    return upper_token.convert_to_list()

# Finds the path to the closest lower_token and returns the next move
def closest_lower_token_path(game_board, upper_token, lower_tokens, avoid_token=False):
    min_distance = -1
    for lower_token in lower_tokens:
        l_token = Token(lower_token, False)
        # Tim's heuristic test
        # print("heuristic distance to", (lower_token), heuristic(upper_token, l_token))
        if avoid_token:
            viable_actions = upper_token.viable_actions(game_board, True)
            if [l_token.r, l_token.q] in viable_actions: 
                if len(viable_actions) > 1:
                    viable_actions.remove([l_token.r, l_token.q])
                    for action in viable_actions:
                        if heuristic(Token([upper_token.symbol] + action, True), l_token) == 1:
                            return action
                
                return viable_actions[0]

        distance, path = bfs(game_board, upper_token, l_token)

        if distance < min_distance or min_distance == -1:
            num_tokens = 1
            min_distance = distance
            min_lower_token = lower_token
            new_hex = list(path[0])
        # note two of the same tokens on one hex
        elif min_lower_token == lower_token:
            num_tokens += 1

    return new_hex

# Finds hex which token will be defeated on
def token_defeat(upper_token, game_board):
    for hex in upper_token.neighbours():
        defeated_by_token = [upper_token.defeated_by] + hex
        hex_tokens = ""

        if tuple(hex) in game_board.board_dict:
            hex_tokens = game_board.board_dict[tuple(hex)]

        if defeated_by_token in game_board.upper_occupied_hexes or \
            upper_token.defeated_by in hex_tokens:
            return hex


def bfs(game_board, upper_token, lower_token):

    queue = []
    queue.append(upper_token)
    flood = {(upper_token.r, upper_token.q): (upper_token.r, upper_token.q)}    
    next_action = True
    avoid_curr = None

    while len(queue) > 0:
        current = queue.pop()
        
        # Avoids path that is blocked by lower token, unless it's the only move
        if (current.r, current.q) in game_board.board_dict:
            if upper_token.defeated_by in game_board.board_dict[(current.r, current.q)] and len(queue) > 0:
                avoid_curr = current
                continue

        if current.r == lower_token.r and current.q == lower_token.q:
            break
        
        viable_actions = current.viable_actions(game_board, next_action)

        # Token is trapped so stay in place
        # Token should always be able to move
        # Token will need to be defeated if it can't move / defeat another token
        if len(viable_actions) == 0 and next_action:
            return 0, [token_defeat(upper_token, game_board)]
        else:
            for next in viable_actions:
                if tuple(next) not in flood:

                    next_token = Token([current.symbol] + next, True)
                    queue.insert(0, next_token)
                    flood[tuple(next)] = (current.r, current.q)
        
        if len(queue) == 0 and avoid_curr != None:
            queue.insert(0, avoid_curr)
            avoid_curr = None

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