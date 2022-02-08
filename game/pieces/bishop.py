import pieces.sliding_piece as sliding_piece


class Bishop(sliding_piece.SlidingPiece):
    """
    Represents Bishop piece.  Inherits from SlidingPiece class.

    Attributes
    ----------
    cls.notation : str
        algebraic notation of Bishop - B
    cls.direction_indexes : list[int] (4)
        indexes corresponding to direction offset Bishop can move
    """

    notation          = "B"
    direction_indexes = [4, 5, 6, 7]
