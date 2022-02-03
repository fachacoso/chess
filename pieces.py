from abc import ABC, abstractmethod

# Class for each chess piece
class Piece(ABC):
    def __init__(self, index, player):
        self.index = index
        self.player = player

    def __str__(self):
        return self.symbol

    def __repr__(self):
        return self.player + self.notation

# index (int) - index of piece on board
# player (str) - (w)hite or (b)lack
# symbol (str) - unicode symbol of piece (ex. ♙, ♜, ♘)
# notation (str) - representative letter of piece (ex. R, B, N)

# __str__ (str) - calls symbol for debugging
# __repr__ (str) - letter representation of player and piece (ex. wP, wR, bN, bB )


class Pawn(Piece):
    piece_value = 1
    def __init__(self, index, player):
        super().__init__(index, player)
        self.notation = 'P'
        if self.player == "w":
            self.symbol = "♙"
            self.value = self.piece_value
        else:
            self.symbol = "♟︎"
            self.value = -self.piece_value

class Rook(Piece):
    piece_value = 5
    def __init__(self, index, player):
        super().__init__(index, player)
        self.notation = 'R'
        if self.player == "w":
            self.symbol = "♖"
            self.value = self.piece_value
        else:
            self.symbol = "♜"
            self.value = -self.piece_value

class Knight(Piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        self.notation = 'N'
        if self.player == "w":
            self.symbol = "♘"
            self.value = self.piece_value
        else:
            self.symbol = "♞"
            self.value = -self.piece_value

class Bishop(Piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        self.notation = 'B'
        if self.player == "w":
            self.symbol = "♗"
            self.value = self.piece_value
        else:
            self.symbol = "♝"
            self.value = -self.piece_value

class Queen(Piece):
    piece_value = 8
    def __init__(self, index, player):
        super().__init__(index, player)
        self.notation = 'Q'
        if self.player == "w":
            self.symbol = "♕"
            self.value = self.piece_value
        else:
            self.symbol = "♛"
            self.value = -self.piece_value

class King(Piece):
    piece_value = 999
    def __init__(self, index, player):
        super().__init__(index, player)
        self.notation = 'K'
        if self.player == "w":
            self.symbol = "♔"
            self.value = self.piece_value
        else:
            self.symbol = "♚"
            self.value = -self.piece_value
