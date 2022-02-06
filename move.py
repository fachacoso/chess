from constants import *
from util.utils import *

# Class for a movement in a chess game
class Move:
    def __init__(self, piece, start_index, end_index, captured_piece, castling, en_passant):
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
                capture = index_to_coordinate(self.start)[0]
            capture += 'x'
        coordinate = index_to_coordinate(self.end)
        
        return notation + capture + coordinate
    
def parse_PGN(PGN):
    NotImplemented
        
    
sliding_offsets = [8, -8, -1, 1, 7, 9, -9, -7] # Directions for index offset - N, S, E, W, NE, NW, SE, SW
num_squares_to_edge = {}
for square_index in range(SQUARE_COUNT):
    x = get_x(square_index)
    y = get_y(square_index)
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
       
def legal_moves(game_state, square_index):
    square = game_state.get_square(square_index)
    piece = square.get_piece()
    
    legal_moves = []
    if piece.notation == 'P':
        return legal_pawn_moves(game_state, square_index)
    elif piece.notation == 'R':
        return legal_rook_moves(game_state, square_index)
    elif piece.notation == 'N':
        return legal_knight_moves(game_state, square_index)
    elif piece.notation == 'B':
        return legal_bishop_moves(game_state, square_index)
    elif piece.notation == 'Q':
        return legal_rook_moves(game_state, square_index) + legal_bishop_moves(game_state, square_index)
    elif piece.notation == 'K':
        return legal_king_moves(game_state, square_index)
    
def legal_pawn_moves(game_state, piece_index):
    legal_moves = []
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
            if num_east > 1:
                captures.append(piece_index + 7)
            if num_west > 1:
                captures.append(piece_index + 9)
    else:
        if num_south > 0:
            forward_offset = -8
            if num_east > 1:
                captures.append(piece_index - 9)
            if num_west > 1:
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
            legal_moves.append(target_index)
        
        # Captures
        for target_index in captures:
            target_square = game_state.get_square(target_index)
            if not target_square.is_empty():
                if not same_team(piece, target_square):
                    legal_moves.append(target_index)
            # Check for en passant
            elif game_state.en_passant == target_index:
                legal_moves.append(target_index)
    return legal_moves
        
def legal_knight_moves(game_state, piece_index):
    legal_moves = []
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
                        legal_moves.append(target_index)
                else:
                    legal_moves.append(target_index)
            offset_index += 1
    return legal_moves

def legal_rook_moves(game_state, piece_index):
    legal_moves = []
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
                    legal_moves.append(target_index)
                    break
            legal_moves.append(target_index)
    return legal_moves
            
def legal_bishop_moves(game_state, piece_index):
    legal_moves = []
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
                    legal_moves.append(target_index)
                    break
            legal_moves.append(target_index)
    return legal_moves

def legal_king_moves(game_state, piece_index):
    legal_moves = []
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
                    legal_moves += [target_index]
                    continue
            legal_moves += [target_index]
            
    # Castling
    wK_castle, wQ_castle, bK_castle, bQ_castle = game_state.castling
    wk_able, wQ_able, bK_able, bQ_able = [True, True, True, True]
    player = piece.player
    if player == 'w':
        if wK_castle:
            for square_index in range(WHITE_KING_INDEX + 1, WHITE_ROOK_K_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    wk_able = False
                    break
            if wk_able:
                legal_moves.append(6)
        if wQ_castle:
            for square_index in range(WHITE_ROOK_Q_INDEX + 1, WHITE_KING_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    wQ_able = False
                    break
            if wQ_able:
                legal_moves.append(2)
    else:
        if bK_castle:
            for square_index in range(BLACK_KING_INDEX + 1, BLACK_ROOK_K_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    bK_able = False
                    break
            if bK_able:
                legal_moves.append(54)
        if bQ_castle:
            for square_index in range(BLACK_ROOK_Q_INDEX + 1, BLACK_KING_INDEX):
                between_square = game_state.get_square(square_index)
                if not between_square.is_empty():
                    bQ_able = False
                    break
            if bQ_able:
                legal_moves.append(58)
    return legal_moves


def same_team(selected_piece, target_square):
    """Takes selected piece and target square(NOT PIECE)"""
    return selected_piece.player == target_square.get_piece().player