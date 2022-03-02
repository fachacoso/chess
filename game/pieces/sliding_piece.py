from pieces.piece import Piece
import pieces.piece as piece
import pieces.piece_constants as piece_constants


class SlidingPiece(piece.Piece):
    """
    Class for all sliding chess pieces (Rook, Bishop, and Queen)

    Attributes
    ----------
    notation : str
        Algebraic notation of piece - (R, B, Q)
        
    checking_offset : int
        Offset pointing to direction of king if sliding piece is checking

    Methods
    -------
    get_moves(self, game_state)
        gets possible moves for sliding piece
    """
    
    direction_indexes = [0, 1, 2, 3, 4, 5, 6, 7]
    notation          = None
    
    def __init__(self, index, player, move_count = 0):
        Piece.__init__(self, index, player, move_count)
        self.checking_offset = 0
        

    def update_movement_attributes(self, game_state):
        """Updates possible moves, attacked squares, and defended squares"""
        moves            = []
        attacked_squares = []
        defended_squares = []
        
        square = game_state.get_square(self.index)
        piece  = square.get_piece()
        
        if self.player == 'w':
            enemy_king_index = game_state.black_king_index
        else:
            enemy_king_index = game_state.white_king_index

        # For each direction
        for direction_index in self.direction_indexes:
            offset = piece_constants.SLIDING_OFFSETS[direction_index]
            direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index][direction_index]

            seen_king = False
            # For max length of each direction
            for index in range(direction_max):
                target_index = self.index + offset * (index + 1)
                target_square = game_state.get_square(target_index)
                
                # If target square has piece
                if not target_square.is_empty():
                    # If target piece is same team, it's defended
                    if self.same_team(target_square):
                        defended_squares.append(target_index)
                        break
                    # If target piece is different team, it's a possible move
                    else:
                        moves.append(target_index)
                        # If target piece is enemy king, square behind is also attacked
                        if target_index == enemy_king_index:
                            attacked_squares.append(enemy_king_index + offset)
                            self.checking_offset = offset
                        break
                        
                # If target square has NO piece
                else:
                    # Target square is attacked
                    attacked_squares.append(target_index)
                    # Target square is a possible move   
                    moves.append(target_index)

        self.attacked_squares = attacked_squares
        self.defended_squares = defended_squares
        self.possible_moves   = moves
    
    