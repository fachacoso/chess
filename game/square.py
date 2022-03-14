import constants
import pieces.piece as piece

class Square:
    """
    Class representing square in board in GameState

    Attributes
    ----------
    piece : Piece
        Piece contained in square - (P, R, N, B, Q, K)
    index : int
        Index of square in game_state
        

    Methods
    -------
    get_piece(self)
        Returns piece in square
    
    is_empty(self)
        Returns True if a piece is in square
     
    move_piece(self, end_square)
        Moves piece to end_square
    
    undo_move_piece(self, old_square)
        Moves piece back to old_square
    
    set_piece(self, piece)
        Set piece to square
        
    remove_piece(self)
        Removes piece from square
    
    #! Pawn stuff
    """
    # Initialize empty square
    def __init__(self, index, piece = None):
        self.piece = piece
        self.index = index
    
    def get_piece(self):
        """Returns piece in square"""
        return self.piece

    def is_empty(self):
        """Returns True if a piece is in square"""
        return self.piece == None
    
    def move_piece(self, end_square):
        """Moves piece to end_square"""
        piece = self.get_piece()
        
        # Update squares
        self.remove_piece()
        end_square.set_piece(piece)
        
        # Update Piece
        piece.move(end_square.index)
                        
    def undo_move_piece(self, old_square):
        """Moves piece back to old_square"""
        piece = self.get_piece()
        self.remove_piece()
        old_square.set_piece(piece)
        piece.undo_last_move(old_square.index)
        
    def set_piece(self, piece):
        """Set piece to square"""
        self.piece = piece
        
    def remove_piece(self):
        """Removes piece from square"""
        self.piece = None
        
                
    """
    STRING REPRESENTATION
    """
    # Unicode representation
    def __str__(self):
        if self.is_empty():
            return '--'
        else:
            return self.get_piece().__str__()
    
    # FEN notation    
    def __repr__(self):
        if self.is_empty():
            return '-'
        else:
            return self.get_piece().__repr__()