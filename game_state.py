from move import Move, legal_moves
from utils import *
from constants import *

class GameState:
    def __init__(self, FEN_string = None):
        # Initializes starting board using FEN notation
        if FEN_string == None:
            self.parse_fen(STARTING_FEN) #  Starting_FEN = (rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1)
            self.history_counter = 0
        else:
            self.parse_fen(FEN_string)
            self.history_counter = self.turn_counter
        self.move_history = []
            
            
    def parse_fen(self, FEN):
        FEN_list = FEN.split()
        
        # Piece placement that sets self.board --> (Square[64])
        piece_placement = FEN_list[0]
        self.board = FEN_Util.FEN_to_board(piece_placement)
        
        
        # Side to move - str
        # ('w')hite or ('b')lack
        self.turn = FEN_list[1] 
        
        # Castling ability - list
        # 'K' for white, king-side castle, 'Q' for white, queen-side castle, 'k' for black, king-side castle, 'q' for black, queen-side castle, 
        self.castling = FEN_Util.FEN_to_castling(FEN_list[2])
        
        # En Passant square - index
        # Index where En Passant can happen
        self.en_passant = FEN_Util.FEN_to_en_pessant(FEN_list[3])
        
        # Halfmove Counter - int
        # Moves since last pawn move or capture
        self.halfmove_counter = int(FEN_list[4])
        
        # Turn(Fullmove) Counter - int
        # Moves since game started
        self.turn_counter = int(FEN_list[5])
        
    def is_legal_move(self, start_index, end_index):
        return end_index in legal_moves(self, start_index)
    
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
        if end_square.is_empty():
            captured_piece = None
        else:
            captured_piece = end_square.get_piece()
        
        # Update GameState
        self.history_counter += 1
        self.update_turn()
        self.update_en_passant(piece, start_index, end_index)
        self.update_castling(piece)
        self.update_halfmove(piece, captured_piece)
        
        # Update Start and End Square
        start_square.remove_piece()
        end_square.set_piece(piece)
            
        # Update Piece
        piece.move(end_index)
        
        # Create Move Instance
        move = Move(piece, start_index, end_index, captured_piece, self.castling, self.en_passant)
        self.move_history.append(move)

        
    def update_turn(self, undo = False):
        if undo:
            self.turn_counter -= 1
        else:
            self.turn_counter += 1
        self.turn = 'w' if self.turn == 'b' else 'b'
    
    def update_en_passant(self, piece, start_index, end_index):
        if piece.notation == 'P':
            if abs(start_index - end_index) == 16:
                self.en_passant = (start_index + end_index) // 2
            
        

    def update_castling(self, piece):
        if piece.notation == 'K' or piece.notation == 'N':
            castle_list = []
            # Checks if specified piece is elligible for castling
            def validate_piece(index, piece_type, piece_player):
                square = self.get_square(index)
                if not square.is_empty():
                    piece = square.get_piece()
                    if piece.type == piece_type and piece_player == piece_player:
                        if not piece.has_moved():
                            return True
                return False
            
            # Check white castling rights
            WHITE_KING_INDEX = 4
            WHITE_ROOK_K_INDEX = 7
            WHITE_ROOK_Q_INDEX = 0
            if validate_piece(WHITE_KING_INDEX, 'K', 'w'):
                if validate_piece(WHITE_ROOK_K_INDEX, 'R', 'w'):
                    castle_list.append('K')
                if validate_piece(WHITE_ROOK_Q_INDEX, 'R', 'w'):
                    castle_list.append('Q')
                    
        # Check black castling rights        
            BLACK_KING_INDEX = 56
            BLACK_ROOK_K_INDEX = 63
            BLACK_ROOK_Q_INDEX = 60
            if validate_piece(BLACK_KING_INDEX, 'K', 'b'):
                if validate_piece(WHITE_ROOK_K_INDEX, 'R', 'b'):
                    castle_list.append('k')
                if validate_piece(BLACK_ROOK_Q_INDEX, 'R', 'b'):
                    castle_list.append('q')
                    
            self.castling = castle_list

    def update_halfmove(self, piece, captured_piece):
        if piece.notation == 'P' or captured_piece != None:
            self.halfmove_counter = 0
        else:
            self.halfmove_counter += 1 

    # Unicode representation of board
    def __str__(self):
        string = ''
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
        piece_placement = ''
        string = ''
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
            if char == '-':
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
        FEN_list.append(''.join(self.castling))
        
        # En Passant Square
        FEN_list.append(index_to_coordinate(self.en_passant))
        
        # Halfmove Counter
        FEN_list.append(str(self.halfmove_counter))
        
        # Turn(Fullmove) Counter
        FEN_list.append(str(self.turn_counter))
        
        return ' '.join(FEN_list)