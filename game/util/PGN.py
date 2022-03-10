import util.utils as util
import pieces.piece as piece
import pieces.piece_constants as piece_constants
import pieces.pawn as pawn
import regex as re


class PGN:
    @classmethod    
    def create_PGN_string(cls, move_object):
        moving_piece = move_object.piece
        
        # CASTLING 
        if moving_piece.notation == 'K':
            distance = move_object.end - move_object.start
            if abs(distance) == 2:
                if distance > 0:
                    return 'O-O'
                else:
                    return 'O-O-O'
            
        current_player_pieces = piece.Piece.white_pieces if moving_piece.player == 'w' else piece.Piece.black_pieces
        
        # PIECE NOTATION
        notation = move_object.piece.notation
        if isinstance(moving_piece, pawn.Pawn) and (moving_piece.notation == 'P' or moving_piece.promoted_move_count == 0):
            notation = ''
        else:
            # IF MULTIPLE PIECES OF SAME TYPE CAN GO TO END, SPECIFY COLUMN OF PIECE
            legal_moves = move_object.non_FEN_attributes['legal_moves']
            
            same_legal_move  = False
            same_column      = False
            same_rank        = False
            coordinate       = util.index_to_coordinate(move_object.start)
            for other_piece in current_player_pieces:
                other_coordinate = util.index_to_coordinate(other_piece.index)
                # Get all other pieces of same type
                if other_piece != moving_piece and other_piece.notation == notation:
                    if other_piece.index in legal_moves:
                        if move_object.end in legal_moves[other_piece.index]:
                            same_legal_move  = True
                            if coordinate[0] == other_coordinate[0]:
                                same_column = True
                            if coordinate[1] == other_coordinate[1]:
                                same_rank = True
            if same_legal_move:
                if same_rank:
                    notation += coordinate[0]
                if same_column:
                    notation += coordinate[1]
                if not same_rank and not same_column:
                    notation += coordinate[0]

            
        # CAPTURE
        capture = ''
        if move_object.captured:
            if move_object.piece.notation == 'P':
                capture = util.index_to_coordinate(move_object.start)[0]
            capture += 'x'

        # END COORDINATE
        coordinate = util.index_to_coordinate(move_object.end)
        
        # PAWN PROMOTION
        promotion = ''
        if isinstance(moving_piece, pawn.Pawn) and moving_piece.promotion_choice and moving_piece.promoted_move_count == 0:
            promotion = '=' + moving_piece.notation
            
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
                if moving_piece.player == 'w':
                    game_over += ' 1-0'
                else:
                    game_over += ' 0-1'
            # DRAW
            else:
                # STALEMATE
                if move_object.game_over == 'Stalemate':
                    game_over = '$'
                elif  move_object.game_over == 'some other draw':
                    NotImplemented
                game_over += '1/2-1/2'
                
            # ! implemenet 1-0 for white wins, 0-1 for black, and 1/2-1/2 for a draw.
                
                    
        return notation + capture + coordinate + promotion + check + game_over
    
    @classmethod
    def load_moves_from_PGN(cls, game_state, PGN_string):
        """Makes all moves in PGN_string in game state

        Args:
            game_state (GameState()): current game state
            PGN_string (string): PGN notation of all moves
        """
        PGN_string = re.sub(r'\[.+\]', "", PGN_string) # Remove tag roster
        PGN_string = re.sub(r"{(.*?)}", "", PGN_string) # Remove annotations
        PGN_string = re.sub(r"\(.*?\)", "", PGN_string) # Remove branching moves
        PGN_string = re.sub(r"[0-9]+\.+", "", PGN_string) # Remove number
        PGN_string = re.sub(r'(1\/2-1\/2)?', "", PGN_string) # Remove draw notation
        PGN_string = re.sub(r'[0-1]-[0-1]?', "", PGN_string) # Remove win notation
        PGN_list = PGN_string.split()
        for PGN_move_string in PGN_list:
            PGN.move_from_PGN(game_state, PGN_move_string)
                
    @classmethod    
    def move_from_PGN(cls, game_state, PGN_move_string):
        """Find start and end index for move in PGN_string

        Args:
            PGN_move_string (str): PGN representation of move
        """
        current_player_pieces   = piece.Piece.white_pieces if game_state.turn == 'w' else piece.Piece.black_pieces
        
        # CASTLE
        if 'O-O-O' in PGN_move_string:
            if game_state.turn == 'w':
                start_index = piece_constants.WHITE_KING_INDEX
                end_index = start_index - 2
            else:
                start_index = piece_constants.BLACK_KING_INDEX
                end_index = start_index - 2
            game_state.make_move(start_index, end_index)
            return
        if 'O-O' in PGN_move_string:
            if game_state.turn == 'w':
                start_index = piece_constants.WHITE_KING_INDEX
                end_index = start_index + 2
            else:
                start_index = piece_constants.BLACK_KING_INDEX
                end_index = start_index + 2
            game_state.make_move(start_index, end_index)
            return
        
        # FIND ENDING SQUARE INDEX
        end_coordinate = re.findall(r'[a-h][1-8]', PGN_move_string)[-1]
        no_end_coordinate_string = re.sub(r'[a-h][1-8]', '', PGN_move_string)
        end_index = util.coordinate_to_index(end_coordinate)
        
        # FIND PIECE TYPE
        piece_string = re.match(r'^[KRNBQ]{1}', no_end_coordinate_string)
        if not piece_string:
            possible_pieces = [piece for piece in current_player_pieces if piece.notation == 'P']
        else:
            piece_string = piece_string.group()
            piece_notation = piece_string
            possible_pieces = [piece for piece in current_player_pieces if piece.notation == piece_notation]
        
        no_piece_string         = re.sub(r'^[RNBQ]', '', no_end_coordinate_string)
        piece_coordinate_string = re.match(r'^[a-h]?[1-8]?', no_piece_string)
        if piece_coordinate_string.group() != '':
            # FILTER COLUMN AND RANK
            possible_column = re.match(r'[a-h]', no_piece_string[:])
            possible_rank   = re.match(r'[1-8]', no_piece_string[:])
            if possible_column:
                possible_column = possible_column.group()
                possible_pieces = [piece for piece in possible_pieces if util.index_to_coordinate(piece.index)[0] == possible_column]
            if possible_rank:
                possible_rank   = possible_rank.group()
                possible_pieces = [piece for piece in possible_pieces if util.index_to_coordinate(piece.index)[1] == possible_rank]
        
        # FILTER CAPTURED PIECES
        possible_pieces = [piece for piece in possible_pieces if not piece.captured]
        
        # FILTER LEGAL MOVES
        legal_moves = game_state.legal_moves
        for possible_piece in possible_pieces:
            if possible_piece.index in legal_moves:
                if end_index in legal_moves[possible_piece.index]:
                    start_index = possible_piece.index
                    break
                
        move_successful = game_state.make_move(start_index, end_index)
        assert move_successful
        
        
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
    
    