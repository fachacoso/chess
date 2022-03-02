from abc import ABC, abstractmethod
from numpy import square
import pieces.piece_constants as piece_constants


class Piece(ABC):
    """
    ABSTRACT class for all chess pieces

    Abstract Class Attributes
    ----------
    notation : str
        Algebraic notation of piece - (P, R, N, B, Q, K)
        
    direction_indexes : list[int] (8)
        list of direction indexes corresponding to piece_constants.SLIDING_OFFSETS
        
    white_pieces and black_pieces : list[Piece()]
        list of pieces for white and black respectively
        
    
    Instance Attributes
    ----------
    index : int
        Index of piece
        
    player : str
        'w' if player is white, 'b' if player is black
        
    move_count : int
        Number of times moved
        
    captured : bool
        True if piece has been captured
        
    Movement Attributes
        possible_moves : list[int]
            List of indexes piece can possibly move
            
        attacked_squares : list[int]
            List of indexes of empty squares piece is attacking
            
        defended_squares : list[int]
            List of indexes piece is defending
            
        pinned_line : lint[int]
            List of indexes in between king and pinning enemy piece if current piece is pinned

    Methods
    -------
    get_moves(self, game_state)
        Gets possible moves for piece
        
    get_attacking_squares(self, game_state)
        Get list of index this piece is attacking
        
    has_moved(self)
        Checks if piece has moved
        
    move(self, new_index)
        Moves piece to new index
        
    undo_last_move(self, old_index)
        Move back piece to old_index
        
    same_team(self, target_square)
        Checks if piece is same side as piece in target_square
        
    piece_in_between(self, game_state, direction_offset, start_index, end_index)
        Checks if there are any pieces between start_index and end_index       
    """
    
    notation          = None
    direction_indexes = [0, 1, 2, 3, 4, 5, 6, 7]
    white_pieces      = []
    black_pieces      = []

    def __init__(self, index, player, move_count = 0):
        self.index      = index
        self.player     = player
        self.move_count = move_count
        self.captured   = False
        
        # Piece movement attributes
        self.possible_moves   = []
        self.attacked_squares = []
        self.defended_squares = []
        self.pinned_line      = []
        
        # List of all pieces
        if player == 'w':
            Piece.white_pieces.append(self)
        else:
            Piece.black_pieces.append(self)
    
    @abstractmethod
    def update_movement_attributes(self, game_state):
        """Updates possible_moves, attacked_squares, and defended_squares"""        
        pass
    
    @classmethod
    def update_all_movement_attributes(cls, game_state):
        """Updates possible_moves, attacked_squares, and defended_squares for ALL pieces"""  
        for piece in Piece.white_pieces:
            if not piece.captured:
                piece.update_movement_attributes(game_state)
        for piece in Piece.black_pieces:
            if not piece.captured:
                piece.update_movement_attributes(game_state)
        
    def has_moved(self):
        """Return true if piece has moved""" 
        if self.move_count > 0:
            return True
        return False
    
    def move(self, new_index):
        """Move piece to new_index"""
        self.index = new_index
        self.move_count += 1
        
    def undo_last_move(self, old_index):
        """Move back piece to old_index"""
        self.index = old_index
        self.move_count -= 1
             
    def same_team(self, target_square):
        """Return True if piece's owner is same as piece in target square"""
        return self.player == target_square.get_piece().player
    
    def piece_in_between(self, game_state, direction_offset, start_index, end_index):
        """Return True if there are any pieces between start_index and end_index"""
        square_index = start_index + direction_offset
        while square_index <= end_index:
            between_square = game_state.get_square(square_index)
            if not between_square.is_empty():
                return False
            square_index += direction_offset
        return True
    
    def indexes_in_between(self, direction_offset, end_index):
        index_list = []
        square_index = self.index + direction_offset
        while square_index != end_index:
            index_list.append(square_index)
            square_index += direction_offset
        return index_list
    
    
    """
    STRING REPRESENTATION
    """
    # Unicode representation
    def __str__(self):
        return piece_constants.UNICODE_SYMBOLS[self.player + self.notation]

    # FEN notation
    def __repr__(self):
        if self.player == 'w':
            return self.notation
        else:
            return self.notation.lower()


    

