import pieces.pawn
import pieces.rook
import pieces.knight
import pieces.bishop
import pieces.queen
import pieces.king

"""
BOARD CONSTANTS
"""
SQUARE_COUNT = 64
FILE = RANK = 8

"""
NOTATION CONSTANTS
"""
# Notation to Piece Initialization
INSTANCE_NOTATION_DICTIONARY = {
    'P': pieces.pawn.Pawn,
    'R': pieces.rook.Rook,
    'N': pieces.knight.Knight,
    'B': pieces.bishop.Bishop,
    'Q': pieces.queen.Queen,
    'K': pieces.king.King
    }

# Piece to Fen Notation
FEN_NOTATION = {
    'wP': 'P',
    'wR': 'R',
    'wN': 'N',
    'wB': 'B',
    'wQ': 'Q',
    'wK': 'K',
    'bP': 'p',
    'bR': 'r',
    'bN': 'n',
    'bB': 'b',
    'bQ': 'q',
    'bK': 'k'
    }

"""
STARTING FEN CONSTANT
"""
STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'


"""
PAWN CONSTANTS
"""
# Pawn promotion
FIRST_RANK_INDEXES = [0, 1, 2, 3, 4, 5, 6, 7]
EIGHT_RANK_INDEXES = [56, 57, 58, 59, 60, 61, 62, 63]

# Double forward
SECOND_RANK_INDEXES  = [8, 9, 10, 11, 12, 13, 14, 15]
SEVENTH_RANK_INDEXES = [48, 49, 50, 51, 52, 53, 54, 55]