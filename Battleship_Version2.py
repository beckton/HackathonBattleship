'''
Battleship Raspberry Pi Interactive Game
    -This game is intended to be a game of Battleship that lights an led board on a 
     Raspberry Pi to mimmick the traditional board game.
Hack The Ozarks
April 27-28, 2018
Authors:
    Andrew Beers
    Bec Braughton
    Desmond Ford
    Bailey Lalonde
    Miranda McCoy
    Bennie O'Neal
'''
import RPi.GPIO as GPIO
import time
import threading

SDI   = 11
RCLK  = 12
SRCLK = 13

code_J = [0x01,0xff,0x80,0xff,0x01,0x02,0x04,0x08,0x10,0x20,0x40,0x80,0xff,0xff,0xff,0xff,0xff,0xff,0xff,0xff]
code_K = [0x00,0x7f,0x00,0xfe,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0xfe,0xfd,0xfb,0xf7,0xef,0xdf,0xbf,0x7f]

code_H = [0b10000000,0b01000000,0b00100000,0b00010000,0b00001000,0b00000100,0b00000010,0b00000001, 0b00000000]
code_L = [0b11111110,0b11111101,0b11111011,0b11110111,0b11101111,0b11011111,0b10111111,0b01111111, 0b00000000]
let_w = [["X","X","X","X","X","X","X","X"],
        ["X","X","X","X","X","X","X","X"],
        ["0","0","0","0","0","X","X","0"],
        ["0","0","0","0","X","X","0","0"],
        ["0","0","0","0","X","X","0","0"],
        ["0","0","0","0","0","X","X","0"],
        ["X","X","X","X","X","X","X","X"],
        ["X","X","X","X","X","X","X","X"]]
let_i = [["0","0","0","0","0","0","0","0"],
        ["X","X","0","0","0","0","X","X"],
        ["X","X","0","0","0","0","X","X"],
        ["X","X","X","X","X","X","X","X"],
        ["X","X","X","X","X","X","X","X"],
        ["X","X","0","0","0","0","X","X"],
        ["X","X","0","0","0","0","X","X"],
        ["0","0","0","0","0","0","0","0"]]
let_n = [["X","X","X","X","X","X","X","X"],
        ["X","X","X","X","X","X","X","X"],
        ["0","X","X","0","0","0","0","0"],
        ["0","0","X","X","X","0","0","0"],
        ["0","0","0","X","X","X","0","0"],
        ["0","0","0","0","0","X","X","0"],
        ["X","X","X","X","X","X","X","X"],
        ["X","X","X","X","X","X","X","X"]]
let_e = [["0","0","0","0","0","0","0","0"],
        ["X","X","X","X","X","X","X","X"],
        ["X","X","X","X","X","X","X","X"],
        ["X","X","0","X","X","0","X","X"],
        ["X","X","0","X","X","0","X","X"],
        ["X","X","0","0","0","0","X","X"],
        ["X","X","0","0","0","0","X","X"],
        ["0","0","0","0","0","0","0","0"]]
let_r = [["0","0","0","0","0","0","0","0"],
        ["X","X","X","X","X","X","X","X"],
        ["X","X","X","X","X","X","X","X"],
        ["X","0","0","0","X","X","0","0"],
        ["X","X","0","X","X","X","X","0"],
        ["X","X","X","X","X","0","X","X"],
        ["0","X","X","X","0","0","0","X"],
        ["0","0","0","0","0","0","0","0"]]



ships_set = False
player_one_turn = True
blink_counter = 0

class Player:
        def __init__(self):
            self.ship_board = [[0 for x in range(8)] for y in range(8)]
            self.hit_board = [[0 for x in range(8)] for y in range(8)]
            self.ship_one = False
            self.ship_two = False
            self.ship_three = False
            self.ship_four = False
            self.ship_five = False
            self.ship_one_hits = 0
            self.ship_two_hits = 0
            self.ship_three_hits = 0
            self.ship_four_hits = 0
            self.ship_five_hits = 0
        def increment_hits_one(self):
            self.ship_one_hits += 1
        def increment_hits(self):
            self.ship_two_hits += 1
        def increment_hits_two(self):
            self.ship_three_hits += 1
        def increment_hits_three(self):
            self.ship_four_hits += 1
        def increment_hits_four(self):
            self.ship_five_hits += 1

