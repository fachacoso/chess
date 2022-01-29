# Class for an entire chess game
from abc import ABC
from codecs import BOM_BE

INITIAL_BOARD_STATE = [
 'bR', 'bN', 'bB', 'bB', 'bQ', 'bK', 'bN', 'bR',
 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 'bP', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 '--', '--', '--', '--', '--', '--', '--', '--', 
 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP', 'wP',
 'wR', 'wN', 'wB', 'wB', 'wQ', 'wK', 'wN', 'wR'
]


class game_state:
    
    # Player with current turn - (W)hite or (B)lack
    turn = "W"
    turn_counter = 0
    history_counter = 0
    move_history = []
    highlight = {}
    

    def __init__(self):
        self.board = board()
        
    def is_game_over(self):
        self.board
        
    def move(self, start, end):
        self.board(start, end)
        self.move_history.append(move(self.turn, start, end))
        
class move:
    def __init__(self, player, start, end):
        move.player = player
        move.start = start
        move.end = end
        
# Class for chess board
class board:
    
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
                    self.board_pos[i] = pawn(i, player)
                elif type == 'R':
                    self.board_pos[i] = rook(i, player)
                elif type == 'N':
                    self.board_pos[i] = knight(i, player)
                elif type == 'B':
                    self.board_pos[i] = bishop(i, player)
                elif type == 'Q':
                    self.board_pos[i] = queen(i, player)
                elif type == 'K':
                    self.board_pos[i] = king(i, player)
                

    def __repr__(self):
        string = ""
        """    
        stack = []
        #CODE FOR BLACK SIDE    
        for i in range(8):
            stack.append(board_pos_copy[i * 8 : (i+1) * 8])
        stack.pop()
        """
        for i in range(8):
            string += " ".join([str(x) for x in self.board_pos[i * 8 : (i + 1) * 8]])
            string += "\n"
        return string
    
    def move(self, start, end):
        self.board_pos[end] = self.board_pos[start]
        self.board_pos[start] = "-"
        
        
# Class for each chess piece
class piece(ABC):
    def __init__(self, index, player):
        self.index = index
        self.player = player
    
    def __str__(self):
        return self.symbol

    def legal_moves(self):
        NotImplemented()
    
    
class pawn(piece):
    piece_value = 1
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♙"
            self.value = self.piece_value
        else:
            self.symbol = "♟︎"
            self.value = -self.piece_value
    
class rook(piece):
    piece_value = 5
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♖"
            self.value = self.piece_value
        else:
            self.symbol = "♜"
            self.value = -self.piece_value

class knight(piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♘"
            self.value = self.piece_value
        else:
            self.symbol = "♞"
            self.value = -self.piece_value

class bishop(piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♗"
            self.value = self.piece_value
        else:
            self.symbol = "♝"
            self.value = -self.piece_value

class queen(piece):
    piece_value = 8
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♕"
            self.value = self.piece_value
        else:
            self.symbol = "♛"
            self.value = -self.piece_value

class king(piece):
    piece_value = 999
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♔"
            self.value = self.piece_value
        else:
            self.symbol = "♚"
            self.value = -self.piece_value