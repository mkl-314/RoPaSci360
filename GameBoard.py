from util import print_board

class GameBoard(object):

    def __init__(self, data):
        self.data = data
        self.board_dict = self.format_file(data)
    
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
                    board_dict[hex] = "#"
                
        return board_dict

    def print(self):
        print_board(self.board_dict)