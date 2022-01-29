from abc import ABC, abstractmethod

# Class for each chess piece
class Piece(ABC):
    def __init__(self, index, player):
        self.index = index
        self.player = player

    def __str__(self):
        return self.symbol
    
class Pawn(Piece):
    piece_value = 1
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♙"
            self.value = self.piece_value
        else:
            self.symbol = "♟︎"
            self.value = -self.piece_value
            
    def __str__(self):
        return self.player + 'P'
    
class Rook(Piece):
    piece_value = 5
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♖"
            self.value = self.piece_value
        else:
            self.symbol = "♜"
            self.value = -self.piece_value
            
    def __str__(self):
        return self.player + 'R'

class Knight(Piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♘"
            self.value = self.piece_value
        else:
            self.symbol = "♞"
            self.value = -self.piece_value
            
    def __str__(self):
        return self.player + 'N'

class Bishop(Piece):
    piece_value = 3
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♗"
            self.value = self.piece_value
        else:
            self.symbol = "♝"
            self.value = -self.piece_value
    
    def __str__(self):
        return self.player + 'B'

class Queen(Piece):
    piece_value = 8
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♕"
            self.value = self.piece_value
        else:
            self.symbol = "♛"
            self.value = -self.piece_value
            
    def __str__(self):
        return self.player + 'Q'

class King(Piece):
    piece_value = 999
    def __init__(self, index, player):
        super().__init__(index, player)
        if self.player == "w":
            self.symbol = "♔"
            self.value = self.piece_value
        else:
            self.symbol = "♚"
            self.value = -self.piece_value
    
    def __str__(self):
        return self.player + 'K'