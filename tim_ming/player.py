
from classes.GameBoard import GameBoard
from ai.sim_minimax import *
from MachineLearning import ml



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

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """
        self.turn += 1
        value, move = minimax_manager(self.game_board)

        ml(self.game_board, move[0])
        return move[1].do_action(move[2])

    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        self.game_board.update(player_action, opponent_action)

