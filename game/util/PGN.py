import util.utils as util
import pieces.piece as piece
import pieces.piece_constants as piece_constants
import regex as re


class PGN:
    @classmethod    
    def create_PGN_string(cls, move_object):
        # ! CASTLING 
        castling = ''
        castling_bool = False
        if castling_bool:
            #if queen side castle
            return 'O-O'
            #if king side castle
            return 'O-O-O'
        
        moving_piece = move_object.piece
        current_player_pieces = piece.Piece.white_pieces if moving_piece.player == 'w' else piece.Piece.black_pieces
        
        # PIECE NOTATION
        notation = move_object.piece.notation
        if notation == 'P':
            notation = ''
        else:
            # IF MULTIPLE PIECES OF SAME TYPE CAN GO TO END, SPECIFY COLUMN OF PIECE
            legal_moves = move_object.non_FEN_attributes['legal_moves']
            for other_piece in current_player_pieces:
                # Get all other pieces of same type
                if other_piece != moving_piece and other_piece.notation == notation:
                    if other_piece.index in legal_moves:
                        if move_object.end in legal_moves[other_piece.index]:
                           notation  += util.index_to_coordinate(move_object.start)[0]

            
        # CAPTURE
        capture = ''
        if move_object.captured:
            if move_object.piece.notation == 'P':
                capture = util.index_to_coordinate(move_object.start)[0]
            capture += 'x'

        # END COORDINATE
        coordinate = util.index_to_coordinate(move_object.end)
        
        # CHECK
        check     = ''
        if not move_object.game_over:
            if len(move_object.checking_pieces) > 0:
                check = '+'
        
        # GAME OVER
        game_over = ''
        if move_object.game_over:
            # CHECKMATE
            if move_object.game_over == 'Checkmate':
                game_over = '#'
            # STALEMATE
            elif move_object.game_over == 'Stalemate':
                game_over = '$'
            # DRAW
            elif  move_object.game_over == 'some other draw':
                NotImplemented
                
            # ! implemenet 1-0 for white wins, 0-1 for black, and 1/2-1/2 for a draw.
                
                    
        return notation + capture + coordinate + check + game_over
    
    @classmethod
    def load_moves_from_PGN(cls, game_state, PGN_string):
        """Makes all moves in PGN_string in game state

        Args:
            game_state (GameState()): current game state
            PGN_string (string): PGN notation of all moves
        """
        PGN_string = re.sub(r"{(.*?)}", "", PGN_string) # Remove annotations
        PGN_string = re.sub(r"\(.*?\)", "", PGN_string) # Remove branching moves
        PGN_string = re.sub(r"[0-9]+\.+", "", PGN_string) # Remove number
        PGN_list = PGN_string.split()
        for PGN_move_string in PGN_list:
            PGN.move_from_PGN(game_state, PGN_move_string)
                
    @classmethod    
    def move_from_PGN(cls, game_state, PGN_move_string):
        """Find start and end index for move in PGN_string

        Args:
            PGN_move_string (str): PGN representation of move
        """
        piece_notations = ['K', 'Q', 'B', 'N', 'R', 'P']
        columns         = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        ranks           = ['1', '2', '3', '4', '5', '6', '7', '8']
        current_player_pieces   = piece.Piece.white_pieces if game_state.turn == 'w' else piece.Piece.black_pieces
        
        # CASTLE
        if PGN_move_string == 'O-O':
            if game_state.turn == 'w':
                start_index = piece_constants.WHITE_KING_INDEX
                end_index = start_index + 2
            else:
                start_index = piece_constants.BLACK_KING_INDEX
                end_index = start_index + 2
            game_state.make_move(start_index, end_index)
        elif PGN_move_string == 'O-O-O':
            if game_state.turn == 'w':
                start_index = piece_constants.WHITE_KING_INDEX
                end_index = start_index - 2
            else:
                start_index = piece_constants.BLACK_KING_INDEX
                end_index = start_index - 2
            game_state.make_move(start_index, end_index)
            
    
        
        # FIND PIECE TYPE
        possible_piece_notation = PGN_move_string[0]
        if possible_piece_notation in piece_notations:
            possible_pieces = [piece for piece in current_player_pieces if piece.notation == possible_piece_notation]
        else:
            possible_pieces = [piece for piece in current_player_pieces if piece.notation == 'P']
        
        # FIND ENDING SQUARE INDEX
        column = ''
        for char in PGN_move_string:
            if char in columns:
                
                # If nothing in column
                if not column:
                    column = char
                # If second column, first column specifies piece location
                else:
                    possible_pieces = [piece for piece in possible_pieces if util.index_to_coordinate(piece.index)[0] == column]
                    column = char
            elif char in ranks:
                end_coordinate = column + char
                end_index = util.coordinate_to_index(end_coordinate)
                
                # FIND PIECE IN POSSIBLE PIECES THAT CAN MOVE TO END_COORDINATE
                legal_moves = game_state.legal_moves
                for possible_piece in possible_pieces:
                    if possible_piece.index in legal_moves:
                        if end_index in legal_moves[possible_piece.index]:
                            start_index = possible_piece.index
                            break
                break
        game_state.make_move(start_index, end_index)
        #pawn promotion
        
        
    @classmethod    
    def PGN_string_of_game(cls, game_state):
        """Create string containing PGN of moves in game

        Args:
            game_state (game_state): current game_state

        Returns:
            [string]: String of all PGN notation of moves
        """        
        pgn_string = ''
        turn = 0
        for i in range(game_state.turn_counter):
            if turn % 2 == 0:
                pgn_string += (turn % 2) + 1
                pgn_string += ' '
            pgn_string += game_state.move_history[i].__str__()
        return pgn_string
    
    