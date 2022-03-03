import util.utils as util


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
        
        # PIECE NOTATION
        notation = move_object.piece.notation
        if notation == 'P':
            notation = ''
            
        # CAPTURE
        capture = ''
        if move_object.captured:
            if move_object.piece.notation == 'P':
                capture = util.index_to_coordinate(move_object.start)[0]
            capture += 'x'

        # END COORDINATE
        coordinate = util.index_to_coordinate(move_object.end)
        
        
        if not move_object.game_over:
            # CHECK
            check = ''
            if len(move_object.checking_pieces) > 0:
                check = '+'
                
            return notation + capture + coordinate + check
        
        # GAME OVER
        else:
            if move_object.game_over:
                # CHECKMATE
                if move_object.game_over == 'Checkmate':
                    game_over = '#'
                # STALEMATE
                else:
                    game_over = '$'
            return notation + capture + coordinate + game_over
    
    @classmethod
    def load_moves_from_PGN(cls, game_state, PGN_string):
        """Makes all moves in PGN_string in game state

        Args:
            game_state (GameState()): current game state
            PGN_string (string): PGN notation of all moves
        """        
        PGN_moves = []
        
        pgn_list = PGN_string.split()
        parse_counter = 0
        for i in len(pgn_list):
            if parse_counter % 3 == 0:
                continue
            
        return PGN_moves
    
    @classmethod
    def parse_PGN(cls, string):
        """

        Args:
            game_state (GameState()): current game state
            PGN_string (string): PGN notation of all moves
        """    
        NotImplemented
                
    @classmethod    
    def move_from_PGN(cls, PGN_string):
        NotImplemented
        # return start_index, end_index
        
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
    
    