from random import randint
import numpy as np

class Player:
    def __init__(self):
        self.ship_board = [[0 for x in range(8)] for y in range(8)]
        self.hit_board = [[0 for x in range(8)] for y in range(8)]

def print_board(board):
    for row in board: 
        pring " ".join(row)

player1 = Player()
player2 = Player()

player1.ship_board[0] [0] = 1

print (np.matrix(player1.ship_board))

guess_row = int(raw_input("Guess Row: "))
guess_col = int(raw_input("Guess Column: "))

if player1.ship_board[guess_row][guess_col] == 1:
    print ("You did it!")
else:
    print ("Failure.")