from game_state import GameState
from move import Move


class PGN:
    def parse_PGN(string):
        NotImplemented


    def load_PGN(self, PGN_string):
        PGN_moves = []
        
        pgn_list = PGN_string.split()
        parse_counter = 0
        for i in len(pgn_list):
            if parse_counter % 3 == 0:
                continue
            
        return PGN_moves
                
        
    def move_from_PGN(self, PGN_string):
        NotImplemented
        # return start_index, end_index
        
        
    def get_PGN(self):
        pgn_string = ''
        turn = 0
        for i in range(self.turn_counter):
            if turn % 2 == 0:
                pgn_string += (turn % 2) + 1
                pgn_string += ' '
            pgn_string += self.move_history[i].__str__()
        return pgn_string