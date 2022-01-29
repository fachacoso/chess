from pieces import Pawn, Rook, Knight, Bishop, Queen, King

INITIAL_BOARD_STATE = [
 'bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR',
 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP',
 'wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR'
]

# Class for chess game session
class GameState:
    turn = "W"
    turn_counter = 0
    history_counter = 0
    move_history = []
    highlight = {}
    

    def __init__(self):
        self.board = Board()
        
    def is_game_over(self):
        self.board
        
    def move(self, start, end):
        piece = self.board.board_pos[start]
        self.board.board_pos[end] = piece
        self.board.board_pos[start] = '--'
        self.move_history.append(move(self.turn, start, end))

class move:
    def __init__(self, start, end):
        self.start = start
        self.end = end     
        
    
           
        
# Class for chess board
class Board:
    
    def __init__(self):
        self.captured_stack = []
        self.board_pos = ['-'] * 64
        for i in range(64):
            if i == '-':
                self.board_pos[i] = INITIAL_BOARD_STATE[i]
            else:
                player = INITIAL_BOARD_STATE[i][0]
                type = INITIAL_BOARD_STATE[i][1]
                if type == 'P':
                    self.board_pos[i] = Pawn(i, player)
                elif type == 'R':
                    self.board_pos[i] = Rook(i, player)
                elif type == 'N':
                    self.board_pos[i] = Knight(i, player)
                elif type == 'B':
                    self.board_pos[i] = Bishop(i, player)
                elif type == 'Q':
                    self.board_pos[i] = Queen(i, player)
                elif type == 'K':
                    self.board_pos[i] = King(i, player)
                

    def __str__(self):
        string = "\n"
        for i in range(8):
            string += " ".join([str(x) for x in self.board_pos[i * 8 : (i + 1) * 8]])
            string += "\n"
        return string
    
    def move(self, start, end):
        self.board_pos[end] = self.board_pos[start]
        self.board_pos[start] = "-"
        