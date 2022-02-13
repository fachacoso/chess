import constants

class Square:
    # Initialize empty square
    def __init__(self, index, piece = None):
        self.piece = piece
        self.index = index
        self.promoted_pawn = None
    
    def get_piece(self):
        return self.piece

    def is_empty(self):
        return self.piece == None
    
    def move_piece(self, end_square):
        piece = self.get_piece()
        
        # Update squares
        self.remove_piece()
        end_square.set_piece(piece)
        
        # Update Piece
        piece.move(end_square.index)
        """
        if piece.notation == "P":
            if end_square.index in constants.FIRST_RANK_INDEXES or end_square.index in constants.EIGHT_RANK_INDEXES:
                end_square.promote_pawn(end_square, "Q")
        """
                        
    def undo_move_piece(self, old_square):
        piece = self.get_piece()
        self.remove_piece()
        old_square.set_piece(piece)
        piece.undo_last_move(old_square.index)
        
        
    
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
        
    def check_pawn_promotion(self, index):
        """Checks if piece is pawn and eligible to promote.  If so, promotes to Queen.

        Args:
            index (int): index of piece
        """        
        square = self.get_square(index)
        piece = square.get_piece()
        if piece.notation == "P":
            if index in constants.FIRST_RANK_INDEXES or index in constants.EIGHT_RANK_INDEXES:
                square.promote_pawn(index, "Q")
    
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