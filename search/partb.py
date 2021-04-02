import sys
from util import print_board, print_slide, print_swing
from Token import Token
from GameBoard import GameBoard
from AllTokens import AllTokens
from moves.throw_move import *
from minimax import *

'''
bfs function derived from
https://www.redblobgames.com/pathfinding/a-star/introduction.html
'''

def get_input():

    data = {"lower": [], "upper": [], "block": []}

    turn = 1

    # assume ai is Upper
    while turn <= 360:

        # Formats: ("Throw", "p", (0, 0))
        # ("Slide", (0, 0), (0, 1))

        # Simple Formats for testing: ("Throw", "p", 0, 0)
        # ("Slide", 0, 0, 0, 1)
        next_move = input("Input turn:")

        data = do_upper_move(data, turn)
        lower_move(data, next_move)

        print("Turn: " + str(turn))
        game_board = GameBoard(data, turn)
        game_board.print()
        turn += 1

def lower_move(data, next_move):

    try:
        # Formats: ("Throw", "p", (0, 0))
        # ("Slide", (0, 0), (0, 1))

        # Simple Formats for testing: ("Throw", "p", 0, 0)
        # ("Slide", 0, 0, 0, 1)
        #next_move = input("Input turn:")
        lst_next_move = next_move.strip("][)(").split(", ")


        if lst_next_move[0] == "THROW":
            token = [lst_next_move[1], int(lst_next_move[2]), int(lst_next_move[3])]
            data["lower"].append(token)
            #data["lower"] += [lst_next_move[1], int(lst_next_move[2].strip("(")), int(lst_next_move[3].strip(")"))]
        elif lst_next_move[0] == "SLIDE" or lst_next_move[0] == "SWING":
            found_token = False
            for old_token in data["lower"]:
                token_pos = [int(lst_next_move[1]), int(lst_next_move[2])]
                if token_pos == old_token[1:3]:
                    old_token[1:3] = [int(lst_next_move[3]), int(lst_next_move[4])]
                    found_token = True
                    break
                    # check that the token gets updated
            if not found_token:
                raise ValueError("Print correct format")

        return data
    except:
        print("Print correct format as seen in function lower_move")
        next_move = input("Input turn:")
        lower_move(data, next_move)

def do_upper_move(data, turn):
    game_board = GameBoard(data, turn)

    all_tokens = AllTokens()

    # Find potential paths to token 
    # Throw move
    #hexes = throwable_hexes()
    
    hexes = throwable_hexes()

    if turn <=2:
        # Do throw move  
        symbol = all_tokens.upper_tokens_in_hand.pop()
        
        #upper_tokens.append([symbol] + hexes[0])
        game_board = game_board.apply_action(Token([symbol] + hexes[0], True), None)
    else:
        move = minimax_manager(game_board)
        game_board = game_board.apply_action(move[0], move[1])
        move[0].do_action(turn, move[1])

    return game_board.data


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
            for i in range(num_tokens):
                defeated_tokens.append(min_lower_token)
    else:
        # TODO Find other hexes to swing move
        # Get viable moves and move there
        viable_actions = upper_token.viable_actions(game_board, 1)
        new_hex = viable_actions[0]

    upper_token.do_action(turn, new_hex)
    game_board.upper_occupied_hexes.append(new_hex)

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
