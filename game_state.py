# Class for an entire chess game
from abc import ABC
from codecs import BOM_BE


class game_state:
    
    # Player with current turn - (W)hite or (B)lack
    turn = "W"
    turn_counter = 1
    move_history = []

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
        self.board_pos = ['-'] * 64
        self.board_pos[0] = rook(0, "W")
        self.board_pos[1] = knight(1, "W")
        self.board_pos[2] = bishop(2, "W")
        self.board_pos[3] = queen(3, "W")
        self.board_pos[4] = king(4, "W")
        self.board_pos[5] = bishop(5, "W")
        self.board_pos[6] = knight(6, "W")
        self.board_pos[7] = rook(7, "W")
        for i in range(8, 16):
            self.board_pos[i] = pawn(i, "W")
        for i in range(48, 56):
            self.board_pos[i] = pawn(i, "B")
        self.board_pos[56] = rook(56, "B")
        self.board_pos[57] = knight(57, "B")
        self.board_pos[58] = bishop(58, "B")
        self.board_pos[59] = queen(59, "B")
        self.board_pos[60] = king(60, "B")
        self.board_pos[61] = bishop(61, "B")
        self.board_pos[62] = knight(62, "B")
        self.board_pos[63] = rook(63, "B")
            

    def __repr__(self):
        board_pos_copy = self.board_pos
        stack = []
        string = ""
        for i in range(8):
            stack.append(board_pos_copy[i * 8 : (i+1) * 8])
        for i in range(8):
            string += " ".join([str(x) for x in stack.pop()])
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
        if self.player == "W":
            self.symbol = "♙"
            self.value = self.piece_value
        else:
            self.symbol = "♟︎"
            self.value = -self.piece_value
    
class rook(piece):
    piece_value = 5
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "W":
            self.symbol = "♖"
            self.value = self.piece_value
        else:
            self.symbol = "♜"
            self.value = -self.piece_value

class knight(piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "W":
            self.symbol = "♘"
            self.value = self.piece_value
        else:
            self.symbol = "♞"
            self.value = -self.piece_value

class bishop(piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "W":
            self.symbol = "♗"
            self.value = self.piece_value
        else:
            self.symbol = "♝"
            self.value = -self.piece_value

class queen(piece):
    piece_value = 8
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "W":
            self.symbol = "♕"
            self.value = self.piece_value
        else:
            self.symbol = "♛"
            self.value = -self.piece_value

class king(piece):
    piece_value = 999
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "W":
            self.symbol = "♔"
            self.value = self.piece_value
        else:
            self.symbol = "♚"
            self.value = -self.piece_value