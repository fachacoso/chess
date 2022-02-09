import constants

class Square:
    # Initialize empty square
    def __init__(self, piece = None):
        self.piece = piece
    
    def get_piece(self):
        return self.piece

    def is_empty(self):
        return self.piece == None
    
    def set_piece(self, piece):
        self.piece = piece
        
    def remove_piece(self):
        self.piece = None
        
    def promote_pawn(self, index, piece_notation):
        piece = self.get_piece()
        player = piece.player
        move_count = piece.move_count
        self.remove_piece()
        piece = constants.INSTANCE_NOTATION_DICTIONARY[piece_notation](index, player, move_count)
        self.set_piece(piece)
        
    
    # Unicode representation
    def __str__(self):
        if self.is_empty():
            return '-'
        else:
            return self.get_piece().__str__()
    
    # FEN notation    
    def __repr__(self):
        if self.is_empty():
            return '-'
        else:
            return self.get_piece().__repr__()