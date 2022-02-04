from constants import *
from utils import *
 
sliding_offsets = [-8, 8, -1, 1, -9, -7, 7, 9] # Directions for index offset - N, S, E, W, NE, NW, SE, SW
num_squares_to_edge = {}
for square_index in range(SQUARE_COUNT):
    x = get_X(square_index)
    y = get_Y(square_index)
    num_north = y
    num_south = 7 - y
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
       
       
def legal_moves(game_state, piece_index):
    turn = game_state.turn
    piece = game_state.board.board_pos[piece_index]
    if piece.player != game_state.turn:
        print('{} turn not {}'.format(game_state.turn.upper(), piece.player.upper()))
        return []      
    
    legal_moves = []
    if piece.notation == 'P':
        return legal_pawn_moves(game_state, piece_index)
    elif piece.notation == 'R':
        return legal_rook_moves(game_state, piece_index)
    elif piece.notation == 'N':
        return legal_knight_moves(game_state, piece_index)
    elif piece.notation == 'B':
        return legal_bishop_moves(game_state, piece_index)
    elif piece.notation == 'Q':
        return legal_rook_moves(game_state, piece_index) + legal_bishop_moves(game_state, piece_index)
    elif piece.notation == 'K':
        print(legal_king_moves(game_state, piece_index))
        return legal_king_moves(game_state, piece_index)
    
def legal_pawn_moves(game_state, piece_index):
    piece = game_state.board.board_pos[piece_index]
    legal_moves = []
    if piece.player == 'w':
        forward = -8
        captures = [piece_index - 7, piece_index - 9]
    else:
        forward = 8
        captures = [piece_index + 7, piece_index + 9]
    forward_max = 1
    if piece.has_not_moved():
        forward_max = 2
    for i in range(forward_max):
        target_index = piece_index + forward * (i + 1)
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            break
        legal_moves += [target_index]
    for target_index in captures:
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if piece.player != target_square.player:
                legal_moves += [target_index]
    return legal_moves
        
def legal_knight_moves(game_state, piece_index):
    piece = game_state.board.board_pos[piece_index]
    turn = piece.player
    legal_moves = []
    direction_max = num_squares_to_edge[piece_index]
    num_north = direction_max[0]
    num_south = direction_max[1]
    num_east = direction_max[2]
    num_west = direction_max[3]
    if num_east >= 2 and num_north >= 1:
        target_index = piece_index - 10
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    if num_east >= 1 and num_north >= 2:
        target_index = piece_index - 17
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    if num_west >= 1 and num_north >= 2:
        target_index = piece_index - 15
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    if num_west >= 2 and num_north >= 1:
        target_index = piece_index - 6
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    if num_west >= 2 and num_south >= 1:
        target_index = piece_index +10
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    if num_west >= 1 and num_south >= 2:
        target_index = piece_index + 17
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    if num_east >= 1 and num_south >= 2:
        target_index = piece_index + 15
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    if num_east >= 2 and num_south >= 1:
        target_index = piece_index + 6
        target_square = get_square(game_state, target_index)
        if is_piece(target_square):
            if not piece.player == target_square.player:
                legal_moves += [target_index]
        else:
            legal_moves += [target_index]
    return legal_moves

def legal_king_moves(game_state, piece_index):
    piece = game_state.board.board_pos[piece_index]
    turn = piece.player
    legal_moves = []
    
    directions = 8
    for direction_index in range(directions):
        offset = sliding_offsets[direction_index]
        direction_max = num_squares_to_edge[piece_index][direction_index]
        print(offset, direction_max)
        if direction_max > 0:
            target_index = piece_index + offset
            target_square = get_square(game_state, target_index)
            if is_piece(target_square):
                # If target piece player is same, it's blocked 
                if piece.player == target_square.player:
                    continue
                # If target piece player is different, it's captured 
                else:
                    legal_moves += [target_index]
                    continue
            legal_moves += [target_index]
            
    return legal_moves
            
        
    
    
    

def legal_rook_moves(game_state, piece_index):
    piece = game_state.board.board_pos[piece_index]
    turn = piece.player
    legal_moves = []
    
    directions = 4
    for direction_index in range(directions):
        offset = sliding_offsets[direction_index]
        direction_max = num_squares_to_edge[piece_index][direction_index]
        for i in range(direction_max):
            target_index = piece_index + offset * (i + 1)
            target_square = get_square(game_state, target_index)
            
            if is_piece(target_square):
                # If target piece player is same, it's blocked 
                if piece.player == target_square.player:
                    break
                # If target piece player is different, it's captured 
                else:
                    legal_moves += [target_index]
                    break
            legal_moves += [target_index]
    return legal_moves
            
def legal_bishop_moves(game_state, piece_index):
    piece = game_state.board.board_pos[piece_index]
    turn = piece.player
    legal_moves = []
    
    directions = 4
    for direction_index in range(directions):
        offset = sliding_offsets[4 + direction_index]

        direction_max = num_squares_to_edge[piece_index][4 + direction_index]
        for i in range(direction_max):
            
            target_index = piece_index + offset * (i + 1)
            target_square = get_square(game_state, target_index)
            
            if is_piece(target_square):
                # If target piece player is same, it's blocked 
                if piece.player == target_square.player:
                    break
                # If target piece player is different, it's captured 
                else:
                    legal_moves += [target_index]
                    break
            legal_moves += [target_index]
    return legal_moves
    