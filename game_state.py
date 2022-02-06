from move import Move, moves
from util.utils import *
from util.FEN import FEN
from constants import *

  
class GameState:
    '''
    GameState object reflects state of game

    Parameters
    ----------
    FEN_string : str
        FEN notation of board state
        
    Attributes
    ----------
    board : Square[64]
        list of Square objects representing board
    turn : str
        player to move ('w' or 'b')
    castling : bool[4]
        rights to castle
    en_passant : int
        target index for en passant
    halfmove_counter : int
        counter for halfmove
    turn_counter : int
        counter for turn
    current_FEN : FEN
        FEN object that represents current game state
    FEN_history : FEN[]
        list of previous FEN's
    move_history : Move[]
        list of previous moves
    history_counter : int
        index of current board viewed, used for viewing previous moves
    
    Methods
    -------
    info(additional=""):
        Prints the person's name and age.
    
    '''
    def __init__(self, FEN_string=STARTING_FEN):
        # Initializes starting board using FEN notation string
        self.current_FEN = FEN(FEN_string)
        self.set_attributes_from_FEN()
        self.move_history = []
        self.history_counter = self.turn_counter
        
    
    # FEN methods
    def set_attributes_from_FEN(self):
        ''' Load game_state attributes from current_FEN '''
        self.__dict__.update(self.current_FEN.__dict__)
    
    def get_updated_FEN(self):
        ''' Return new FEN notation after move '''
        new_FEN = FEN(self.__repr__())
        return new_FEN

    def is_legal_move(self, start_index, end_index):
        return end_index in moves(self, start_index)

    def get_square(self, index):
        return self.board[index]

    def move(self, start_index, end_index):
        start_square = self.get_square(start_index)
        end_square = self.get_square(end_index)
        piece = start_square.get_piece()

        if piece.player != self.turn:
            return

        if not self.is_legal_move(start_index, end_index):
            return

        # Record if a piece was captured
        captured_piece = None
        en_passant_capture = False
        if end_square.is_empty():
            # If en passant capture
            if piece.notation == "P" and end_index == self.en_passant:
                en_passant_capture = True
                if piece.player == "W":
                    captured_index = end_index + 8
                else:
                    captured_index = end_index - 8
                captured_square = self.get_square(captured_index)
                captured_piece = captured_square.get_piece()
        # Stores captured piece
        else:
            captured_piece = end_square.get_piece()

        # Castle move check
        if piece.notation == "K" and abs(start_index - end_index) == 2:
            castle_index = (start_index + end_index) // 2
            self.castle_move(castle_index)

        # Update GameState
        self.history_counter += 1
        self.update_turn()
        self.update_en_passant(piece, start_index, end_index)
        self.update_castling(piece)
        self.update_halfmove(piece, captured_piece)

        # Update Start and End Square
        start_square.remove_piece()
        end_square.set_piece(piece)
        if en_passant_capture:
            captured_square.remove_piece()

        # Update Piece
        piece.move(end_index)
        if piece.notation == "P":
            if end_index in FIRST_RANK_INDEXES or end_index in EIGHT_RANK_INDEXES:
                end_square.promote_piece(end_index, "Q")

        # Create Move Instance
        """check = is_check(self, self.player)"""
        move = Move(
            piece,
            start_index,
            end_index,
            captured_piece,
            self.castling,
            self.en_passant,
            False,
        )
        self.move_history.append(move)

    def castle_move(self, end_index):
        # Key - end index | Val - rook index
        # ! bK castling not working
        castle_dic = {3: 0, 5: 7, 61: 63, 59: 56}
        start_square = self.get_square(castle_dic[end_index])
        piece = start_square.get_piece()
        end_square = self.get_square(end_index)
        start_square.remove_piece()
        end_square.set_piece(piece)
        piece.move(end_index)

    def update_turn(self, undo=False):
        if undo:
            self.turn_counter -= 1
        else:
            self.turn_counter += 1
        self.turn = "w" if self.turn == "b" else "b"

    def update_en_passant(self, piece, start_index, end_index):
        if piece.notation == "P":
            # Adds en passant when pawn moves forward twice
            if abs(start_index - end_index) == 16:
                self.en_passant = (start_index + end_index) // 2
        else:
            self.en_passant = None

    def update_castling(self, piece):

        # Checks if specified piece is elligible for castling
        def validate_piece(index, piece_notation, player):
            square = self.get_square(index)
            if not square.is_empty():
                piece = square.get_piece()
                if piece.notation == piece_notation and piece.player == player:
                    if not piece.has_moved():
                        return True
            return False

        if piece.notation == "K" or piece.notation == "R":
            castle_list = [False, False, False, False]
            if validate_piece(WHITE_KING_INDEX, "K", "w"):
                if validate_piece(WHITE_ROOK_K_INDEX, "R", "w"):
                    castle_list[0] = True
                if validate_piece(WHITE_ROOK_Q_INDEX, "R", "w"):
                    castle_list[1] = True

            # Check black castling rights
            if validate_piece(BLACK_KING_INDEX, "K", "b"):
                if validate_piece(BLACK_ROOK_K_INDEX, "R", "b"):
                    castle_list[2] = True
                if validate_piece(BLACK_ROOK_Q_INDEX, "R", "b"):
                    castle_list[3] = True

            self.castling = castle_list

    def update_halfmove(self, piece, captured_piece):
        if piece.notation == "P" or captured_piece != None:
            self.halfmove_counter = 0
        else:
            self.halfmove_counter += 1

    # Unicode representation of board
    def __str__(self):
        string = ""
        stack = []
        for rank in range(RANK):
            current_rank = []
            for file in range(FILE):
                index = xy_to_index(file, rank)
                current_rank.append(self.get_square(index).__str__())
            stack.append(current_rank)
        for _ in range(RANK):
            string += " ".join(stack.pop())
            string += "\n"
        return string

    # FEN notation
    def __repr__(self):
        FEN_list = []

        # Piece Placement
        piece_placement = ""
        string = ""
        stack = []
        for rank in range(RANK):
            current_rank = []
            for file in range(FILE):
                index = xy_to_index(file, rank)
                current_rank.append(self.get_square(index).__repr__())
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
                    piece_placement += str(dash_count)
                    dash_count = 0
            piece_placement += char
        FEN_list.append(piece_placement)

        # Turn
        FEN_list.append(self.turn)

        # Castling
        castling_string_list = ["KQkq"[i] for i in range(4) if self.castling[i]]
        FEN_list.append("".join(castling_string_list))

        # En Passant Square
        FEN_list.append(index_to_coordinate(self.en_passant))

        # Halfmove Counter
        FEN_list.append(str(self.halfmove_counter))

        # Turn(Fullmove) Counter
        FEN_list.append(str(self.turn_counter))

        return " ".join(FEN_list)
