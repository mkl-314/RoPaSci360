from AllTokens import AllTokens

def throw_move():
    all_tokens = AllTokens()
    # Do throw move  
    symbol = all_tokens.upper_tokens_in_hand.pop()
    offset = 5
    #upper_tokens.append([symbol, offset - turn, -2])
    return


def throwable_hexes():
    all_tokens = AllTokens()

    lower_range = len(all_tokens.upper_tokens_in_hand) - 5
    throw_ran = range(lower_range, 4+1)
    ran = range(-4, 4+1)
    return [(r,q) for r in throw_ran for q in ran if r+q in ran]