class dots_thread (threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
        def run(self):
                light_loop()
                

def setup():
    GPIO.setmode(GPIO.BOARD)    # Number GPIOs by its physical location
    GPIO.setup(SDI, GPIO.OUT)
    GPIO.setup(RCLK, GPIO.OUT)
    GPIO.setup(SRCLK, GPIO.OUT)
    GPIO.output(SDI, GPIO.LOW)
    GPIO.output(RCLK, GPIO.LOW)
    GPIO.output(SRCLK, GPIO.LOW)
    
def hc595_in(dat):
    for bit in range(0, 8): 
        GPIO.output(SDI, 0x80 & (dat << bit))
        GPIO.output(SRCLK, GPIO.HIGH)
        #time.sleep(0.001)
        GPIO.output(SRCLK, GPIO.LOW)

def hc595_out():
    GPIO.output(RCLK, GPIO.HIGH)
    #time.sleep(0.001)
    GPIO.output(RCLK, GPIO.LOW)


def turn_on_miss_dot(col,row):
        hc595_in(code_L[row])
        hc595_in(code_H[col])
        hc595_out()
def turn_on_hit_dot(col,row):
        if blink_counter < 20:
                hc595_in(code_L[row])
                hc595_in(code_H[col])
                hc595_out()
        else:
                hc595_in(code_L[8])
                hc595_in(code_H[8])
                hc595_out()

def loop():
        for i in range(0, len(code_J)):
                hc595_in(code_K[i])
                hc595_in(code_J[i])
                hc595_out()
                time.sleep(0.1)

        for i in range(len(code_J)-1, -1, -1):
                hc595_in(code_K[i])
                hc595_in(code_J[i])
                hc595_out()
                time.sleep(0.1)
def fin():
        timer = 0
        while timer < 25:
                show_hit_board(let_w)
                timer = timer + 1
        turn_on_miss_dot(8,8)
        time.sleep(.15)
        timer = 0
        while timer < 25:
                show_hit_board(let_i)
                timer = timer + 1
        turn_on_miss_dot(8,8)
        time.sleep(.15)
        timer = 0
        while timer < 25:
                show_hit_board(let_n)
                timer = timer + 1
        turn_on_miss_dot(8,8)
        time.sleep(.15)
        timer = 0
        while timer < 25:
                show_hit_board(let_n)
                timer = timer + 1
        turn_on_miss_dot(8,8)
        time.sleep(.15)
        timer = 0
        while timer < 25:
                show_hit_board(let_e)
                timer = timer + 1
        turn_on_miss_dot(8,8)
        time.sleep(.15)
        timer = 0
        while timer < 25:
                show_hit_board(let_r)
                timer = timer + 1
        loop()
def show_ship_board(player_ship_board):
        for col in range(0,8):
                for row in range(0,8):
                        time.sleep(.0001)
                        if player_ship_board[col][row] != 0:
                                turn_on_miss_dot(col,row)

def show_hit_board(player_hit_board):
        global blink_counter
        for col in range(0,8):
                for row in range(0,8):
                        time.sleep(.0001)
                        if player_hit_board[col][row] == "H":
                                turn_on_hit_dot(col,row)
                        elif player_hit_board[col][row] == "X":
                                turn_on_miss_dot(col,row)
        if blink_counter == 40:
                blink_counter = 0
        else:
                blink_counter = blink_counter + 1  
def light_loop():
        while True:
                while ships_set == False:
                        while player_one_turn == True:
                                show_ship_board(player1.ship_board)
                        while player_one_turn == False:
                                show_ship_board(player2.ship_board)
                while player_one_turn == True:
                        show_hit_board(player1.hit_board)
                while player_one_turn == False:
                        show_hit_board(player2.hit_board)
                while winner == True:
                        fin()

def print_board(board):
        for x in range(8):
            row = ""

            for y in range(8):
                row = row + str(board[y][x]) + " "
            print(row.rstrip())
                
one = 1
two = 2
three = 3
four = 4
five = 5
miss = 'x'
winner = False 
player_guess = False
placement = False

player1 = Player()
player2 = Player()

def place_piece(board, player):
    print(player + " Place First Ship (1x3)")
    small_ship_row = getNumber_col3("Place Row:")
    small_ship_col = getNumber("Place Column:")
    board[small_ship_col][small_ship_row] = one
    board[small_ship_col][small_ship_row + 1] = one
    board[small_ship_col][small_ship_row + 2] = one

def place_piece_two(board, player):
    global placement
    placement = False
    print(player + " Place Second Ship (1x2)")
    while placement == False:
        small_ship_row = getNumber_col2("Place Row:")
        small_ship_col = getNumber("Place Column:")
        if board[small_ship_col][small_ship_row] == 0 and board[small_ship_col][small_ship_row + 1] == 0:
            board[small_ship_col][small_ship_row] = two
            board[small_ship_col][small_ship_row + 1] = two
            active_dot_array = board
            placement = True
        else:
            print("Ship already there, place somewhere else.")

def place_piece_three(board, player):
    global placement
    placement = False
    print(player + " Place Third Ship (2x1)")
    while placement == False:
        small_ship_row = getNumber("Place Row:")
        small_ship_col = getNumber_row2("Place Column:")
        if board[small_ship_col][small_ship_row] == 0 and board[small_ship_col + 1][small_ship_row] == 0:
            board[small_ship_col][small_ship_row] = three
            board[small_ship_col + 1][small_ship_row] = three
            placement = True
        else:
            print("Ship already there, place somewhere else.")

def place_piece_four(board, player):
    global placement
    placement = False
    print(player + " Place Fourth Ship (3x1)")
    while placement == False:
        small_ship_row = getNumber("Place Row:")
        small_ship_col = getNumber_col3("Place Column:")
        if board[small_ship_col][small_ship_row] == 0 and board[small_ship_col + 1][small_ship_row] == 0 and board[small_ship_col + 2][small_ship_row] == 0:
            board[small_ship_col][small_ship_row] = four
            board[small_ship_col + 1][small_ship_row] = four
            board[small_ship_col + 2][small_ship_row] = four
            placement = True
        else:
            print("Ship already there, place somewhere else.")

def place_piece_five(board, player):
    global placement
    placement = False
    print(player + " Place Fifth Ship (4x1)")
    while placement == False:
        small_ship_row = getNumber("Place Row:")
        small_ship_col = getNumber_col4("Place Column:")
        if board[small_ship_col][small_ship_row] == 0 and board[small_ship_col + 1][small_ship_row] == 0 and board[small_ship_col + 2][small_ship_row] == 0 and board[small_ship_col + 3][small_ship_row] == 0:
            board[small_ship_col][small_ship_row] = five
            board[small_ship_col + 1][small_ship_row] = five
            board[small_ship_col + 2][small_ship_row] = five
            board[small_ship_col + 3][small_ship_row] = five
            placement = True
        else:
            print("Ship already there, place somewhere else.")
def getNumber(position):
    try:
        value = int(input(position + " 0-7: "))
        if (0 <= value <= 7):
            return value
        else:
            print("\nOut of Bounds!")
            return getNumber(position)
    except NameError:
        print("\nInvalid Input!")
        return getNumber(position)
    except SyntaxError:
        print("\nInvalid Input!")
        return getNumber(position)

def getNumber_col2(position):
    try:
        value = int(input(position + " 0-6: "))
        if (0 <= value <= 6):
            return value
        else:
            print("\nOut of Bounds!")
            return getNumber_col2(position)
    except NameError:
        print("\nInvalid Input!")
        return getNumber_col2(position)
    except SyntaxError:
        print("\nInvalid Input!")
        return getNumber_col2(position)

def getNumber_col3(position):
    try:
        value = int(input(position + " 0-5: "))
        if (0 <= value <= 5):
            return value
        else:
            print("\nOut of Bounds!")
            return getNumber_col3(position)
    except NameError:
        print("\nInvalid Input!")
        return getNumber_col3(position)
    except SyntaxError:
        print("\nInvalid Input!")
        return getNumber_col3(position)

def getNumber_col4(position):
    try:
        value = int(input(position + " 0-4: "))
        if (0 <= value <= 4):
            return value
        else:
            print("\nOut of Bounds!")
            return getNumber_col4(position)
    except NameError:
        print("\nInvalid Input!")
        return getNumber_col4(position)
    except SyntaxError:
        print("\nInvalid Input!")
        return getNumber_col4(position)
    
def getNumber_row2(position):
    try:
        value = int(input(position + " 0-6: "))
        if (0 <= value <= 6):
            return value
        else:
            print("\nOut of Bounds!")
            return getNumber_row2(position)
    except NameError:
        print("\nInvalid Input!")
        return getNumber_row2(position)
    except SyntaxError:
        print("\nInvalid Input!")
        return getNumber_row2(position)
    
def guess(ship_board, player, hit_board, Player):
    global player_guess
    global winner
    while player_guess == False:
        print_board(hit_board)
        print(player + " Guess.")
        guess_row = getNumber("Guess Row:")
        guess_col = getNumber("Guess Column:")
        if hit_board[guess_col][guess_row] == 0:
            if ship_board[guess_col][guess_row] == one:
                print("Hit!")
                hit_board[guess_col][guess_row] = 'H'
                player_guess = False
                Player.increment_hits_one()
                if (Player.ship_one_hits == 3 and Player.ship_two == True and Player.ship_three == True and Player.ship_four == True and Player.ship_five == True):
                    print("You sunk a ship!")
                    Player.ship_one = True
                    winner = True
                    player_guess = True
                    break
                elif (Player.ship_one_hits == 3):
                    print("You sunk a ship!")
                    hit_board[guess_col][guess_row] = 'H'
                    Player.ship_one = True
                    player_guess = False
            elif ship_board[guess_col][guess_row] == two:
                print("Hit!")
                hit_board[guess_col][guess_row] = 'H'
                player_guess = False
                Player.increment_hits()
                if (Player.ship_two_hits == 2 and Player.ship_three == True and Player.ship_four == True and Player.ship_one == True and Player.ship_five == True):
                    print("You sunk a ship!")
                    Player.ship_two = True
                    winner = True
                    player_guess = True
                    break
                elif (Player.ship_two_hits == 2):
                    print("You sunk a ship!")
                    Player.ship_two = True
                    player_guess = False
            elif ship_board[guess_col][guess_row] == three:
                print("Hit!")
                hit_board[guess_col][guess_row] = 'H'
                player_guess = False
                Player.increment_hits_two()
                if (Player.ship_three_hits == 2 and Player.ship_two == True and Player.ship_four == True and Player.ship_one == True and Player.ship_five == True):
                    print("You sunk a ship!")
                    Player.ship_three = True
                    winner = True
                    player_guess = True
                    break
                elif (Player.ship_three_hits == 2):
                    print("You sunk a ship!")
                    Player.ship_three = True
                    player_guess= False
            elif ship_board[guess_col][guess_row] == four:
                print("Hit!")
                hit_board[guess_col][guess_row] = 'H'
                player_guess = False
                Player.increment_hits_three()
                if (Player.ship_four_hits == 3 and Player.ship_two == True and Player.ship_three == True and Player.ship_one == True and Player.ship_five == True):
                    print("You sunk a ship!")
                    Player.ship_four = True
                    winner = True
                    player_guess = True
                    break
                elif (Player.ship_four_hits == 3):
                    print("You sunk a ship!")
                    Player.ship_four = True
                    player_guess = False
            elif ship_board[guess_col][guess_row] == five:
                print("Hit!")
                hit_board[guess_col][guess_row] = 'H'
                player_guess = False
                Player.increment_hits_four()
                if (Player.ship_five_hits == 4 and Player.ship_two == True and Player.ship_three == True and Player.ship_one == True and Player.ship_four == True):
                    print("You sunk a ship!")
                    Player.ship_five = True
                    winner = True
                    player_guess = True
                    break
                elif (Player.ship_five_hits == 4):
                    print("You sunk a ship!")
                    Player.ship_five = True
                    player_guess = False
            else:
                print("Miss.")
                hit_board[guess_col][guess_row] = 'X'
                raw_input("End Turn./nNext Player [ENTER]")
                player_guess = True
        else:
            print("Already guessed that!")
# start of program
#light thread starts
GPIO.setwarnings(False)
setup()
light_thread = dots_thread()
light_thread.start()
turn_on_miss_dot(8, 8)


  #clears matrix
player_one_turn = True
place_piece(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_two(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_three(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_four(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_five(player1.ship_board, "Player 1")
print_board(player1.ship_board)
raw_input("Ready Player One?")
print("\n" * 100)
player_one_turn = False
time.sleep(.05)
turn_on_miss_dot(8, 8)

place_piece(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_two(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_three(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_four(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_five(player2.ship_board, "Player 2")
print_board(player2.ship_board)
raw_input("Ready Player Two?")
print("\n" * 100)
#print_board(player1.ship_board)
#print("\n")
#print_board(player2.ship_board)
ships_set = True
player_one_turn = True
time.sleep(.05)
turn_on_miss_dot(8, 8)

while winner == False:
    if winner == False:
        player_guess = False
    guess(player2.ship_board, "Player 1", player1.hit_board, player2)
    player_one_turn = False
    turn_on_miss_dot(8, 8)
    if winner == False:
        player_guess = False
    turn_on_miss_dot(8, 8)
    guess(player1.ship_board, "Player 2", player2.hit_board, player1)
    player_one_turn = True
    turn_on_miss_dot(8, 8)

if (player1.ship_one == True and player1.ship_two == True):
    print("Player 2 Wins!")
else:
    print("Player 1 Wins!")
