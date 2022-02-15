from abc import ABC, abstractmethod
from tracemalloc import start

from numpy import square
import pieces.piece_constants as piece_constants


class Piece(ABC):
    """
    ABSTRACT class for all chess pieces

    Attributes
    ----------
    notation : str
        Algebraic notation of piece - (P, R, N, B, Q, K)
    direction_indexes : list[int] (8)
        list of direction indexes corresponding to piece_constants.SLIDING_OFFSETS

    Methods
    -------
    get_moves(self, game_state)
        gets possible moves for piece
        
    has_moved(self)
        checks if piece has moved
        
    move(self, new_index)
        moves piece to new index
        
    same_team(self, target_square)
        checks if piece is same side as piece in target_square
    """
    
    notation          = None
    direction_indexes = [0, 1, 2, 3, 4, 5, 6, 7]

    def __init__(self, index, player, move_count = 0):
        self.index            = index
        self.player           = player
        self.move_count       = move_count
        self.defended_squares = []
    
    @abstractmethod 
    def get_moves(cls, game_state):
        pass
    
    def get_attacking_squares(self, game_state):
        return self.get_moves(game_state)
        
    def has_moved(self):
        if self.move_count > 0:
            return True
        return False
    
    def move(self, new_index):
        self.index = new_index
        self.move_count += 1
        
    def undo_last_move(self, old_index):
        self.index = old_index
        self.move_count -= 1
             
    def same_team(self, target_square):
        return self.player == target_square.get_piece().player
    
    def piece_in_between(self, game_state, direction_offset, start_index, end_index):
        """Checks if there are any pieces between start_index and end_index"""
        square_index = start_index + direction_offset
        while square_index <= end_index:
            between_square = game_state.get_square(square_index)
            if not between_square.is_empty():
                return False
            square_index += direction_offset
        return True
    
    # Unicode representation
    def __str__(self):
        return piece_constants.UNICODE_SYMBOLS[self.player + self.notation]

    # FEN notation
    def __repr__(self):
        if self.player == 'w':
            return self.notation
        else:
            return self.notation.lower()


    

