from classes.Token import Token

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


'''
    Find all viable moves
    try sorting to maximise pruning
    return state (game_board)
'''
def actions(state, my_action):
    next_states = []

    if my_action:
        tokens = state.data[state.me]
        token_type = state.me # lower
    else: 
        tokens = state.data[state.opponent]
        token_type = state.opponent

    # Slide and Swing moves
    for token in tokens:
        player = Token(token, token_type == "upper")
        player_actions = player.viable_actions(state, True)

        for player_action in player_actions:
                new_state = state.apply_action(player, player_action, my_action)
                next_states.append( [new_state, player, player_action])

    # Throw moves
    if state.tokens_in_hand[token_type] > 0:
        for hex in throwable_hexes(state, token_type):
            for token in ["r", "p", "s"]:
                player = Token([token, None, None], token_type == "upper")

                new_state = state.apply_action(player, hex, my_action)
                next_states.append( [new_state, player, hex])           

    # sort for perfect ordering
    # next_states.sort(key=lambda x: x[0].eval(), reverse= my_action)

    return next_states



'''
Returns a list of tuples of all the hexes a player can throw to
'''
def throwable_hexes(game_board, player):

    # Flip board if lower
    if player == "upper":
        flip = 1
    else:
        flip = -1

    short_range = flip * (game_board.tokens_in_hand[player] - 5)

    if flip == 1:
        throw_ran = range(short_range, (4+1))
    else:
        throw_ran = range(-4, short_range + 1)
    ran = range(-4, 4+1)
    return [(r,q) for r in throw_ran for q in ran if r+q in ran]


def throwable_row_range(game_board, player):
    # Flip board if lower
    if player == "upper":
        flip = 1
    else:
        flip = -1

    short_range = flip * (game_board.tokens_in_hand[player] - 5)

    if flip == 1:
        throw_ran = range(short_range, (4+1))
    else:
        throw_ran = range(-4, short_range + 1)
    
    return [*throw_ran]
