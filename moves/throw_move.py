def throw_move():
    pass


def throwable_hexes(game_board):

    # Flip board if lower
    if game_board.me == "upper":
        flip = 1
    else:
        flip = -1

    short_range = flip * (game_board.tokens_in_hand[game_board.me] - 5)

    if flip == 1:
        throw_ran = range(short_range, (4+1))
    else:
        throw_ran = range(-4, short_range + 1)
    ran = range(-4, 4+1)
    return [(r,q) for r in throw_ran for q in ran if r+q in ran]