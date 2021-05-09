import csv
from ai.eval import *

def ml(state, future_state):

    with open('ml.csv', 'a', newline='') as csvfile:
        filewriter = csv.writer(csvfile, delimiter=',')
        
        # current_score, tokens_on_board, tokens_in_hand, future_score
        # my_invincible, op invincible

        current_score = tokens_on_board(state) + tokens_in_hand(state)
        on_board = tokens_on_board(state) 
        in_hand = tokens_in_hand(state)

        future_score = tokens_on_board(future_state) + tokens_in_hand(future_state)
        filewriter.writerow([str(current_score), str(on_board), str(in_hand), str(future_score)])


