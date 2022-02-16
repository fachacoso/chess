import constants
import util.PGN as PGN_util
import pieces.sliding_piece

# Class for a movement in a chess game
class Move:
    def __init__(self, piece, start_index, end_index, captured_piece, checking_piece_index, non_FEN_attributes):
        self.piece                = piece
        self.start                = start_index
        self.end                  = end_index
        self.captured             = captured_piece
        self.checking_piece_index = checking_piece_index
        self.PGN                  = PGN_util.PGN.create_PGN_string(self)
        self.non_FEN_attributes   = non_FEN_attributes
        print(self.__str__())
    
        
    # PGN notation
    def __str__(self):
        return self.PGN
    
    @classmethod
    def get_moves(cls, game_state, square_index):
        square = game_state.get_square(square_index)
        piece  = square.get_piece()
        moves  = piece.get_moves(game_state)
        return moves

    @classmethod
    def get_legal_moves(cls, game_state, square_index):
        legal_moves = []
        square = game_state.get_square(square_index)
        piece  = square.get_piece()
        possible_moves = Move.get_moves(game_state, square_index)
        
        attacked_squares_list = Move.get_attacked_squares_list(game_state.attacked_squares)
        
        # King cannot capture defended squares
        if piece.notation == 'K':
            attacked_squares_list.extend(game_state.defended_squares)
        
        is_check = type(game_state.checking_piece_index) == int
        if is_check:
            checking_piece_square = game_state.get_square(game_state.checking_piece_index)
            checking_piece  = checking_piece_square.get_piece()
            if piece.notation == 'K':
                if isinstance(checking_piece, pieces.sliding_piece.SlidingPiece):
                    attacked_squares_list.extend(checking_piece.line_to_king())
                for move in possible_moves:
                    if move not in attacked_squares_list:
                        legal_moves.append(move)
                return legal_moves
            else:
                for move in possible_moves:
                    for pinning_index, pinned_line in game_state.pinned_lines.items():
                        # If move will let the piece stay pinned or capture pinning piece, append
                        if move in pinned_line or move == pinning_index:
                            legal_moves.append(move)   
                return legal_moves

        # If piece is king, can only move to non-attacked square
        if piece.notation == 'K':
            for move in possible_moves:
                if move not in attacked_squares_list:
                    legal_moves.append(move)
            return legal_moves
        else:
            # If non-king piece is pinned, can only move within the pinned_line
            for pinning_index, pinned_line in game_state.pinned_lines.items():
                if square_index in pinned_line:
                    for move in possible_moves:
                        # If move will let the piece stay pinned, append
                        if move in pinned_line or move == pinning_index:
                            legal_moves.append(move)   
                    return legal_moves
        return possible_moves
            
        
    
    @classmethod        
    def get_attacked_squares(cls, game_state):
        attacked_squares_dictionary = {}
        opponent = 'w' if game_state.turn == 'b' else 'b'
        for square in game_state.board:
            if not square.is_empty():
                piece = square.get_piece()
                if piece.player == opponent:
                    piece = square.get_piece()
                    attacked_square_list = piece.get_attacking_squares(game_state)
                    if len(attacked_square_list) != 0:
                        attacked_squares_dictionary[piece.index] = attacked_square_list
        return attacked_squares_dictionary
    
    @classmethod        
    def get_pinned_lines(cls, game_state):
        pinned_line_dictionary = {}
        opponent = 'w' if game_state.turn == 'b' else 'b'
        for square in game_state.board:
            if not square.is_empty():
                piece = square.get_piece()
                if piece.player == opponent:
                    if isinstance(piece, pieces.sliding_piece.SlidingPiece):
                        piece = square.get_piece()
                        if len(piece.pinned_line) != 0:
                            pinned_line_dictionary[piece.index] = piece.pinned_line
        return pinned_line_dictionary
        
    @classmethod
    def get_all_legal_moves(cls, game_state):
        legal_moves_dictionary = {}
        for square in game_state.board:
            if not square.is_empty():
                piece = square.get_piece()
                if game_state.turn == piece.player:
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
    def get_checking_piece_index(cls, game_state):
        if game_state.turn == 'w':
            king_index = game_state.white_king_index
        else:
            king_index = game_state.black_king_index
        for piece_index, attacked_square_list in game_state.attacked_squares.items():
            if king_index in attacked_square_list:
                return piece_index
        return None
    
    @classmethod
    def get_attacked_squares_list(cls, attacked_squares_dictionary):
        attacked_squares_list = []
        for key, value in attacked_squares_dictionary.items():
            attacked_squares_list.extend(value)
        return list(set(attacked_squares_list))
    
    @classmethod
    def get_defended_squares(cls, game_state):
        defended_squares_list = []
        
        # Check if king near opponent pieces
        if game_state.turn == 'w':
            king_index = game_state.white_king_index
        else:
            king_index = game_state.black_king_index
        king_square = game_state.get_square(king_index)
        king = king_square.get_piece()
        
        if king.enemy_piece_around(game_state):
            opponent = 'w' if game_state.turn == 'b' else 'b'
            for square in game_state.board:
                if not square.is_empty():
                    piece = square.get_piece()
                    if piece.player == opponent:
                        piece = square.get_piece()
                        if len(piece.defended_squares) != 0:
                            defended_squares_list.extend(piece.defended_squares)
        return defended_squares_list