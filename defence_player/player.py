
from classes.GameBoard import GameBoard
from moves.throw_move import *
from ai.minimax import *
import copy

class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        self.player = player
        self.turn = 0
        self.game_board = GameBoard(player)
        self.symbols = ["p", "r", "s", "p", "r"]
        self.single_destroy = True


    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        self.turn += 1
        
        if self.game_board.me == "upper":
            flip = 1
        else:
            flip = -1

        if self.turn <= 5:

            symbol = self.symbols.pop()

            return ('THROW', symbol, (4 * flip, flip * (1 - self.turn)) )
        elif self.turn == 6:
            return ('THROW', "s", (0, 0) )
        
        if len(self.game_board.data[self.player]) == 6 and self.single_destroy:
            new_game_board = copy.deepcopy(self.game_board)

            for token in new_game_board.data[self.player]:
                if token[1] != flip * 4:
                    the_token = [token]
                else:
                    new_game_board.board_dict.pop( (token[1], token[2]))
            
            new_game_board.data[self.player] = the_token

            new_game_board.tokens_in_hand[self.player] = 0

            move = minimax_manager(new_game_board)

            return move[0].do_action(move[1])
        
        else:
            self.single_destroy = False

        move = minimax_manager(self.game_board)

        return move[0].do_action(move[1])

    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        self.game_board.update(player_action, opponent_action)

