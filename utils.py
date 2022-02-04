def get_X(index):
    return index % 8

def get_Y(index):
    return index // 8

def is_piece(square):
    return str(square) != '-'

def get_square(game_state, index):
    return game_state.board.board_pos[index]