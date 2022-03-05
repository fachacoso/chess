from msilib.schema import Error

import move
import util.utils as util
import util.FEN as FEN_util
import constants
import pieces.piece_constants as piece_constants
import pieces.pawn as pawn

  
class GameState:
    '''
    GameState object reflects state of game

    Parameters
    ----------
    FEN_string : str
        FEN notation of board state
        
    Attributes
    ----------
    FEN Attributes
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
        
    attacked_squares : list[int]
        squares being attacked by opponent
        
    defended_squares : list[int]
        squares containing enemy pieces current king cannot move to
        
    checking_piece_list : list[Piece()] (2, 1, 0)
        pieces checking current player's king
        
    legal_moves : dic{ key = piece_index : val = list[target_index]}
        dictionary  of all moves
        
    game_over : str
        'Checkmate' / 'Stalemate' / 'Draw'
    
    Methods
    -------
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
                        
        self.attacked_squares, self.defended_squares, self.pinned, self.checking_pieces = move.Move.get_attacked_defended_pinned_check(self)
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
        
        non_FEN_attributes = {'attacked_squares': self.attacked_squares,
                              'defended_squares': self.defended_squares,
                              'legal_moves'     : self.legal_moves,
                              'white_king_index': self.white_king_index,
                              'black_king_index': self.black_king_index
                              }

        if start_square.is_empty():
            print("ERROR No piece on index {}".format(start_index))
            return False
            

        if not move.Move.is_legal_move(self, start_index, end_index):
            print("ERROR Piece on index {} moving to index {} NOT LEGAL".format(start_index, end_index))
            return False

        # CAPTURE
        captured_piece = None
        if end_square.is_empty():
            # EN PASSANT
            if piece.notation == "P" and end_index == self.en_passant:
                if piece.player == "W":
                    captured_index = end_index + 8
                else:
                    captured_index = end_index - 8
                captured_piece = self.capture_piece(captured_index)
        else:
            captured_piece = self.capture_piece(end_index)
            
        # MOVE
        start_square.move_piece(end_square)
        
        # CASTLE MOVE CHECK
        if piece.notation == "K" and abs(start_index - end_index) == 2:
            castle_index = (start_index + end_index) // 2
            self.castle_move(castle_index)

        # UPDATE GAMESTATE
        self.next_turn()
        self.update_game_state(piece, start_index, end_index, captured_piece)
        self.check_game_over()


        # MOVE OBJECT
        move_obj = move.Move(
            piece,
            start_index,
            end_index,
            captured_piece,
            self.checking_pieces,
            self.game_over,
            non_FEN_attributes
        )
        self.move_history.append(move_obj)
        
        return True

    def undo_move(self):
        if len(self.move_history) > 0:
            # GET LAST MOVE
            last_move     = self.move_history.pop()
            current_index = last_move.end
            prev_index    = last_move.start
            current_square = self.get_square(current_index)
            prev_square    = self.get_square(prev_index)
            
            # UNDO CASTLE MOVE - if last move was castle
            if current_square.get_piece().notation == "K" and abs(current_index - prev_index) == 2:
                castle_index = (current_index + prev_index) // 2
                self.undo_castle_move(castle_index)
                
            # MOVE PIECE BACK
            current_square.undo_move_piece(prev_square)
            
            # PLACE CAPTURE PIECE - if last move captured
            captured_piece = last_move.captured
            if captured_piece:
                captured_square = self.get_square(captured_piece.index)
                captured_square.set_piece(captured_piece)
                captured_piece.captured = False
            
            # UPDATE FEN
            last_FEN = self.FEN_history.pop()
            last_FEN.load_FEN_string(self)
            self.__dict__.update(last_move.non_FEN_attributes)
            
            
    def check_game_over(self):
        if len(self.legal_moves) == 0:
            if len(self.checking_pieces) > 0:
                self.game_over = 'Checkmate'
            else:
                self.game_over = 'Stalemate'
            print('Game over! {}'.format(self.game_over))
        else:
            self.game_over = None
        



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
        piece.captured = True
        return piece
    
    

    def castle_move(self, end_index):
        """Move rook when castling

        Args:
            end_index (int): target index of rook
        """
        castle_dic   = {3: 0, 5: 7, 61: 63, 59: 56}
        start_index  = castle_dic[end_index]
        start_square = self.get_square(start_index)
        end_square   = self.get_square(end_index)
        start_square.move_piece(end_square)
        
    def undo_castle_move(self, prev_end_index):
        castle_dic   = {3: 0, 5: 7, 61: 63, 59: 56}
        prev_start_index  = castle_dic[prev_end_index]
        prev_start_square = self.get_square(prev_start_index)
        prev_end_square   = self.get_square(prev_end_index)
        prev_end_square.undo_move_piece(prev_start_square)


    """
    UPDATE FUNCTIONS 
    Used for updating GameState after move
    """
    def update_game_state(self, piece, start_index, end_index, captured_piece):
        self.update_castling(piece)
        self.update_halfmove(piece, captured_piece)
        self.update_king_index(start_index, end_index)
        self.update_movement()
        self.update_en_passant(piece, start_index, end_index)
        self.update_FEN()
        self.update_legal_moves()
    
    def next_turn(self):
        self.turn_count += 1
        self.turn = 'w' if self.turn == 'b' else 'b'
        self.fullmove_count = (self.turn_count // 2) + 1
            

    def update_en_passant(self, piece_moved, start_index, end_index):
        if piece_moved.notation == "P":
            # Possible en passant if double forward
            if abs(start_index - end_index) == 16:
                possible_en_passant = (start_index + end_index) // 2
                
                pieces = piece_moved.white_pieces if self.turn == 'w' else piece_moved.black_pieces
                for piece in pieces:
                    if piece.notation == 'P':
                        # If player pawn can capture en passant square, record square
                        if possible_en_passant in piece.attacked_squares:
                            self.en_passant = end_index
                            return
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
        if isinstance(piece, pawn.Pawn) or captured_piece != None:
            self.halfmove_count = 0
        else:
            self.halfmove_count += 1

    def update_FEN(self):
        self.FEN_history.append(self.current_FEN)
        new_FEN = FEN_util.FEN.create_FEN_string(self)
        self.current_FEN = FEN_util.FEN(new_FEN, self.board)
        
    def update_movement(self):
        self.attacked_squares, self.defended_squares, self.pinned, self.checking_pieces = move.Move.get_attacked_defended_pinned_check(self)

        
    def update_king_index(self, start, end):
        if start == self.white_king_index:
            self.white_king_index = end
        elif start == self.black_king_index:
            self.black_king_index = end
            
    def update_legal_moves(self):
        self.legal_moves = move.Move.get_all_legal_moves(self)
            
        
    """
    STRING REPRESENTATION
    """
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
    