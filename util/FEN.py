from constants import *
from square import Square
from util.utils import coordinate_to_index


class FEN:
    """
    FEN notation describes board positions in a chess game

    FEN notation consists of:
    <Piece Placement>
    <Side to move>
    <Castling ability>
    <En passant target square>
    <Halfmove clock>
    <Fullmove count>

    ex. rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq c6 0 2

    More information found on this link:  https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation
    """

    def __init__(self, FEN):
        """Initialize FEN object from FEN string

        Args:
            FEN ([string]): FEN representation of game state
        """
        # Parse FEN string
        FEN_list                = FEN.split()
        board_string            = FEN_list[0]
        turn_string             = FEN_list[1]
        castling_string         = FEN_list[2]
        en_passant_string       = FEN_list[3]
        halfmove_count_string = FEN_list[4]
        turn_count_string     = FEN_list[5]
        
        # Set attributes
        self.string           = FEN
        self.board            = self.get_board(board_string)
        self.turn             = self.get_turn(turn_string)
        self.castling         = self.get_castling(castling_string)
        self.en_passant       = self.get_en_passant(en_passant_string)
        self.halfmove_count = self.get_halfmove_count(halfmove_count_string)
        self.turn_count     = self.get_turn_count(turn_count_string)

    def get_board(self, piece_placement):
        """Convert string to a GameState board

        Args:
            piece_placement (string): FEN notation of piece placement

        Returns:
            Square[64]: Board with initialized pieces
        """
        board          = []
        position_stack = []
        current_rank   = []
        current_index  = 55
        for char in piece_placement:
            if char.isupper():
                piece  = INSTANCE_NOTATION_DICTIONARY[char]
                square = Square(piece(current_index, "w"))
                current_rank.append(square)
                current_index += 1
            elif char.islower():
                piece  = INSTANCE_NOTATION_DICTIONARY[char.upper()]
                square = Square(piece(current_index, "b"))
                current_rank.append(square)
                current_index += 1
            elif char.isnumeric():
                for i in range(int(char)):
                    current_rank.append(Square())
                    current_index += 1
            else:
                position_stack.append(current_rank)
                current_rank   = []
                current_index -= 16
        position_stack.append(current_rank)
        for _ in range(RANK):
            rank = position_stack.pop()
            board.extend(rank)
        return board

    def get_castling(self, castling):
        """Convert castling string to list for castling rights

        Args:
            castling (string): FEN notation of castling rights

        Returns:
            bool[4]: list of booleans representing ability to castle
        """
        return ["K" in castling, "Q" in castling, "k" in castling, "q" in castling]

    def get_en_passant(self, coordinate):
        """Convert coordinate to respective index

        Args:
            coordinate (string): algebraic notation of en passant target square

        Returns:
            int: index of en passant target square if any
        """        
        if coordinate == "-":
            return None
        return coordinate_to_index(coordinate)

    def get_turn(self, turn_string):
        """Return turn_string
        """
        return turn_string

    def get_halfmove_count(self, halfmove_count_string):
        # Halfmove - moves since last pawn move or capture
        return int(halfmove_count_string)

    def get_turn_count(self, turn_count):
        return int(turn_count)
