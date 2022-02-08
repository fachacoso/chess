import constants
import util.utils as util

# Class for a movement in a chess game
class Move:
    def __init__(self, piece, start_index, end_index, captured_piece, castling, en_passant, check):
        self.piece = piece
        self.start = start_index
        self.end = end_index        
        self.captured = captured_piece
        self.castling = castling
        self.en_passant = en_passant
        self.check = NotImplemented
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
    
def parse_PGN(PGN):
    NotImplemented
        
    
sliding_offsets = [8, -8, -1, 1, 7, 9, -9, -7] # Directions for index offset - N, S, E, W, NE, NW, SE, SW
num_squares_to_edge = {}
for square_index in range(constants.SQUARE_COUNT):
    x = util.get_x(square_index)
    y = util.get_y(square_index)
    num_north = 7 - y
    num_south = y
    num_east = x
    num_west = 7 - x
    num_squares_to_edge[square_index] = [
        num_north,
        num_south,
        num_east,
        num_west,
        min(num_north, num_east),
        min(num_north, num_west),
        min(num_south, num_east),
        min(num_south, num_west)
    ]
       
def moves(game_state, square_index):
    square = game_state.get_square(square_index)
    piece = square.get_piece()
    
    moves = []
    if piece.notation == 'P':
        return pawn_moves(game_state, square_index)
    elif piece.notation == 'R':
        return rook_moves(game_state, square_index)
    elif piece.notation == 'N':
        return knight_moves(game_state, square_index)
    elif piece.notation == 'B':
        return bishop_moves(game_state, square_index)
    elif piece.notation == 'Q':
        return rook_moves(game_state, square_index) + bishop_moves(game_state, square_index)
    elif piece.notation == 'K':
        return king_moves(game_state, square_index)
    return moves

def legal_moves(game_state, square_index):
    
    possible_moves = moves(game_state, square_index)
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
    
def pawn_moves(game_state, piece_index):
    moves = []
    square = game_state.get_square(piece_index)
    piece = square.get_piece()
    
    # Helper variables
    direction_max = num_squares_to_edge[piece_index]
    num_north, num_south, num_east, num_west = direction_max[:4]
    
    # Makes offsets for possible legal movement (forward or capture)
    direction_max = num_squares_to_edge[piece_index]
    captures = []
    if piece.player == 'w':
        if num_north > 0:
            forward_offset = 8
            if num_east > 0:
                captures.append(piece_index + 7)
            if num_west > 0:
                captures.append(piece_index + 9)
    else:
        if num_south > 0:
            forward_offset = -8
            if num_east > 0:
                captures.append(piece_index - 9)
            if num_west > 0:
                captures.append(piece_index - 7)

    if (piece.player == 'w'and num_north > 0) or (piece.player == 'b'and num_south > 0):
        # Forward movement
        forward_max = 1
        if not piece.has_moved():
            forward_max = 2
        for i in range(forward_max):
            target_index = piece_index + forward_offset * (i + 1)
            target_square = game_state.get_square(target_index)
            if not target_square.is_empty():
                break
            moves.append(target_index)
        
        # Captures
        for target_index in captures:
            target_square = game_state.get_square(target_index)
            if not target_square.is_empty():
                if not same_team(piece, target_square):
                    moves.append(target_index)
            # Check for en passant
            elif game_state.en_passant == target_index:
                moves.append(target_index)
    return moves
        
