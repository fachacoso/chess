import constants
import util.PGN as PGN_util
import pieces.sliding_piece

# Class for a movement in a chess game
class Move:
    def __init__(self, piece, start_index, end_index, captured_piece, check, non_FEN_attributes):
        self.piece              = piece
        self.start              = start_index
        self.end                = end_index
        self.captured           = captured_piece
        self.check              = check
        self.PGN                = PGN_util.PGN.create_PGN_string(self)
        self.non_FEN_attributes = non_FEN_attributes
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
        # If piece is king, can only move to non-attacked square
        if piece.notation == 'K':
            for move in possible_moves:
                if move not in game_state.attacked_squares:
                    legal_moves.append(move)
            return legal_moves
        
        # If piece is pinned, can only move within the pinned_line
        for pinned_line in game_state.pinned_lines:
            if square_index in pinned_line:
                for move in possible_moves:
                    # If move will let the piece stay pinned, append
                    if move in game_state.pinned_lines:
                        legal_moves.append(move)   
                return legal_moves
        return possible_moves
            
        
    
    @classmethod        
    def get_attacked_squares(cls, game_state):
        attacked_squares_list = []
        opponent = 'w' if game_state.turn == 'b' else 'b'
        for square in game_state.board:
            if not square.is_empty():
                piece = square.get_piece()
                if piece.player == opponent:
                    piece = square.get_piece()
                    attacked_squares_list.extend(piece.get_attacking_squares(game_state))
        return set(attacked_squares_list)
    
    @classmethod        
    def get_pinned_lines(cls, game_state):
        pinned_line_list = []
        opponent = 'w' if game_state.turn == 'b' else 'b'
        for square in game_state.board:
            if not square.is_empty():
                piece = square.get_piece()
                if piece.player == opponent:
                    if isinstance(piece, pieces.sliding_piece.SlidingPiece):
                        piece = square.get_piece()
                        if len(piece.pinned_line) != 0:
                            pinned_line_list.append(piece.pinned_line)
        return pinned_line_list
        
    
                    
    @classmethod
    def is_check(cls, game_state):
        if game_state.turn == 'w':
            king_index = game_state.white_king_index
        else:
            king_index = game_state.black_king_index

        if king_index in game_state.attacked_squares:
            return True
        return False