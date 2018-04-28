import numpy as np

class Player:
    def __init__(self):
        self.ship_board = [[0 for x in range(8)] for y in range(8)]
        self.hit_board = [[0 for x in range(8)] for y in range(8)]

def print_board(board):
    for row in board: 
        print (" ".join(row))

on = 1
off = 0

player1 = Player()
player2 = Player()

print ("Player 1 Place Ship.")
small_ship1_row = int(raw_input("Place Row: "))
small_ship1_col = int(raw_input("Place Column: "))

print ("Player 2 Place Ship.")
small_ship2_row = int(raw_input("Place Row: "))
small_ship2_col = int(raw_input("Place Column: "))

player1.ship_board[small_ship1_row][small_ship1_col] = on
player2.ship_board[small_ship2_row][small_ship2_col] = on

print (np.matrix(player1.ship_board));
print (np.matrix(player2.ship_board));

winner = False
while winner == False:
    guess = False
    while guess == False: 
        guess_row = int (raw_input("Guess Row: "))
        guess_col = int (raw_input("Guess Column: "))
        if player2.hit_board[guess_row][guess_col] == 0:
            if player2.ship_board[guess_row][guess_col] == on:
                print ("You did it!")
                winner = True
                guess = True
                break
            else: 
                print ("Failure.")
                player2.hit_board[guess_row][guess_col] == on
                guess = True
        else: 
            print ("Already guessed that.")

    guess = False
    while guess == False:
        guess_row = int(raw_input("Guess Row: "))
        guess_col = int(raw_input("Guess Column: "))
        if player1.hit_board[guess_row][guess_col] == 0:
            if player1.ship_board[guess_row][guess_col] == on:
                print ("You did it!")
                winner = True
                guess = True
                break
            else:
                print ("Failure")
                player1.hit_board[guess_row][guess_col] == on
                guess = True
        else: 
            print ("Already guessed that.")

