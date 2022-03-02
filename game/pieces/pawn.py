import pieces.piece as piece
import pieces.piece_constants as piece_constants

class Pawn(piece.Piece):
    """
    Represents pawn piece.  Inherits from base Piece class.

    Attributes
    ----------
    cls.notation : str
        algebraic notation of Pawn - P


    Methods
    -------
    get_moves(self, game_state)
        gets possible moves for pawn
    """

    notation = "P"

    def update_movement_attributes(self, game_state):
        """Returns list of moves for pawn"""
        moves  = []

        # Returns possible moves
        forward_square_list, capture_square_list = self.possible_indices()

        # Forward movement
        moves.extend(self.forward_moves(game_state, forward_square_list))

        # Captures
        moves.extend(self.capture_moves(game_state, capture_square_list))
        
        self.possible_moves =  moves


    def possible_indices(self):
        """Returns two lists containing possible target indexes for piece

        Returns:
            tuple: 
                forward_square_list (list[int] (2)): list of all indexes for possible forward movement
                capture_square_list (list[int] (2)): list of all indexes for possible captures
        """        
        # Helper variables
        direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index]
        num_north, num_south, num_east, num_west = direction_max[:4]

        # Find offsets for possible legal movement (forward or capture)
        direction_max       = piece_constants.NUM_SQUARES_TO_EDGE[self.index]
        forward_square_list = []
        capture_square_list = []
        if self.player == "w":
            if num_north > 0:
                forward_offset = 8
                if num_east > 0:
                    capture_square_list.append(self.index + 7)
                if num_west > 0:
                    capture_square_list.append(self.index + 9)
        else:
            if num_south > 0:
                forward_offset = -8
                if num_east > 0:
                    capture_square_list.append(self.index - 9)
                if num_west > 0:
                    capture_square_list.append(self.index - 7)

        forward_max = 1
        if not self.has_moved():
            forward_max = 2
        for i in range(forward_max):
            forward_square = self.index + forward_offset * (i + 1)
            forward_square_list.append(forward_square)

        return forward_square_list, capture_square_list

    def forward_moves(self, game_state, forward_square_list):
        """Returns possible forward moves"""
        moves = []
        for target_index in forward_square_list:
            target_square = game_state.get_square(target_index)
            if not target_square.is_empty():
                break
            moves.append(target_index)
        return moves

    def capture_moves(self, game_state, capture_square_list):
        """Returns possible capture moves and updates attacked and defended squares"""
        moves            = []
        attacked_squares = []
        defended_squares = []
        
        for target_index in capture_square_list:
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
                
                # If target square is en_passant, it's a possible move
                if game_state.en_passant == target_index:
                    moves.append(target_index)
                
        self.attacked_squares = attacked_squares
        self.defended_squares = defended_squares
        return moves