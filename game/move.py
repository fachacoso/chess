import constants
import util.utils as util

# Class for a movement in a chess game
class Move:
    def __init__(self, piece, start_index, end_index, captured_piece, check):
        self.piece      = piece
        self.start      = start_index
        self.end        = end_index
        self.captured   = captured_piece
        self.check      = NotImplemented
        print(self.__str__())
        
    # PGN notation
    def __str__(self):
        notation = self.piece.notation
        if notation == 'P':
            notation = ''
        capture = ''
        if self.captured:
            if self.piece.notation == 'P':
                capture = util.index_to_coordinate(self.start)[0]
            capture += 'x'
        coordinate = util.index_to_coordinate(self.end)
        
        return notation + capture + coordinate
    
    @classmethod
    def moves(cls, game_state, square_index):
        square = game_state.get_square(square_index)
        piece  = square.get_piece()
        moves  = piece.get_moves(game_state)
        return moves
    
def parse_PGN(PGN):
    NotImplemented
        


def legal_moves(game_state, square_index):
    
    possible_moves = move.moves(game_state, square_index)
    for move in possible_moves:
        NotImplemented
    
    
def find_opponent_king(game_state, player):
    opponent = 'w' if player == 'b' else 'b'
    for square_index in range(constants.SQUARE_COUNT):
        square = game_state.get_square(square_index)
        if not square.is_empty():
            piece = square.get_piece()
            if piece.notation == 'K' and piece.player == opponent:
                opponent_king_index = square_index
                break
    return opponent_king_index
                    
    
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
