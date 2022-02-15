import pieces.piece as piece
import pieces.piece_constants as piece_constants


class King(piece.Piece):
    """
    Represents King piece.  Inherits from base Piece class.

    Attributes
    ----------
    cls.notation : str
        algebraic notation of King - K


    Methods
    -------
    get_moves(self, game_state)
        gets possible moves for king
    """

    notation = "K"

    def get_moves(self, game_state):
        """Returns list of moves for King"""
        moves  = []

        # Standard moves
        moves.extend(self.standard_moves(game_state))

        # Castling
        moves.extend(self.castle_moves(game_state))
        
        return moves

    def standard_moves(self, game_state):
        """Returns list of moves of single spaced moves King can do"""
        moves = []
        for direction_index in self.direction_indexes:
            offset = piece_constants.SLIDING_OFFSETS[direction_index]
            direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index][direction_index]
            if direction_max > 0:
                target_index = self.index + offset
                target_square = game_state.get_square(target_index)
                if not target_square.is_empty():
                    # If target piece player is same, it's blocked
                    if self.same_team(target_square):
                        continue
                    # If target piece player is different, it's captured
                    else:
                        moves.append(target_index)
                        continue
                moves.append(target_index)
        return moves
    
    def castle_moves(self, game_state):
        """Returns list of eligible castle moves"""
        wK_castle, wQ_castle, bK_castle, bQ_castle = game_state.castling
        player = self.player
        moves  = []

        if player == "w":
            if wK_castle:
                start_index       = piece_constants.WHITE_KING_INDEX
                end_index         = piece_constants.WHITE_ROOK_K_INDEX
                king_target_index = 6
                if self.piece_in_between(game_state, 1, start_index, end_index):
                    moves.append(king_target_index)
            if wQ_castle:
                start_index       = piece_constants.WHITE_ROOK_Q_INDEX
                end_index         = piece_constants.WHITE_KING_INDEX
                king_target_index = 2
                if self.piece_in_between(game_state, 1, start_index, end_index):
                    moves.append(king_target_index)
        else:
            if bK_castle:
                start_index       = piece_constants.BLACK_KING_INDEX
                end_index         = piece_constants.BLACK_ROOK_K_INDEX
                king_target_index = 62
                if self.piece_in_between(game_state, 1, start_index, end_index):
                    moves.append(king_target_index)
            if bQ_castle:
                start_index       = piece_constants.BLACK_ROOK_Q_INDEX
                end_index         = piece_constants.BLACK_KING_INDEX
                king_target_index = 58
                if self.piece_in_between(game_state, 1, start_index, end_index):
                    moves.append(king_target_index)
        return moves