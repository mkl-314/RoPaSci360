# RoPaSci360
COMP30024 Game

Upper tokens should never be on the same hex bc not optimal or token will be eaten

## Test Cases
- 1a_simple_test: Basic test of movement/search
- 1b_impossible_test: No valid targets
- 1c_simple_test2: Basic test of movement/search
- 2_impossible_block: Wall blocking, no solution test
- 2_three_s: Test of multi-target searching
- 2_maze: Test of blocks and searching around them
- 3_paper_block: Wall of paper blocking Rock and tests swinging
- 3_trapped.json: Upper rock surrounded and cannot move until freed by paper 
- 4_swing_test.json: Test of 3 tokens at once with swinging


## Part B
i think we should assign each move a value which determines how good a move is. e.g. eating a piece is 1 point. Moving towards a piece is 0.2. -1 point if our piece can be eaten.
Total points = our move points - their move points
