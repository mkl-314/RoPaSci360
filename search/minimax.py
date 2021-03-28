

def minimax_decision(game_board):

    value = {}

    for op in Operators[game_board]:
        value[op] = minimax_value(Apply(op, game_board), game_board)

    return max(value, key=value.get())


def minimax_value(state, game_board):
    if state.turn - game_board.turn > 2:
        return 0.5


def max_value(state, game, a, b):
    if state.turn - game.turn > 2:
        return eval(state)
    
    for s in successors(state):
        a = max(a, min_value(s, game, a, b))
        if a >= b:
            return b
    
    return a

def max_value(state, game, a, b):
    if state.turn - game.turn > 2:
        return eval(state)
    
    for s in successors(state):
        b = min(a, max_value(s, game, a, b))
        if a >= b:
            return a
    
    return b

def successors(state):
    # Find all viable moves
    # try sorting to maximise pruning
    # return state 

def eval(state):
    # Evaluate the value that the state has
    # count my tokens to their tokens + positioning + location
    pass