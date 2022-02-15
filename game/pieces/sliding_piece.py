from tkinter import E
from pieces.piece import Piece
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
    white_sliding_pieces = []
    black_sliding_pieces = []
    
    def __init__(self, index, player, move_count = 0):
        Piece.__init__(self, index, player, move_count)
        self.pinned_line = []
        if player == 'w':
            SlidingPiece.white_sliding_pieces.append(self)
        else:
            SlidingPiece.black_sliding_pieces.append(self)
            
    def get_moves(self, game_state):
        """Returns list of moves for sliding piece"""
        moves  = []
        square = game_state.get_square(self.index)
        piece  = square.get_piece()
        if game_state.turn == 'w':
            king_index = game_state.white_king_index
        else:
            king_index = game_state.black_king_index

        # For each direction
        seen_king = False
        for direction_index in self.direction_indexes:
            offset = piece_constants.SLIDING_OFFSETS[direction_index]
            direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index][direction_index]
            
            blocked = False
            king_line = []

            # For max length of each direction
            for i in range(direction_max):
                target_index = self.index + offset * (i + 1)
                target_square = game_state.get_square(target_index)
                
                if not blocked:
                    # If target square empty, append
                    if target_square.is_empty():
                            moves.append(target_index)
                    else:  
                        blocked = True
                        # If target piece player is different, piece is blocked AND can capture
                        if not piece.same_team(target_square):
                            moves.append(target_index)
                            
                if not seen_king:           
                    if blocked and not target_square.is_empty() and target_index == king_index:          
                        # If king is seen, set the list of indices to pinned_line            
                        self.pinned_line = king_line
                        seen_king == True
                        continue
                    else:
                        king_line.append(target_index)
        return moves