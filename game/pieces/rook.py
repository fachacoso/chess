import pieces.sliding_piece as sliding_piece


class Rook(sliding_piece.SlidingPiece):
    """
    Represents Rook piece.  Inherits from SlidingPiece class.

    Attributes
    ----------
    cls.notation : str
        algebraic notation of Rook - R
    cls.direction_indexes : list[int] (4)
        indexes corresponding to direction offset Rook can move
    """

    notation          = "R"
    direction_indexes = [0, 1, 2, 3]
