
from classes.GameBoard import GameBoard
from moves.throw_move import *
from ai.minimax import *



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

        if player == "upper":
            self.game_board.w1 = 0.7
            self.game_board.w2 = 0.9
            self.game_board.w3 = 0.3
            self.game_board.w4 = 0.3
        else:
            self.game_board.w1 = 1
            self.game_board.w2 = 1
            self.game_board.w3 = 0.1
            self.game_board.w4 = 0.1

        # w1 needs to be higher than everything else
        # w2 needs to be low


    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        self.turn += 1
        # print(self.player + " w1=" + str(self.game_board.w1))
        # print(self.player + " w2=" + str(self.game_board.w2))
        # print(self.player + " w3=" + str(self.game_board.w3))
        # print(self.player + " w4=" + str(self.game_board.w4))
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

