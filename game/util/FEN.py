from constants import *
from square import Square
from util.utils import coordinate_to_index, xy_to_index, index_to_coordinate


class FEN:
    """
    FEN object holds FEN notation: describes board positions in a chess game
    More information found on this link:  https://en.wikipedia.org/wiki/Forsyth–Edwards_Notation

    FEN notation consists of:
    <Piece Placement>
    <Side to move>
    <Castling ability>
    <En passant target square>
    <Halfmove count>
    <Fullmove count>
    """
    
    def __init__(self, FEN):
        """Initialize FEN object from FEN string

        Args:
            FEN ([string]): FEN representation of game state
        """
        # Parse FEN string
        FEN_list              = FEN.split()
        board_string          = FEN_list[0]
        turn_string           = FEN_list[1]
        castling_string       = FEN_list[2]
        en_passant_string     = FEN_list[3]
        halfmove_count_string = FEN_list[4]
        turn_count_string     = FEN_list[5]
        
        # Set attributes
        self.FEN_string     = FEN
        self.board          = self.read_board(board_string)
        self.turn           = self.read_turn(turn_string)
        self.castling       = self.read_castling(castling_string)
        self.en_passant     = self.read_en_passant(en_passant_string)
        self.halfmove_count = self.read_halfmove_count(halfmove_count_string)
        self.turn_count     = self.read_turn_count(turn_count_string)
        
    @classmethod
    def load_FEN_string(cls, game_state, FEN_string):
        ''' Load GameState attributes from FEN_string '''
        game_state.current_FEN = FEN(FEN_string)
        game_state.__dict__.update(game_state.current_FEN.__dict__)
    
    def __str__(self):
        return self.FEN_string

    """
    READ FUNCTIONS 
    Used for loading GameState from FEN string
    """
    def read_board(self, piece_placement):
        """Convert string to a GameState board

        Args:
            piece_placement (string): FEN notation of piece placement

        Returns:
            Square[64]: Board with initialized pieces
        """
        board          = []
        position_stack = []
        current_rank   = []
        current_index  = 56
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

    def read_castling(self, castling):
        """Convert castling string to list for castling rights

        Args:
            castling (string): FEN notation of castling rights

        Returns:
            bool[4]: list of booleans representing ability to castle
        """
        return ["K" in castling, "Q" in castling, "k" in castling, "q" in castling]

    def read_en_passant(self, coordinate):
        """Convert coordinate to respective index

        Args:
            coordinate (string): algebraic notation of en passant target square

        Returns:
            int: index of en passant target square if any
        """        
        if coordinate == "-":
            return None
        return coordinate_to_index(coordinate)

    def read_turn(self, turn_string):
        """Return turn_string
        """
        return turn_string

    def read_halfmove_count(self, halfmove_count_string):
        """ Halfmove - moves since last pawn move or capture """
        return int(halfmove_count_string)

    def read_turn_count(self, turn_count):
        """ How many turns passed in game"""
        return int(turn_count)

    
    """
    CREATE FUNCTIONS
    Used for creating FEN string from GameState
    """
    @classmethod
    def create_FEN_string(cls, game_state):
        ''' Return new FEN notation after move '''
        FEN_list = []
        FEN_list.append(FEN.create_board(game_state))
        FEN_list.append(FEN.create_turn(game_state))
        FEN_list.append(FEN.create_castling(game_state))
        FEN_list.append(FEN.create_en_passant(game_state))
        FEN_list.append(FEN.create_halfmove_count(game_state))
        FEN_list.append(FEN.create_turn_count(game_state))
        return " ".join(FEN_list)
    
    @classmethod
    def create_board(cls, game_state):
        FEN_string = ''
        string     = ""
        stack      = []
        for rank in range(RANK):
            current_rank = []
            for file in range(FILE):
                index = xy_to_index(file, rank)
                current_rank.append(game_state.get_square(index).__repr__())
            stack.append(current_rank)
        for rank in range(RANK):
            string += "".join(stack.pop())
            if rank < 7:
                string += "/"
        dash_count = 0
        for char in string:
            if char == "-":
                dash_count += 1
                continue
            else:
                if dash_count > 0:
                    FEN_string += str(dash_count)
                    dash_count = 0
            FEN_string += char
        if dash_count > 0:
            FEN_string += str(dash_count)
        return FEN_string
    
    @classmethod
    def create_turn(cls, game_state):
        FEN_string = game_state.turn
        return FEN_string

    @classmethod
    def create_castling(cls, game_state):
        FEN_string = ''
        castling_string_list = ["KQkq"[i] for i in range(4) if game_state.castling[i]]
        if any(castling_string_list) == False:
            castling_string_list = '-'
        FEN_string = "".join(castling_string_list)
        return FEN_string
    
    @classmethod
    def create_en_passant(cls, game_state):
        FEN_string = ''
        if game_state.en_passant == None:
            FEN_string = '-'
        else:
            FEN_string = index_to_coordinate(game_state.en_passant)
        return FEN_string
    
    @classmethod
    def create_halfmove_count(cls, game_state):
        FEN_string = str(game_state.halfmove_count)
        return FEN_string
    
    @classmethod
    def create_turn_count(cls, game_state):
        FEN_string = str(game_state.turn_count)
        return FEN_string