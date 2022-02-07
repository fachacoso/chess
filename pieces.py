from abc import ABC, abstractmethod

# Class for each chess piece
class Piece(ABC):

    def __init__(self, index, player, move_count = 0):
        self.index = index
        self.player = player
        self.move_count = move_count
        
    def has_moved(self):
        if self.move_count > 0:
            return True
        return False
    
    def move(self, new_index):
        self.index = new_index
        self.move_count += 1
        
    def undo_move(self, old_index):
        self.index = old_index
        self.move_count -= 1

    # Unicode representation
    def __str__(self):
        return UNICODE_SYMBOLS[self.player + self.notation]

    # FEN notation
    def __repr__(self):
        if self.player == 'w':
            return self.notation
        else:
            return self.notation.lower()
    

class Pawn(Piece):
    notation = 'P'

class Rook(Piece):
    notation = 'R'

class Knight(Piece):
    notation = 'N'

class Bishop(Piece):
    notation = 'B'

class Queen(Piece):
    notation = 'Q'

class King(Piece):
    notation = 'K'
    
UNICODE_SYMBOLS = {
                    'wP':'♙',
                    'wR':'♖',
                    'wN':'♘',
                    'wB':'♗',
                    'wQ':'♕',
                    'wK':'♔',                         
                    'bP':'♟︎',
                    'bR':'♜',
                    'bN':'♞',
                    'bB':'♝',
                    'bQ':'♛',
                    'bK':'♚'
                    }