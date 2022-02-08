import pieces.sliding_piece as sliding_piece

class Queen(sliding_piece.SlidingPiece):
    """
    Represents Queen piece.  Inherits from SlidingPiece class.

    Attributes
    ----------
    cls.notation : str
        algebraic notation of Queen - Q
    cls.direction_indexes : list[int] (8)
        indexes corresponding to direction offset Queen can move
    """
    notation = 'Q'
    direction_indexes = [0, 1, 2, 3, 4, 5, 6, 7]
    
    
