from pieces import *

# BOARD CONSTANTS
SQUARE_COUNT = 64
FILE = RANK = 8

# NOTATION CONSTANTS
NOTATION = {'P': Pawn, 'R': Rook, 'N': Knight, 'B': Bishop, 'Q': Queen, 'K': King}

FEN_NOTATION = {
                'wP':'P',
                'wR':'R',
                'wN':'N',
                'wB':'B',
                'wQ':'Q',
                'wK':'K',                         
                'bP':'p',
                'bR':'r',
                'bN':'n',
                'bB':'b',
                'bQ':'q',
                'bK':'k'
                }

STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

FILE_TO_NUM_DICTIONARY = {'a': 1,
                    'b': 2,
                    'c': 3,
                    'd': 4,
                    'e': 5,
                    'f': 6,
                    'g': 7,
                    'h': 8
                    }

NUM_TO_FILE_DICTIONARY = {0: 'a',
                    1: 'b',
                    2: 'c',
                    3: 'd',
                    4: 'e',
                    5: 'f',
                    6: 'g',
                    7: 'h'
                    }