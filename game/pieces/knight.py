import pieces.piece as piece
import pieces.piece_constants as piece_constants

class Knight(piece.Piece):
    """
    Represents knight piece.  Inherits from base Piece class.

    Attributes
    ----------
    cls.notation : str
        algebraic notation of Knight - N


    Methods
    -------
    get_moves(self, game_state)
        gets possible moves for knight
    """
    notation = 'N'


    def update_movement_attributes(self, game_state):
        """Returns list of moves for pawn"""
        moves  = []
        attacked_squares = []
        defended_squares = []
        
        square = game_state.get_square(self.index)
        piece  = square.get_piece()
        
        # Helper variables
        direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index]
        num_north, num_south, num_east, num_west = direction_max[:4]
        
        # All 8 offsets
        offsets      = [-10, 6, -17, 15, -15, 17, -6, 10]
        offset_index = 0
        
        # Uglier but compact way to iterate over all possible knight moves
        for x in range(-2, 3):
            if x == 0:
                continue
            if x < 0:
                horizontal_max = num_east
            else:
                horizontal_max = num_west
            for y in range(-2, 3):
                if y == 0 or abs(x) == abs(y):
                    continue
                if y < 0:
                    vertical_max = num_south
                else:
                    vertical_max = num_north
                
                if horizontal_max >= abs(x) and  vertical_max >= abs(y):
                    target_index = self.index + offsets[offset_index]
                    target_square = game_state.get_square(target_index)
                    
                    # If target square has piece
                    if not target_square.is_empty():
                        # If target piece is same team, it's defended
                        if self.same_team(target_square):
                            defended_squares.append(target_index)
                        # If target piece is different team, it's a possible move
                        else:
                            moves.append(target_index)
                            
                    # If target square has NO piece
                    else:
                        # Target square is attacked
                        attacked_squares.append(target_index)
                        # Target square is a possible move   
                        moves.append(target_index)
                        
                offset_index += 1
        
        self.attacked_squares = attacked_squares
        self.defended_squares = defended_squares
        self.possible_moves   = moves