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