import pieces.piece as piece
import pieces.piece_constants as piece_constants

class Knight(piece.Piece):
    notation = 'N'


    def get_moves(self, game_state):
        moves  = []
        square = game_state.get_square(self.index)
        piece  = square.get_piece()
        
        # Helper variables
        direction_max = piece_constants.NUM_SQUARES_TO_EDGE[self.index]
        num_north, num_south, num_east, num_west = direction_max[:4]
        
        # All 8 directions
        offsets      = [-10, 6, -17, 15, -15, 17, -6, 10]
        offset_index = 0
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
                    if not target_square.is_empty():
                        if not piece.same_team(target_square):
                            moves.append(target_index)
                        else:
                            self.defended_squares.append(target_index)
                    else:
                        moves.append(target_index)
                offset_index += 1
        return moves