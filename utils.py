from constants import *
from square import Square


def coordinate_to_index(coordinate):
    """Takes coordinate (ex. 'g3') and returns index"""
    file_num, rank = coordinate
    return FILE_TO_NUM_DICTIONARY[file_num] + rank * 8 - 1

def index_to_coordinate(index):
    if index == None:
        return '-'
    file_num =  get_x(index)
    file = NUM_TO_FILE_DICTIONARY[file_num]
    rank = get_y(index)
    return file + str(rank + 1)

def xy_to_index(file, rank):
    return file + rank * 8

def get_x(index):
    return index % 8

def get_y(index):
    return index // 8

class FEN_Util:
    # Piece placement that sets self.board --> (Square[64])
    def FEN_to_board(piece_placement):
        board = []
        
        position_stack = []
        current_rank = []
        current_index = 55
        for char in piece_placement:
            if char.isupper():
                piece = NOTATION[char]
                square = Square(piece(current_index, 'w'))
                current_rank.append(square)
                current_index += 1
            elif char.islower():
                piece = NOTATION[char.upper()]
                square = Square(piece(current_index, 'b'))
                current_rank.append(square)
                current_index += 1
            elif char.isnumeric():
                for i in range(int(char)):
                    
                    current_rank.append(Square())
                    current_index += 1
            else:
                position_stack.append(current_rank)
                current_rank = []
                current_index -= 16
        position_stack.append(current_rank)
        for _ in range(RANK):
            rank = position_stack.pop()
            board.extend(rank)
        return board


    def FEN_to_castling(castling):
        if castling == '-':
            return []
        return [castle_notation for castle_notation in castling]

    def FEN_to_en_pessant(coordinate):
        if coordinate == '-':
            return None
        return coordinate_to_index(coordinate)    