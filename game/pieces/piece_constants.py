import util.utils as util

SQUARE_COUNT = 64

# Index offset for each direction - N, S, E, W, NE, NW, SE, SW
SLIDING_OFFSETS = [8, -8, -1, 1, 7, 9, -9, -7] 
NUM_SQUARES_TO_EDGE = {}
for square_index in range(SQUARE_COUNT):
    x = util.get_x(square_index)
    y = util.get_y(square_index)
    num_north = 7 - y
    num_south = y
    num_east = x
    num_west = 7 - x
    NUM_SQUARES_TO_EDGE[square_index] = [
        num_north,
        num_south,
        num_east,
        num_west,
        min(num_north, num_east),
        min(num_north, num_west),
        min(num_south, num_east),
        min(num_south, num_west)
    ]
    
    
UNICODE_SYMBOLS = {
                'wP':'♙',
                'wR':'♖',
                'wN':'♘',
                'wB':'♗',
                'wQ':'♕',
                'wK':'♔',                         
                'bP':'♟︎',
                'bR':'♜',
                'bN':'♞',
                'bB':'♝',
                'bQ':'♛',
                'bK':'♚'
                }

# Helper var for Castling rights
WHITE_KING_INDEX = 4
WHITE_ROOK_K_INDEX = 7
WHITE_ROOK_Q_INDEX = 0
BLACK_KING_INDEX = 60
BLACK_ROOK_K_INDEX = 63
BLACK_ROOK_Q_INDEX = 56