import constants
import util.PGN as PGN_util

# Class for a movement in a chess game
class Move:
    def __init__(self, piece, start_index, end_index, captured_piece, check):
        self.piece    = piece
        self.start    = start_index
        self.end      = end_index
        self.captured = captured_piece
        self.check    = NotImplemented
        self.PGN      = PGN_util.PGN.create_PGN_string(self)
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
        possible_moves = move.moves(game_state, square_index)
        for move in possible_moves:
            NotImplemented
    
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
        
    
                    
    
    def is_check(game_state, player):
        opponent_king_index = game_state.find_opponent_king(player)
        
        # Check all legal moves for 
        for square_index in range(constants.SQUARE_COUNT):
            square = game_state.get_square(square_index)
            if not square.is_empty():
                piece = square.get_piece()
                if piece.player == game_state.turn:
                    piece_moves = moves(piece, square_index)
                    print('Check if king index {} in piece_moves {}'.format(opponent_king_index, piece_moves))
                    if opponent_king_index in moves(piece, piece_moves):
                        return True
        return False