from classes.Token import Token
from moves.throw_move import throwable_hexes
from math import inf

CUT_OFF_LIMIT = 1


def minimax_manager(game):
    #value = max_value(game, game, -inf, inf)

    value, move = max_value(game, game, -inf, inf)
    return move

def max_value(state, game, a, b):
    if state.turn - game.turn >= CUT_OFF_LIMIT:
        return state.eval(), None

    val = -inf 
    for s in actions(state, True):
        a_temp, move2 = min_value(s[0], game, a, b)

        if a_temp > val:
            val, move = a_temp, s[1:3]
            a = max(val, a)

        if val >= b:
            return val, move 
    
    return val, move

'''
return value, action

'''
def min_value(state, game, a, b):
    if state.turn - game.turn >= CUT_OFF_LIMIT:
        return state.eval(), None
    
    val = inf 
    for s in actions(state, False):
        b_temp, move2 = max_value(s[0], game, a, b)

        if b_temp < val:
            val, move = b_temp, s[1:3]
            b = min(val, b)

        if val >= a:
            return val, move 

    return val, move

'''
    Find all viable moves
    try sorting to maximise pruning
    return state (game_board)
'''
def actions(state, max_val):
    next_states = []

    if max_val:
        tokens = state.data[state.me]
        token_type = state.me
    else: 
        tokens = state.data[state.opponent]
        token_type = state.opponent

    # TODO Throw moves
    for hex in throwable_hexes(state):
        for token in set(state.tokens_in_hand[token_type]):
            player = Token([token, None, None], token_type == "upper")

            new_state = state.apply_action(player, hex)
            next_states.append( [new_state, player, hex])

    # Slide and Swing moves
    for token in tokens:
        player = Token(token, token_type == "upper")
        player_actions = player.viable_actions(state, True)

        for player_action in player_actions:
                new_state = state.apply_action(player, player_action)
                next_states.append( [new_state, player, player_action])

    # player_tokens = state.data[state.player]
    # opponent_tokens = state.data[state.opponent]

    # TODO Throw moves

    # Slide and Swing Moves
    # for player_token in player_tokens:
    #     for opponent_token in opponent_tokens:
    #         player = Token(player_token, state.player == "upper")
    #         opponent = Token(opponent_token, state.opponent == "upper")
    #         player_actions = player.viable_actions(state, True)
    #         opponent_actions = opponent.viable_actions(state, True)

    #         for player_action in player_actions:
    #             for opponent_action in opponent_actions:
    #                 new_state = state.apply_action(player, player_action)
    #                 new_state = new_state.apply_action(opponent, opponent_action)
    #                 next_states.append( [new_state, player, player_action])


    # sort for perfect ordering
    next_states.sort(key=lambda x: x[0].eval(), reverse=max_val)

    return next_states


