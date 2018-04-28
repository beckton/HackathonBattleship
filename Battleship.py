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
placement = False

player1 = Player()
player2 = Player()

def place_piece(board, player):
    print (player + " Place Ship")
    small_ship_row = getNumber("Place Row: ")
    small_ship_col = getNumber("Place Column: ")
    board[small_ship_row][small_ship_col] = on

def place_piece_two(board, player):
    global placement
    placement = False
    print (player + "Place Second Ship")
    while placement == False:
        small_ship_row = int(raw_input("Place Row: "))
        small_ship_col = int(raw_input("Place Column: "))
        if board[small_ship_row][small_ship_col] == 0 and board[small_ship_row][small_ship_col + 1] == 0:
            board[small_ship_row][small_ship_col] = 1
            board[small_ship_row][small_ship_col + 1] = 1
            placement = True
        else:
            print ("Ship already there, place somewhere else.")

def getNumber(position):
    try:
        return input(position + " 0-7:")
    except NameError:
        print ("\nInvalid Input!")
        return getNumber(position)

def guess(ship_board, player, hit_board):
    global player_guess
    global winner
    while player_guess == False:
        print(player = " Guess.")
        guess_row = int(raw_input("Guess Row: "))
        guess_col = int(raw_input("Guess Column: "))
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
#print("\n" * 100)
place_piece(player2.ship_board, "Player 2")
#print("\n" * 100)
place_piece_two(player1.ship_board, "Player 1")
#print("\n" * 100)
place_piece_two(player2.ship_board, "Player 2")
#print("\n" * 100)
