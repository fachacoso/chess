import pieces.piece as piece
import pieces.piece_constants as piece_constants
import pieces.knight as knight
import pieces.bishop as bishop
import pieces.rook as rook
import pieces.queen as queen
import constants

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
    
    def __init__(self, index, player, move_count=0):
        super().__init__(index, player, move_count)
        self.promotion_choice    = None
        self.promoted_move_count = 0

    def update_movement_attributes(self, game_state):
        """Returns list of moves for pawn"""
        moves  = []

        if not self.promotion_choice:
            # Returns possible moves
            forward_square_list, capture_square_list = self.possible_indices()

            # Forward movement
            moves.extend(self.forward_moves(game_state, forward_square_list))

            # Captures
            moves.extend(self.capture_moves(game_state, capture_square_list))
            
            self.possible_moves =  moves
            
        else:
            if self.promotion_choice == 'Q':
                queen.Queen.update_movement_attributes(self, game_state)
            elif self.promotion_choice == 'B':
                bishop.Bishop.update_movement_attributes(self, game_state)
            elif self.promotion_choice == 'N':
                knight.Knight.update_movement_attributes(self, game_state)
            elif self.promotion_choice == 'R':
                rook.Rook.update_movement_attributes(self, game_state)
        
    def promote_pawn(self, promotion_choice):
        self.promotion_choice = promotion_choice
        if promotion_choice == 'Q':
            self.notation = 'Q'
        elif promotion_choice == 'B':
            self.notation = 'B'
        elif promotion_choice == 'N':
            self.notation = 'N'
        elif promotion_choice == 'R':
            self.notation = 'R'
            
    def undo_pawn_promotion(self):
        self.promotion_choice = None
        self.notation = 'P'
            
    def move(self, new_index):
        """Move piece to new_index"""
        super().move(new_index)
        
        if self.promotion_choice:
            self.promoted_move_count += 1
        
        if new_index in constants.FIRST_RANK_INDEXES or new_index in constants.EIGHT_RANK_INDEXES:
            self.promote_pawn('Q')
            
        
    def undo_last_move(self, old_index):
        """Move back piece to old_index"""
        super().undo_last_move(old_index)
        if self.promotion_choice:
            if self.promoted_move_count != 0:
                self.promoted_move_count -= 1        
            else:
                self.undo_pawn_promotion()

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
        player_pawn_rank = constants.SECOND_RANK_INDEXES if self.player == 'w' else constants.SEVENTH_RANK_INDEXES
        if self.index in player_pawn_rank:
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
    
