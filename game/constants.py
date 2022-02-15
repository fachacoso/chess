import pieces.pawn
import pieces.rook
import pieces.knight
import pieces.bishop
import pieces.queen
import pieces.king

# BOARD CONSTANTS
SQUARE_COUNT = 64
FILE = RANK = 8

# NOTATION CONSTANTS
INSTANCE_NOTATION_DICTIONARY = {
    'P': pieces.pawn.Pawn,
    'R': pieces.rook.Rook,
    'N': pieces.knight.Knight,
    'B': pieces.bishop.Bishop,
    'Q': pieces.queen.Queen,
    'K': pieces.king.King
    }

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

STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

FILE_TO_NUM_DICTIONARY = {
    'a': 0,
    'b': 1,
    'c': 2,
    'd': 3,
    'e': 4,
    'f': 5,
    'g': 6,
    'h': 7
    }

NUM_TO_FILE_DICTIONARY = {
    0: 'a',
    1: 'b',
    2: 'c',
    3: 'd',
    4: 'e',
    5: 'f',
    6: 'g',
    7: 'h'
    }

# Helper var for pawn promotions
FIRST_RANK_INDEXES = [0, 1, 2, 3, 4, 5, 6, 7]
EIGHT_RANK_INDEXES = [56, 57, 58, 59, 60, 61, 62, 63]
