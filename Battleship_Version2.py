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
class Board:
    def __init__(self):
        self.board = [[0 for x in range(8)] for y in range(8)]

    def show(self):
        for x in range(8):
            row = ""
            
            for y in range(8):
                 row = row + str(self.board[x][y]) + " "
            print(row.rstrip())
        print()

    def setPos(self, x, y, value):
        self.board[int(y)][int(x)] = value

    def getPos(self, x, y):
        return self.board[int(y)][int(x)]

class Ship:
    def __init__(self, point, length, orientation):
        self.coords = []
        col = point[0]
        row = point[1]

        if (orientation == 0):
            # Horizontal Orientation
            for x in range(length):
                coord = col + x, point[1]
                self.coords.append(coord)
        else:
            # Vertical Orientation
            for y in range(length):
                coord = point[0], row + y
                self.coords.append(coord)

class Player:
    def __init__(self, name):
        self.name = name
        self.ship_board = Board()
        self.hit_board = Board()
        self.ships = []

    def updateBoard(self):
        for x in range(8):
            for y in range(8):
                # 0 is empty, 1 is a friendly ship, 2 is an enemy hit, 3 is an enemy miss
                if (self.ship_board.getPos(x, y) == 0):
                    for ship in self.ships:
                        for coord in ship.coords:
                            if (coord[0] == x and coord[1] == y):
                                self.ship_board.setPos(x, y, 1)

def place_piece(player, size):
    placed = False

    while(placed == False):
        print(player.name + " Place Ship (Size " + str(size) + ")")
        col = getNumber("Place Column: ", 7)
        row = getNumber("Place Row: ", 7)
        point = col, row

        # Attempt to add a ship
        ship = Ship(point, size, getOrientation())
        available = True

        # Check  the last coordinate (minimal checks) to make sure the ship will fit on the board
        values = ship.coords[size - 1]
        
        if (values[0] > 7 or values[1] > 7):
            # This point is not on the board
            available = False

        # Check to make sure the ship won't intersect with any existing ships
        for placed_ship in player.ships:
            for a in placed_ship.coords:
                for b in ship.coords:
                    if a[0] == b[0] and a[1] == b[1]:
                        # This point is already taken by another ship
                        available = False
                        pass

        if (available == True):
            player.ships.append(ship)
            player.updateBoard()
            player.ship_board.show()
            placed = True
        else:
            print("A ship can't be placed there, please try again.")
            
def getNumber(position, limit):
    try:
        value = int(input(position))

        if (0 <= value <= limit):
            return value
        else:
            print("\nOut of Bounds!")
            return getNumber(position)
    except:
        print("\nInvalid Input!")
        return getNumber(position, limit)

def getOrientation():
    return getNumber("Select Orientation (0 or 1): ", 1)

def guess(current, other):
    done = False
    
    while (done == False):
        print(current.name + " Guess.")
        current.hit_board.show()
        guess_col = getNumber("Guess Column: ", 7)
        guess_row = getNumber("Guess Row: ", 7)

        # Let the player guess this location if they have not tried it already
        if (current.hit_board.getPos(guess_col, guess_row) == 0):
            if (other.ship_board.getPos(guess_col, guess_row) == 1):
                # The player hit an enemy ship
                for ship in other.ships:
                    for coord in ship.coords:
                        if (coord[0] == guess_col and coord[1] == guess_row):
                            # 0 is empty, 1 is a ship, 2 is a hit, 3 is a miss
                            current.hit_board.setPos(guess_col, guess_row, 2)
                            other.ship_board.setPos(guess_col, guess_row, 2)
                            ship.coords.remove(coord)
                            print("Hit!")
                            print()
                            
                            # Check if the ship has been destroyed
                            if (len(ship.coords) == 0):
                                other.ships.remove(ship)
                                print("You destroyed an enemy ship!")
                                print("Enemy ships remaining: " + str(len(other.ships)))

                            # Check if the fleet has been destroyed
                            if (len(other.ships) == 0):
                                print(current.name + " won the game!")
                                return 1
            else:
                current.hit_board.setPos(guess_col, guess_row, 3)
                other.ship_board.setPos(guess_col, guess_row, 3)
                done = True
                print("Miss!")
                print()
        else:
            print("You already guessed these coordinates!")
    return 0

def setup(player):
    place_piece(player, 2)
    place_piece(player, 2)
    place_piece(player, 3)
    place_piece(player, 3)
    place_piece(player, 4)

# Start Game Logic
player1 = Player("Player 1")
setup(player1)

player2 = Player("Player 2")
setup(player2)

done = False

while(done == False):
    if (guess(player1, player2) == 1 or guess(player2, player1) == 1):
        done = True
