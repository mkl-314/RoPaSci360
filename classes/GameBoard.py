#from util import print_board
import re
import copy
#from ai.path_searching import eval
import random

class GameBoard(object):
    token_defeats = ["r", "s", "p"]

    def __init__(self, player):
        self.turn = 1
        self.me = player
        self.opponent = "lower" if self.me == "upper" else "upper"
        self.board_dict = {}
        self.data = {"upper": [], "lower": []} 
        self.tokens_in_hand = {"upper": 9, "lower": 9} 
        self.ignore_token = None
    
    def __eq__(self, gameboard):
        return self.tokens_in_hand == gameboard.tokens_in_hand and self.data == gameboard.data

    def possible_same_state(self, gameboard):
        return self.tokens_in_hand == gameboard.tokens_in_hand and \
            len(self.data["upper"]) == len(gameboard.data["upper"]) and \
                len(self.data["lower"]) == len(gameboard.data["lower"])

    # formats gameboard data by hex
    def update_board(self, data):
        board_dict = {}
        for (token, positions) in data.items():
            for pos in positions:
                hex = (pos[1], pos[2])
                if not hex in board_dict:
                    board_dict[hex] = ""
                    
                if token == "upper":
                    board_dict[hex] += pos[0].upper()
                elif token == "lower":
                    board_dict[hex] += pos[0].lower()
        
        #board_dict = self.delete_defeated_tokens(board_dict)
        return board_dict

    # updates board_dict with battle outcomes
    def delete_defeated_tokens(self, my_move=None, opponent_move=None):
        possible_hex_defeats = []

        if my_move != None:
            possible_hex_defeats += [(my_move, self.board_dict[my_move])]
        if opponent_move != None:
            possible_hex_defeats += [(opponent_move, self.board_dict[opponent_move])]

        for (hex, symbols) in possible_hex_defeats:
            if "r" in symbols.lower() and "p" in symbols.lower() and "s" in symbols.lower():
                self.board_dict[hex] = ""
            else:
                for i in range(3):
                    if self.token_defeats[i] in symbols.lower() and self.token_defeats[i-1] in symbols.lower():
                        self.board_dict[hex] = re.sub(self.token_defeats[i], "", self.board_dict[hex], flags=re.IGNORECASE)
        return None

    # Formats board by the token type
    def convert_to_data(self, board_dict):
        data = {"upper": [], "lower": []}

        for (hex, symbols) in board_dict.items():
            for symbol in symbols:
                if symbol.isupper():
                    data["upper"].append([symbol.lower(), hex[0], hex[1] ])
                elif symbol.islower():
                    data["lower"].append([symbol, hex[0], hex[1] ])
        return data

    def apply_action(self, token, action, my_action):

        new_game_board = copy.deepcopy(self)
        
        if token.r == None:
            # Throw move
            throw_move =  ("THROW", token.symbol, (action[0], action[1]))
            if my_action:
                new_game_board.update( throw_move, None)
            else:
                new_game_board.update( None, throw_move)
        else:
            # Slide and Swing moves
            non_throw_move = ("NOT_THROW", (token.r, token.q), (action[0], action[1]))
            if my_action:
                new_game_board.update( non_throw_move, None)
            else:
                new_game_board.update( None, non_throw_move)

        return new_game_board

    # Update game board state 
    def update(self, my_action, opponent_action):
        self.turn += 1

        self.update_token(self.me, my_action)
        self.update_token(self.opponent, opponent_action)

        self.board_dict = self.update_board(self.data)

        if my_action == None:
            self.delete_defeated_tokens(opponent_move= opponent_action[2])
        elif opponent_action == None:
            self.delete_defeated_tokens(my_move = my_action[2])
        else:
            self.delete_defeated_tokens(my_action[2], opponent_action[2])

        self.data = self.convert_to_data(self.board_dict)

        return copy.deepcopy(self)

    def update_copy(self, my_action, opponent_action):
        new_game_board = copy.deepcopy(self)
        new_game_board.update(my_action, opponent_action)
        return new_game_board




    # Updates the token position
    def update_token(self, player, player_action):

        if player_action != None:
            if player_action[0] == "THROW":
                self.data[player].append([player_action[1]] + list(player_action[2]))
                self.tokens_in_hand[player] -= 1
            else:
                for upper in self.data[player]:
                    if upper[1:3] == list(player_action[1]):
                        upper[1:3] = list(player_action[2])
                        break

    def split_token_symbols(self):
        self.my_tokens = {}
        self.op_tokens = {}
        self.my_tokens["r"], self.my_tokens["p"], self.my_tokens["s"] = self.separate_tokens(self.data[self.me]) 
        self.op_tokens["r"], self.op_tokens["p"], self.op_tokens["s"] = self.separate_tokens(self.data[self.opponent]) 


    def separate_tokens(self, tokens):
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