def knight_moves(game_state, piece_index):
    moves = []
    square = game_state.get_square(piece_index)
    piece = square.get_piece()
    
    # Helper variables
    direction_max = num_squares_to_edge[piece_index]
    num_north, num_south, num_east, num_west = direction_max[:4]
    
    # All 8 directions
    offsets = [-10, 6, -17, 15, -15, 17, -6, 10]
    offset_index = 0
    for x in range(-2, 3):
        if x == 0:
            continue
        if x < 0:
            horizontal_max = num_east
        else:
            horizontal_max = num_west
        for y in range(-2, 3):
            if y == 0 or abs(x) == abs(y):
                continue
            if y < 0:
                vertical_max = num_south
            else:
                vertical_max = num_north
            
            if horizontal_max >= abs(x) and  vertical_max >= abs(y):
                target_index = piece_index + offsets[offset_index]
                target_square = game_state.get_square(target_index)
                if not target_square.is_empty():
                    if not same_team(piece, target_square):
                        moves.append(target_index)
                else:
                    moves.append(target_index)
            offset_index += 1
    return moves

def rook_moves(game_state, piece_index):
    moves = []
    square = game_state.get_square(piece_index)
    piece = square.get_piece()
    
    directions = 4
    for direction_index in range(directions):
        offset = sliding_offsets[direction_index]
        direction_max = num_squares_to_edge[piece_index][direction_index]
        for i in range(direction_max):
            target_index = piece_index + offset * (i + 1)
            target_square = game_state.get_square(target_index)
            
            if not target_square.is_empty():
                # If target piece player is same, it's blocked 
                if same_team(piece, target_square):
                    break
                # If target piece player is different, it's captured 
                else:
                    moves.append(target_index)
                    break
            moves.append(target_index)
    return moves
            
def bishop_moves(game_state, piece_index):
    moves = []
    square = game_state.get_square(piece_index)
    piece = square.get_piece()
    
    directions = 4
    for direction_index in range(directions):
        offset = sliding_offsets[4 + direction_index]
        direction_max = num_squares_to_edge[piece_index][4 + direction_index]
        for i in range(direction_max):
            target_index = piece_index + offset * (i + 1)
            target_square = game_state.get_square(target_index)
            
            if not target_square.is_empty():
                # If target piece player is same, it's blocked 
                if same_team(piece, target_square):
                    break
                # If target piece player is different, it's captured 
                else:
                    moves.append(target_index)
                    break
            moves.append(target_index)
    return moves

def king_moves(game_state, piece_index):
    moves = []
    square = game_state.get_square(piece_index)
    piece = square.get_piece()
    
    directions = 8
    for direction_index in range(directions):
        offset = sliding_offsets[direction_index]
        direction_max = num_squares_to_edge[piece_index][direction_index]
        if direction_max > 0:
            target_index = piece_index + offset
            target_square = game_state.get_square(target_index)
            if not target_square.is_empty():
                # If target piece player is same, it's blocked 
                if same_team(piece, target_square):
                    continue
                # If target piece player is different, it's captured 
                else:
                    moves.append(target_index)
                    continue
            moves.append(target_index)
            
    # Castling
    wK_castle, wQ_castle, bK_castle, bQ_castle = game_state.castling
    wk_able, wQ_able, bK_able, bQ_able = [True, True, True, True]
    player = piece.player
    if player == 'w':
        if wK_castle:
            for square_index in range(constants.WHITE_KING_INDEX + 1, constants.WHITE_ROOK_K_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    wk_able = False
                    break
            if wk_able:
                moves.append(6)
        if wQ_castle:
            for square_index in range(constants.WHITE_ROOK_Q_INDEX + 1, constants.WHITE_KING_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    wQ_able = False
                    break
            if wQ_able:
                moves.append(2)
    else:
        if bK_castle:
            for square_index in range(constants.BLACK_KING_INDEX + 1, constants.BLACK_ROOK_K_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    bK_able = False
                    break
            if bK_able:
                moves.append(54)
        if bQ_castle:
            for square_index in range(constants.BLACK_ROOK_Q_INDEX + 1, constants.BLACK_KING_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    bQ_able = False
                    break
            if bQ_able:
                moves.append(58)
    return moves


def same_team(selected_piece, target_square):
    """Takes selected piece and target square(NOT PIECE)"""
    return selected_piece.player == target_square.get_piece().player