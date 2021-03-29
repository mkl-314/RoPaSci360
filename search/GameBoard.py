<<<<<<< HEAD
from util import print_board
=======
from search.util import print_board
>>>>>>> 9aa5fd7d2e37aef040fdb3c91540f037a71077e9
import re

class GameBoard(object):
    BLOCK = "#"
    token_defeats = ["r", "s", "p"]

<<<<<<< HEAD
    def __init__(self, data, turn):
        self.turn = turn
=======
    def __init__(self, data):
>>>>>>> 9aa5fd7d2e37aef040fdb3c91540f037a71077e9
        self.board_dict = self.updates_board(data)
        self.data = self.convert_to_data(self.board_dict)
        self.upper_occupied_hexes = []

        self.upper_tokens = {}
        self.lower_tokens = {}
        self.upper_tokens["r"], self.upper_tokens["p"], self.upper_tokens["s"] = self.separate_tokens(self.data["upper"]) 
        self.lower_tokens["r"], self.lower_tokens["p"], self.lower_tokens["s"] = self.separate_tokens(self.data["lower"]) 
    
    # formats gameboard data for printing and removes any tokens that are meant to be deleted
    def updates_board(self, data):
        board_dict = {}
        for (token, positions) in data.items():
            for pos in positions:
                hex = ( pos[1], pos[2])
                if not hex in board_dict:
                    board_dict[hex] = ""
                    
                if token == "upper":
                    board_dict[hex] += pos[0].upper()
                elif token == "lower":
                    board_dict[hex] += pos[0].lower()
                else:
                    board_dict[hex] = self.BLOCK
        
        board_dict = self.delete_defeated_tokens(board_dict)
        return board_dict

    def delete_defeated_tokens(self, board_dict):
        for (hex, symbols) in board_dict.items():
            if "r" in symbols.lower() and "p" in symbols.lower() and "s" in symbols.lower():
                board_dict[hex] = ""
            else:
                for i in range(3):
                    if self.token_defeats[i] in symbols.lower() and self.token_defeats[i-1] in symbols.lower():
                        board_dict[hex] = re.sub(self.token_defeats[i], "", board_dict[hex], flags=re.IGNORECASE)
        return board_dict

    def convert_to_data(self, board_dict):
        data = {"upper": [], "lower": [], "block": []}

        for (hex, symbols) in board_dict.items():
            for symbol in symbols:
                if symbol == "#":
                    data["block"].append(["", hex[0], hex[1]])
                elif symbol.isupper():
                    data["upper"].append([symbol.lower(), hex[0], hex[1]])
                elif symbol.islower():
                    data["lower"].append([symbol, hex[0], hex[1]])
        return data

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

    def print(self):
<<<<<<< HEAD
        print_board(self.board_dict)
=======
        print_board(self.board_dict)

>>>>>>> 9aa5fd7d2e37aef040fdb3c91540f037a71077e9
