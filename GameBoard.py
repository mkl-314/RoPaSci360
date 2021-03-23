from search.util import print_board

class GameBoard(object):
    BLOCK = "#"

    def __init__(self, data):
        self.data = data
        self.board_dict = self.format_file(data)
        self.upper_occupied_hexes = []

        self.upper_tokens = {}
        self.upper_tokens["r"], self.upper_tokens["p"], self.upper_tokens["s"] = self.separate_tokens(data["upper"]) 
        self.r_lower_tokens, self.p_lower_tokens, self.s_lower_tokens = self.separate_tokens(data["lower"]) 
    
        self.upper_defeats = {"r": self.s_lower_tokens, "s": self.p_lower_tokens, "p": self.r_lower_tokens}
    
    def format_file(self, data):
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
                
        return board_dict

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
        print_board(self.board_dict)

