from calendar import c
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
    def __init__(self, index, player, move_count=0):
        super().__init__(index, player, move_count)
        self.possible_castle_moves = []

    def update_movement_attributes(self, game_state):
        """Returns list of moves for King"""
        moves        = []
        castle_moves = []

        # STANDARD MOVES
        moves.extend(self.standard_moves(game_state))

        # CASTLE MOVES
        castle_moves.extend(self.castle_moves(game_state))
        
        self.possible_moves        = moves
        self.possible_castle_moves = castle_moves

    def standard_moves(self, game_state):
        """Returns list of possible moves and update attacked and defended squares"""
        moves            = []
        attacked_squares = []
        defended_squares = []
        
        for direction_index in self.direction_indexes:
            offset = piece_constants.SLIDING_OFFSETS[direction_index]
            direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index][direction_index]
            if direction_max > 0:
                target_index = self.index + offset
                target_square = game_state.get_square(target_index)
                
                # If target square has piece
                if not target_square.is_empty():
                    # If target piece is same team, it's defended
                    if self.same_team(target_square):
                        defended_squares.append(target_index)
                    # If target piece is different team, it's a possible move
                    else:
                        moves.append(target_index)
                        
                # If target square has NO piece
                else:
                    # Target square is attacked
                    attacked_squares.append(target_index)
                    # Target square is a possible move   
                    moves.append(target_index)
                    
        self.attacked_squares = attacked_squares
        self.defended_squares = defended_squares
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
    
    def enemy_piece_around(self, game_state):
        """Returns if enemy piece is around self(the king)"""
        valid_direction_indexes = []
        for direction_index in self.direction_indexes:
            direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index][direction_index]
            if direction_max > 0:
                valid_direction_indexes.append(direction_index)
                
        valid_offsets = [piece_constants.SLIDING_OFFSETS[index] for index in valid_direction_indexes]
        indexes_around = [self.index + offset for offset in valid_offsets]
        
        for index in indexes_around:
            square = game_state.get_square(index)
            if not square.is_empty():
                piece = square.get_piece()
                if piece.player != self.player:
                    return True
        return False
    
    def get_pinned_pieces(self, game_state):
        """Returns list of pinned pieces and adds pinned_line to pinned piece"""
        pinning_piece = None
        pinned_pieces = []
        opp = 'w' if game_state.turn == 'b' else 'b'
        # Iterate over all directions
        for direction_index in self.direction_indexes:
            target_index = self.index 
            offset =  piece_constants.SLIDING_OFFSETS[direction_index]
            direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index][direction_index]
            
            # Set elligible pinning pieces according to direction_index
            if direction_index < 4:  
                pinning_pieces = ['R', 'Q']
            else:  
                pinning_pieces = ['B', 'Q']
            
            possible_pin = None
            possible_pin_line = []
            # Iterate over all squares in a single direction to find possible_pin
            for i in range(direction_max):
                target_index = target_index + offset
                square = game_state.get_square(target_index)
                
                possible_pin_line.append(target_index)
                
                # If square is not empty
                if not square.is_empty():
                    piece = square.get_piece()
                    
                    # If there IS NOT a possible pin candidate already
                    if not possible_pin:
                        # If opponent piece, no pin
                        if piece.player == opp:
                            break
                        # If current player piece, possible pin
                        else:
                            possible_pin = target_index
                            
                    # If there IS a possible pin candidate already
                    else:
                        possible_pinned_piece = game_state.get_square(possible_pin).get_piece()
                        # If opponent piece
                        if piece.player == opp:
                            # If elligible sliding piece type, add to pinned
                            if piece.notation in pinning_pieces:
                                possible_pinned_piece.pinning_piece = piece
                                possible_pinned_piece.pinned_line = possible_pin_line
                                pinned_pieces.append(possible_pin)     
                        # If current player piece, stop checking
                        else:
                            break

        return pinned_pieces