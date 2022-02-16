from msilib.schema import Error
import move
import util.utils as util
import util.FEN as FEN_util
import constants
import pieces.piece_constants as piece_constants

  
class GameState:
    '''
    GameState object reflects state of game

    Parameters
    ----------
    FEN_string : str
        FEN notation of board state
        
    Attributes
    ----------
    board : list[Square()] (64)
        list of Square objects representing board
    turn : str
        player to move ('w' or 'b')
    castling : list[bool] (4)
        rights to castle
    en_passant : int
        target index for en passant
    halfmove_count : int
        count for halfmove
    fullmove_count : int
        count for fullmove
    turn_count : int
        count for each turn
    current_FEN : FEN
        FEN object that represents current game state
    FEN_history : FEN[]
        list of previous FEN's
    move_history : list[Move()]
        list of previous moves
    history_count : int
        index of current board viewed, used for viewing previous moves
    captured : list[Piece()]
        list of pieces captured
    
    Methods
    -------
    clone_game_state(self)
        makes copy of GameState
    
    move(self, start_index, end_index)
        makes a move
        
    set_attributes_from_FEN(self)
        load GameState attribute from current_FEN
        
    update_game_state(self, piece, start_index, end_index, captured_piece)
        updates instance attributes
    '''
    def __init__(self, FEN_string = constants.STARTING_FEN):
        # Initializes starting board using FEN notation string
        current_FEN = FEN_util.FEN(FEN_string)
        current_FEN.load_FEN_string(self)
        self.FEN_history      = []
        self.move_history     = []
        self.history_count    = 0
        for square in self.board:
            if not square.is_empty():
                piece = square.get_piece()
                if piece.notation == 'K':
                    if piece.player == 'w':
                        self.white_king_index = piece.index
                    else: 
                        self.black_king_index = piece.index
                        
        self.attacked_squares     = move.Move.get_attacked_squares(self)
        self.pinned_lines         = move.Move.get_pinned_lines(self)
        self.checking_piece_index = move.Move.get_checking_piece_index(self)
        self.defended_squares     = move.Move.get_defended_squares(self)
        self.legal_moves          = move.Move.get_all_legal_moves(self)
        
        
        self.game_over = self.check_game_over()

        
    # Move methods
    def make_move(self, start_index, end_index):
        if type(start_index) == str and type(end_index) == str:
            start_index = util.coordinate_to_index(start_index)
            end_index = util.coordinate_to_index(end_index)
        start_square = self.get_square(start_index)
        end_square   = self.get_square(end_index)
        piece        = start_square.get_piece()
        
        # ? Can I just put the dictionary in move?
        non_FEN_attributes = {'attacked_squares': self.attacked_squares,
                              'pinned_lines': self.pinned_lines,
                              'checking_piece_index': self.checking_piece_index,
                              'legal_moves': self.legal_moves,
                              'defended_squares': self.defended_squares
                              }

        if start_square.is_empty():
            print("ERROR No piece on index {}".format(start_index))
            return False
            

        if not move.Move.is_legal_move(self, start_index, end_index):
            print("ERROR Piece on index {} moving to index {} NOT LEGAL".format(start_index, end_index))
            return False

        # Check capture
        captured_piece = None
        if end_square.is_empty():
            # If en passant capture
            if piece.notation == "P" and end_index == self.en_passant:
                if piece.player == "W":
                    captured_index = end_index + 8
                else:
                    captured_index = end_index - 8
                captured_piece = self.capture_piece(captured_index)
        # Stores captured piece
        else:
            captured_piece = self.capture_piece(end_index)
            
        # Move
        start_square.move_piece(end_square)
        
        # Castle move check
        if piece.notation == "K" and abs(start_index - end_index) == 2:
            castle_index = (start_index + end_index) // 2
            self.castle_move(castle_index)

        # Update GameState
        self.next_turn()
        self.update_game_state(piece, start_index, end_index, captured_piece)
        self.check_game_over()


        # Create Move Instance
        move_obj = move.Move(
            piece,
            start_index,
            end_index,
            captured_piece,
            self.checking_piece_index,
            non_FEN_attributes
        )
        self.move_history.append(move_obj)
        print(self.current_FEN)
        
        return True

    def undo_move(self):
        if len(self.move_history) > 0:
            last_move     = self.move_history.pop()
            current_index = last_move.end
            prev_index    = last_move.start
            
            current_square = self.get_square(current_index)
            prev_square    = self.get_square(prev_index)
            current_square.undo_move_piece(prev_square)
            
            captured_piece = last_move.captured
            if captured_piece:
                captured_square = self.get_square(captured_piece.index)
                captured_square.set_piece(captured_piece)
            
            last_FEN = self.FEN_history.pop()
            last_FEN.load_FEN_string(self)
            
            self.__dict__.update(last_move.non_FEN_attributes)
            
            print(self.current_FEN)
            
    def check_game_over(self):
        if len(self.legal_moves) == 0:
            if type(self.checking_piece_index) == int:
                self.game_over = 'Checkmate'
            else:
                self.game_over = 'Stalemate'
            print('Game over! {}'.format(self.game_over))
        else:
            self.game_over = ''
        



    def capture_piece(self, captured_index):
        """Remove captured piece on captured index and return it

        Args:
            captured_index (int): index of piece captured

        Returns:
            Piece: piece object of captured piece
        """        
        square = self.get_square(captured_index)
        piece = square.get_piece()
        square.remove_piece()
        return piece
    
    

    def castle_move(self, end_index):
        """Move rook when castling

        Args:
            end_index (int): target index of rook
        """
        castle_dic = {3: 0, 5: 7, 61: 63, 59: 56}
        start_index = castle_dic[end_index]
        self.move_piece(start_index, end_index)


    """
    UPDATE FUNCTIONS 
    Used for updating GameState after move
    """
    def update_game_state(self, piece, start_index, end_index, captured_piece):
        self.update_en_passant(piece, start_index, end_index)
        self.update_castling(piece)
        self.update_halfmove(piece, captured_piece)
        self.update_FEN()
        self.update_attacked_squares()
        self.update_pinned_lines()
        self.update_checking_piece_index()
        self.update_legal_moves()
        self.update_defended_squares()
    
    def next_turn(self):
        self.turn_count += 1
        self.turn = 'w' if self.turn == 'b' else 'b'
        self.fullmove_count == (self.turn_count // 2) + 1
            

    def update_en_passant(self, piece, start_index, end_index):
        if piece.notation == "P":
            # Adds en passant when pawn moves forward twice
            if abs(start_index - end_index) == 16:
                self.en_passant = (start_index + end_index) // 2
            else:
                self.en_passant = None
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
            if validate_piece(piece_constants.WHITE_KING_INDEX, "K", "w"):
                if validate_piece(piece_constants.WHITE_ROOK_K_INDEX, "R", "w"):
                    castle_list[0] = True
                if validate_piece(piece_constants.WHITE_ROOK_Q_INDEX, "R", "w"):
                    castle_list[1] = True

            # Check black castling rights
            if validate_piece(piece_constants.BLACK_KING_INDEX, "K", "b"):
                if validate_piece(piece_constants.BLACK_ROOK_K_INDEX, "R", "b"):
                    castle_list[2] = True
                if validate_piece(piece_constants.BLACK_ROOK_Q_INDEX, "R", "b"):
                    castle_list[3] = True

            self.castling = castle_list

    def update_halfmove(self, piece, captured_piece):
        if piece.notation == "P" or captured_piece != None:
            self.halfmove_count = 0
        else:
            self.halfmove_count += 1

    def update_FEN(self):
        self.FEN_history.append(self.current_FEN)
        new_FEN = FEN_util.FEN.create_FEN_string(self)
        self.current_FEN = FEN_util.FEN(new_FEN, self.board)
        
    def update_attacked_squares(self):
        self.attacked_squares = move.Move.get_attacked_squares(self)
        
    def update_pinned_lines(self):
        self.pinned_lines = move.Move.get_pinned_lines(self)
        
    def update_checking_piece_index(self):
        self.checking_piece_index = move.Move.get_checking_piece_index(self)
        
    def update_legal_moves(self):
        self.legal_moves = move.Move.get_all_legal_moves(self)
        
    def update_defended_squares(self):
        self.defended_squares = move.Move.get_defended_squares(self)
        

    # Unicode representation of board
    def __str__(self):
        # ! unicode errors
        string = ""
        stack = []
        for rank in range(constants.RANK):
            current_rank = []
            for file in range(constants.FILE):
                index = util.xy_to_index(file, rank)
                current_rank.append(self.get_square(index).__str__())
            stack.append(current_rank)
        for _ in range(constants.RANK):
            string += " ".join(stack.pop())
            string += "\n"
        return string

    # FEN notation
    def __repr__(self):
        return str(self.current_FEN)



    def get_square(self, index):
        return self.board[index]
    