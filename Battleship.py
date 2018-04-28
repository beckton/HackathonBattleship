'''
Battleship Raspberry Pi Interactive Game
    -This game is intended to be a game of Battleship that lights an led board on a 
     Raspberry Pi to mimmick the traditional board game.
Hack The Ozarks
April 27-28, 2018
Authors:
    Bec Braughton
    Andrew Beers
    Desmond Ford
    Ben O'Neal
    Miranda McCoy
    Bailey Lalonde
'''
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
winner = False
player_guess = False

player1 = Player()
player2 = Player()

def place_piece(board, player):
    print (player + " Place Ship")
    small_ship_row = int(raw_input("Place Row: "))
    small_ship_col = int(raw_input("Place Column: "))
    board[small_ship_row][small_ship_col] = on

def guess(ship_board, player, hit_board):
    global player_guess
    global winner
    while player_guess == False:
        print(player = " Guess.")
        guess_row = int (raw_input("Guess Row: "))
        guess_col = int (raw_input("Guess Column: "))
        if hit_board[guess_row][guess_col] == 0:
            if ship_board[guess_row][guess_col] == on:
                print ("You did it!")
                winner = True
                player_guess = True
                break
            else:
                print ("Failure")
                hit_board[guess_row][guess_col] == on
                player_guess = True
        else: 
            print ("Already guessed that.")

place_piece(player1.ship_board, "Player 1")
place_piece(player2.ship_board, "Player 2")

print (np.matrix(player1.ship_board));
print (np.matrix(player3.ship_board));

while winner == False:
    if winner == False:
        player_guess = False
    guess(player2.ship_board, "Player 1", player1.hit_board)
    if winner == False:
        player_guess = False
    guess(player1.ship_board, "Player 2", player2.hit_board)
