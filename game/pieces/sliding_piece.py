import pieces.piece as piece
import pieces.piece_constants as piece_constants


class SlidingPiece(piece.Piece):
    """
    Class for all sliding chess pieces (ie. Rook, Bishop, Queen)

    Attributes
    ----------
    notation : str
        algebraic notation of piece - (R, B, Q)

    Methods
    -------
    get_moves(self, game_state)
        gets possible moves for sliding piece
    """

    notation          = None

    def get_moves(self, game_state):
        """Returns list of moves for sliding piece"""
        moves  = []
        square = game_state.get_square(self.index)
        piece  = square.get_piece()

        # For each direction
        for direction_index in self.direction_indexes:
            offset = piece_constants.SLIDING_OFFSETS[direction_index]
            direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index][direction_index]

            # For max length of each direction
            for i in range(direction_max):
                target_index = self.index + offset * (i + 1)
                target_square = game_state.get_square(target_index)

                # Check target square
                if not target_square.is_empty():
                    # If target piece player is same, it's blocked
                    if piece.same_team(target_square):
                        break

                    # If target piece player is different, it's captured
                    else:
                        moves.append(target_index)
                        break
                moves.append(target_index)
        return moves
