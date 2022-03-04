import constants
import util.PGN as PGN_util 
import pieces.piece
import pieces.sliding_piece

# Class for a movement in a chess game
class Move:
    def __init__(self, piece, start_index, end_index, captured_piece, checking_pieces, game_over, non_FEN_attributes):
        self.piece              = piece
        self.start              = start_index
        self.end                = end_index
        self.captured           = captured_piece
        self.checking_pieces    = checking_pieces
        self.game_over          = game_over
        self.non_FEN_attributes = non_FEN_attributes
        self.PGN                = PGN_util.PGN.create_PGN_string(self)
        print(self.__str__())
    
    
    @classmethod
    def get_moves(cls, game_state, square_index):
        square = game_state.get_square(square_index)
        piece  = square.get_piece()
        moves  = piece.possible_moves
        return moves

    @classmethod
    def get_legal_moves(cls, game_state, square_index):
        legal_moves    = []
        square         = game_state.get_square(square_index)
        piece          = square.get_piece()
        possible_moves = Move.get_moves(game_state, square_index)
        
        # NO POSSIBLE MOVES - return empty list
        if len(possible_moves) == 0:
            return []
        
        # IF KING
        if piece.notation == 'K':
            
            # ILLEGAL KING MOVES - both attacked and defended squares
            attacked_squares_list = Move.get_attacked_squares_list(game_state.attacked_squares)
            defended_squares_list = game_state.defended_squares
            illegal_king_moves    = attacked_squares_list + defended_squares_list
                
            for move in possible_moves:
                if move not in illegal_king_moves:
                    legal_moves.append(move)
            return legal_moves
        
        # IF NOT KING
        else:
            # DOUBLE CHECK - no legal moves for non-king pieces
            if len(game_state.checking_pieces) == 2:
                return []
                
            # SINGLE CHECK - capture or block checking piece
            elif len(game_state.checking_pieces) == 1:
                checking_piece = game_state.checking_pieces[0]
                king_index = game_state.white_king_index if game_state.turn == 'w' else game_state.black_king_index
                
                # PINNED - cannot move
                if piece in game_state.pinned:
                    return []
                
                # CAPTURE
                if checking_piece.index in possible_moves:
                    legal_moves.append(checking_piece.index)
                    
                # BLOCK - if checking piece is Rook, Bishop, or Queen
                if isinstance(checking_piece, pieces.sliding_piece.SlidingPiece):
                    checking_line = checking_piece.indexes_in_between(checking_piece.checking_offset, king_index)
                    for move in possible_moves:
                        if move in checking_line:
                            legal_moves.append(move)
                            
                return legal_moves
            
            # NO CHECK
            else:
                # PINNED - only move in pinned line
                if piece.index in game_state.pinned:
                    for move in possible_moves:
                        if move in piece.pinned_line:
                            legal_moves.append(move)
                    return legal_moves
                
                # NO RESTRICTION - return all possible moves
                return possible_moves
    
    @classmethod
    def get_attacked_defended_pinned_check(cls, game_state):
        attacked_squares_dictionary = {}
        defended_squares            = []
        pinned_pieces               = []
        checking_pieces             = [] 
        
        # Update all piece movements
        pieces.piece.Piece.update_all_movement_attributes(game_state)
                
        if game_state.turn == 'w':
            opponent_pieces = pieces.piece.Piece.black_pieces
            king_index      = game_state.white_king_index
        else:
            opponent_pieces = pieces.piece.Piece.white_pieces
            king_index      = game_state.black_king_index
        for piece in opponent_pieces:
            attacked_squares_list = piece.attacked_squares
            if len(attacked_squares_list) != 0:
                attacked_squares_dictionary[piece.index] = attacked_squares_list
                
            possible_moves_list = piece.possible_moves
            if king_index in possible_moves_list:
                checking_pieces.append(piece)
            
            defended_squares.extend(piece.defended_squares)
            
        king_square = game_state.get_square(king_index)
        king = king_square.get_piece()
        pinned_pieces = king.get_pinned_pieces(game_state)
        
        return attacked_squares_dictionary, defended_squares, pinned_pieces, checking_pieces
        
    @classmethod
    def get_all_legal_moves(cls, game_state):
        legal_moves_dictionary = {}
        current_player_pieces = pieces.piece.Piece.white_pieces if game_state.turn == 'w' else pieces.piece.Piece.black_pieces
        #!  Iterate over specific playerss pieces
        for piece in current_player_pieces:
            if not piece.captured:
                legal_moves = Move.get_legal_moves(game_state, piece.index)
                if len(legal_moves) > 0:
                    legal_moves_dictionary[piece.index] = legal_moves
        return legal_moves_dictionary
    
    @classmethod
    def is_legal_move(cls, game_state, start_index, end_index):
        if start_index not in game_state.legal_moves.keys():
            return False
        legal_moves = game_state.legal_moves[start_index]
        return end_index in legal_moves
    
    @classmethod
    def get_attacked_squares_list(cls, attacked_squares_dictionary):
        attacked_squares_list = []
        for key, value in attacked_squares_dictionary.items():
            attacked_squares_list.extend(value)
        return list(set(attacked_squares_list))
                
    """
    STRING REPRESENTATION
    """    
    # PGN notation
    def __str__(self):
        return self.PGN