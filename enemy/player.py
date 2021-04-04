
class Player:
    def __init__(self, player):
        """
        Called once at the beginning of a game to initialise this player.
        Set up an internal representation of the game state.

        The parameter player is the string "upper" (if the instance will
        play as Upper), or the string "lower" (if the instance will play
        as Lower).
        """
        # put your code here

    def action(self):
        """
        Called at the beginning of each turn. Based on the current state
        of the game, select an action to play this turn.
        """

        try:
            next_move = input("Input turn:")
            move = next_move.replace(" ", "").split(",")

            if len(move) == 4:
                # THROW, p, 2, 2
                return ("THROW", move[1], (int(move[2]), int(move[3])) )
            elif len(move) == 5:
                # SLIDE, 2, 2, 2, 1
                return (move[0], (int(move[1]), int(move[2])), (int(move[3]), int(move[4])) )
            else:
                raise ValueError("Print correct format")

        except:
            print("Print correct format:")
            self.action()
    
    def update(self, opponent_action, player_action):
        """
        Called at the end of each turn to inform this player of both
        players' chosen actions. Update your internal representation
        of the game state.
        The parameter opponent_action is the opponent's chosen action,
        and player_action is this instance's latest chosen action.
        """
        pass

