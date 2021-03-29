from Token import Token
from math import inf

CUT_OFF_LIMIT = 1

# def minimax_decision(game_board):

#     value = {}

#     for op in Operators[game_board]:
#         value[op] = minimax_value(Apply(op, game_board), game_board)

#     return max(value, key=value.get())


# def minimax_value(state, game_board):
#     if state.turn - game_board.turn > CUT_OFF_LIMIT:
#         return 0.5

def minimax_manager(game):
    #value = max_value(game, game, -inf, inf)

    value, move = max_value(game, game, -inf, inf)

    return move

def max_value(state, game, a, b):
    if state.turn - game.turn >= CUT_OFF_LIMIT:
        return state.eval(), None
    
    # for s in successors(state, True):
    #     a = max(a, min_value(s, game, a, b))
    #     if a >= b:
    #         return b
    
    # return a

    val = -inf 
    for s in actions(state, True):
        a_temp, move2 = min_value(s[0], game, a, b)

        if a_temp > val:
            val, move = a_temp, s[1:3]
            a = max(val, a)

        if val <= a:
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
    # for s in successors(state, False):
    #     b = min(b, max_value(s, game, a, b))
    #     if a >= b:
    #         return a
    

def actions(state, max):
    next_states = []

    upper_tokens = state.data["upper"]
    lower_tokens = state.data["lower"]

    # TODO Throw moves

    # Slide and Swing Moves
    for upper_token in upper_tokens:
        for lower_token in lower_tokens:
            upper = Token(upper_token, True)
            lower = Token(lower_token, False)
            upper_actions = upper.viable_actions(state, True)
            lower_actions = lower.viable_actions(state, True)

            for upper_action in upper_actions:
                for lower_action in lower_actions:
                    new_state = state.apply_action(upper, upper_action)
                    new_state = new_state.apply_action(lower, lower_action)
                    next_states.append( [new_state, upper, upper_action])

    # sort for perfect ordering
    next_states.sort(key=lambda x: x[0].eval(), reverse=max)

    return next_states

'''
    Find all viable moves
    try sorting to maximise pruning
    return state (game_board)
'''
def successors(state, max):
    next_states = []

    upper_tokens = state.data["upper"]
    lower_tokens = state.data["lower"]

    # TODO Throw moves

    # Slide and Swing Moves
    for upper_token in upper_tokens:
        for lower_token in lower_tokens:
            upper = Token(upper_token, True)
            lower = Token(lower_token, False)
            upper_actions = upper.viable_actions(state, True)
            lower_actions = lower.viable_actions(state, True)

            for upper_action in upper_actions:
                for lower_action in lower_actions:
                    new_state = state.apply_action(upper, upper_action)
                    new_state = new_state.apply_action(lower, lower_action)
                    next_states.append(new_state)

    # sort for perfect ordering
    next_states.sort(key=lambda x: x.eval(), reverse=max)

    return next_states
