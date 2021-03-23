import sys
from search.util import print_board, print_slide, print_swing
from search.Token import Token
from search.GameBoard import GameBoard

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
    
    while len(lower_tokens) > 0 and turn <= 360:

        # TODO tokens need to talk to each other
        upper_tokens = do_tokens_turn(turn, game_board, upper_tokens, lower_tokens)

        new_data = {"upper": upper_tokens, "lower": lower_tokens, "block": block_tokens}

        game_board = GameBoard(new_data)
        game_board.print()

        turn += 1

def do_tokens_turn(turn, game_board, upper_tokens, lower_tokens):
    new_upper_tokens = []

    for upper in upper_tokens:
        upper_token = Token(upper, True)
        
        new_upper_token, defeated_tokens = do_token_turn(turn, upper_token, game_board.upper_defeats[upper_token.symbol], game_board)

        if new_upper_token != None:
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
            # Tim's heuristic test
            # print("heuristic distance to", (lower_token), heuristic(upper_token, l_token))
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
            while num_tokens > 0:
                defeated_tokens.append(min_lower_token)
                num_tokens -= 1
        
        # Check if upper token will be defeated

    else:
        # TODO Find other hexes to swing move
        # Get viable moves and move there
        viable_actions = upper_token.viable_actions(game_board, 1)
        # commit suicide if no viable moves
        if len(viable_actions) == 0:
            for hex in upper_token.neighbours():
                defeated_by_token = [upper_token.defeated_by] + hex
                hex_tokens = ""

                if tuple(hex) in game_board.board_dict:
                    hex_tokens = game_board.board_dict[tuple(hex)]

                if defeated_by_token in game_board.upper_occupied_hexes or \
                   upper_token.defeated_by in hex_tokens:

                    new_hex = hex
                    upper_token.set_defeat(True)

        else:
            new_hex = viable_actions[0]

    upper_token.do_action(turn, new_hex)
    game_board.upper_occupied_hexes.append( [upper_token.symbol] + new_hex)

    return upper_token.convert_to_list(), defeated_tokens

def bfs(game_board, upper_token, lower_token):

    queue = []
    queue.append(upper_token)
    flood = {}    
    next_action = True

    while len(queue) > 0:
        current = queue.pop()
        
        if current.r == lower_token.r and current.q == lower_token.q:
            break
        
        viable_actions = current.viable_actions(game_board, next_action)

        # Token is trapped so stay in place
        # Token should always be able to move
        # Token will need to be defeated if it can't move / defeat another token
        if len(viable_actions) == 0 and next_action:
            return 0, [(upper_token.r, upper_token.q)]
        else:
            for next in viable_actions:
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
