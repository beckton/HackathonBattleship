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
    Ben O'Neal
'''
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
                player_guess = True
        else:
            print("Already guessed that.")
      
place_piece(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_two(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_three(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_four(player1.ship_board, "Player 1")
print_board(player1.ship_board)
place_piece_five(player1.ship_board, "Player 1")
print("\n" * 100)
place_piece(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_two(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_three(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_four(player2.ship_board, "Player 2")
print_board(player2.ship_board)
place_piece_five(player2.ship_board, "Player 2")
print("\n" * 100)
#print_board(player1.ship_board)
#print("\n")
#print_board(player2.ship_board)


while winner == False:
    if winner == False:
        player_guess = False
    guess(player2.ship_board, "Player 1", player1.hit_board, player2)
    if winner == False:
        player_guess = False
    guess(player1.ship_board, "Player 2", player2.hit_board, player1)

if (player1.ship_one == True and player1.ship_two == True):
    print("Player 2 Wins!")
else:
    print("Player 1 Wins!")
