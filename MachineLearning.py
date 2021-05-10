import csv
from ai.eval import *

def ml(state, future_state):

    with open('ml.csv', 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        
        # current_score, tokens_on_board, tokens_in_hand, future_score
        # my_invincible, op invincible

        current_score = tokens_on_board(state) + tokens_in_hand(state)
        my_on_board = len(state.data[state.me])
        op_on_board = len(state.data[state.opponent])
        my_in_hand = state.tokens_in_hand[state.me]
        op_in_hand = state.tokens_in_hand[state.opponent]

        future_score = tokens_on_board(future_state) + tokens_in_hand(future_state)
        filewriter.writerow([current_score, my_on_board, op_on_board, my_in_hand, op_in_hand, future_score])


