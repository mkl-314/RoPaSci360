from util import print_slide, print_swing
import math

class Token(object):
    BLOCK = "#"
    possible_neighbours = [ [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0] ]
    token_defeats = ["r", "s", "p"]
    
    def __init__ (self, symbol, upper_player):
        self.symbol = symbol
        self.defeated_by = self.token_defeats[self.token_defeats.index(self.symbol)-1]
        self.defeats = self.token_defeats[self.token_defeats.index(self.symbol)-2]
        self.pos = None  # (r, q)
        self.upper_player = upper_player
        self.defeated = False

    def __eq__ (self, other):
        if isinstance(other, Token):
            return self.r == other.r and self.q == other.q \
            and self.symbol == other.symbol and self.upper_player == other.upper_player

    # Refactor to return ALL viable moves, regardless of how bad they are
    def viable_actions(self, game_board, next_action):

        # slide move
        viable_hexes, swing_hexes = self.get_viable_hexes(self, game_board, next_action)

        # swing move
        # only consider swing moves if next action because tokens move
        if next_action:    
            for hex in swing_hexes:
                # create temp token from swing hex
                temp_token = Token([self.symbol] + hex, self.upper_player)

                viable_hexes_1 = self.get_viable_hexes(temp_token, game_board, next_action)
                viable_hexes += viable_hexes_1[0]

        return viable_hexes

    def get_viable_hexes(self, token, game_board, next_action):
        viable_hexes = []
        swing_hexes = []
        only_hex = []

        for hex in token.neighbours():

            defeated_by_token = [token.defeated_by] + hex
            defeats_token = [token.defeats] + hex
            # check if another Upper token is moving to this hex and if it can be defeated by this token
            if next_action and \
            ( 
                defeated_by_token in game_board.upper_occupied_hexes or \
                (defeats_token in game_board.upper_occupied_hexes and 
                len(game_board.lower_tokens[token.defeated_by] ) > 0)
            ):
                # upper token cannot be defeated
                continue
            else:
                if [token.symbol] + hex in game_board.upper_occupied_hexes:
                    only_hex = hex
                    continue

                # check if block or oppoenent is in hex
                if tuple(hex) in game_board.board_dict:
                    hex_tokens = game_board.board_dict[tuple(hex)]
                    if self.BLOCK not in hex_tokens:
                        if not next_action or token.defeated_by not in hex_tokens:
                            viable_hexes.append(hex)
                    
                        if next_action and self == token:
                            if not hex_tokens.islower():
                                swing_hexes.append(hex)
                # empty hex
                else:
                    viable_hexes.append(hex)

        if len(viable_hexes) == 0 and only_hex != []:
            viable_hexes.append(only_hex)
            
        return viable_hexes, swing_hexes

    def do_action(self, turn, new_hex):
        
        if self.is_adjacent_hex(new_hex):
            print_slide(turn, self.r, self.q, new_hex[0], new_hex[1])
        else:
            print_swing(turn, self.r, self.q, new_hex[0], new_hex[1])

        self.update(new_hex)
        

    def is_adjacent_hex(self, new_hex):
        return new_hex in self.neighbours() or new_hex == [self.r, self.q]

    def neighbours(self):
        list_neighbours = []
        for [r_add, q_add] in self.possible_neighbours:
            ran = range(-4, 4+1)
            new_r = self.r + r_add
            new_q = self.q + q_add
            # Ensure the hex is on the board
            if new_r in ran and new_q in ran and new_r + new_q in ran:
                list_neighbours.append([new_r, self.q + q_add])

        return list_neighbours

    def update(self, new_upper_token):
        self.r = new_upper_token[0]
        self.q = new_upper_token[1]

    def convert_to_list(self):
        return [ self.symbol, self.r, self. q]