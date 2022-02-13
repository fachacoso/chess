import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from testing_constants import *


class TestPawnSpecial:
        
    def test_pawn_en_passant(self):
        test_state = game_state.GameState()
        test_state.make_move(43, 50)
        assert repr(test_state) == pawn_en_passant_FEN
        
    def test_pawn_promotion(self):
        NotImplemented
        
        
class TestCastleSpecial:
    def test_castle_wK(self):
        NotImplemented
    
    def test_castle_wQ(self):
        NotImplemented
    
    def test_castle_bK(self):
        NotImplemented
    
    def test_castle_bQ(self):
        NotImplemented
    
    def test_castle_blocked_by_check(self):
        NotImplemented
    
    def test_castle_blocked_by_piece_in_between(self):
        NotImplemented
    
    def test_castle_blocked_by_sliding_piece_attacking_piece_in_between(self):
        NotImplemented
    
    
class TestUndoSpecial:
    def test_undo_en_passant(self):
        NotImplemented
        
    def test_undo_promotion(self):
        NotImplemented

        
    def test_undo_castle(self):
        NotImplemented
