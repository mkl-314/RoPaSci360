from util import *
import math

class Token(object):
    possible_neighbours = [ [-1, 0], [-1, 1], [0, -1], [0, 1], [1, -1], [1, 0] ]
    token_defeats = ["r", "s", "p"]

    def __init__ (self, token, upper_player):
        self.symbol = token[0]
        self.r = token[1]
        self.q = token[2]
        self.upper_player = upper_player

    def __eq__ (self, other):
        if isinstance(other, Token):
            return self.r == other.r and self.q == other.q \
            and self.symbol == other.symbol and self.upper_player == other.upper_player

    def viable_actions(self, game_board):

        # slide move
        viable_hexes, swing_hexes = self.get_viable_hexes(self, game_board, True)
            
        # swing move
        for hex in swing_hexes:
            # create temp token from swing hex
            temp_token = Token([self.symbol] + hex, self.upper_player)

            viable_hexes_1, empty_list = self.get_viable_hexes(temp_token, game_board, False)
            viable_hexes += viable_hexes_1

        return viable_hexes

    def get_viable_hexes(self, token, game_board, swing):
        viable_hexes = []
        swing_hexes = []
        for hex in token.neighbours():
            # check is block or oppoenent is in block
            if tuple(hex) in game_board.board_dict:
                hex_tokens = game_board.board_dict[tuple(hex)]
                if "#" not in hex_tokens:
                    if token.token_defeats[token.token_defeats.index(token.symbol)-1] not in hex_tokens:
                        viable_hexes.append(hex)
                
                    if swing:
                        if not hex_tokens.islower():
                            swing_hexes.append(hex)
            else:
                viable_hexes.append(hex)

        return viable_hexes, swing_hexes

    def do_action(self, turn, new_upper_token):
        
        if self.is_adjacent_hex(new_upper_token):
            print_slide(turn, self.r, self.q, new_upper_token[0], new_upper_token[1])
        else:
            print_swing(turn, self.r, self.q, new_upper_token[0], new_upper_token[1])

        self.update(new_upper_token)
        

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