from pieces import Pawn, Rook, Knight, Bishop, Queen, King
from constants import *

# Class for chess game session
class GameState:
    turn = "W"
    turn_counter = 0
    history_counter = 0
    move_history = []
    highlight = {}


    def __init__(self):
        self.board = Board()

    def is_game_over(self):
        NotImplemented()

    # Moves piece in start_index to end_index, appends move to move_history, changes index of piece
    def move(self, start_index, end_index):
        piece = self.board.board_pos[start_index]
        captured = None
        if self.board.board_pos[end_index] != '-':
            captured = self.board.board_pos[end_index]
        self.board.board_pos[end_index] = piece
        piece.index = end_index
        self.board.board_pos[start_index] = '-'
        self.move_history.append(move(self.turn, start_index, end_index, captured))

# Class for chess board
class Board:
    def __init__(self):
        self.board_pos = ['-'] * SQUARE_COUNT
        for i in range(SQUARE_COUNT):
            if i == '-':
                self.board_pos[i] = INITIAL_BOARD_STATE[i]
            else:
                player = INITIAL_BOARD_STATE[i][0]
                type = INITIAL_BOARD_STATE[i][1]
                if type == 'P':
                    self.board_pos[i] = Pawn(i, player)
                elif type == 'R':
                    self.board_pos[i] = Rook(i, player)
                elif type == 'N':
                    self.board_pos[i] = Knight(i, player)
                elif type == 'B':
                    self.board_pos[i] = Bishop(i, player)
                elif type == 'Q':
                    self.board_pos[i] = Queen(i, player)
                elif type == 'K':
                    self.board_pos[i] = King(i, player)


    # String representation of board used for debugging
    def __str__(self):
        string = "\n"
        for i in range(8):
            string += " ".join([str(x) for x in self.board_pos[i * 8 : (i + 1) * 8]])
            string += "\n"
        return string

    def move(self, start, end):
        self.board_pos[end] = self.board_pos[start]
        self.board_pos[start] = "-"

# Class used to record each move
class move:
    def __init__(self, turn, start, end, captured_piece):
        self.turn = turn
        self.start = start
        self.end = end
        self.captured = captured_piece
