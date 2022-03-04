import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *


class TestPawnSpecial:
        
    def test_pawn_en_passant(self, tear_down):
        # ARRANGE
        test_state = game_state.GameState()
        
        # ACT
        test_state.make_move('d2', 'd4')
        
        # ASSERT
        assert repr(test_state) == 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
        
    def test_pawn_promotion(self, tear_down):
        NotImplemented
        
        
class TestCastle:
    def test_castle_wQ(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move('e1', 'c1')
        
        actual   = repr(test_state)
        expected = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/2KR3R b kq - 1 1'
        assert expected == actual
    
    def test_castle_wK(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move('e1', 'g1')
        
        # ASSERT
        actual   = repr(test_state)
        expected = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R4RK1 b kq - 1 1'
        assert expected == actual
    
    def test_castle_bK(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move('e8', 'g8')
        
        # ASSERT
        actual   = repr(test_state)
        expected = 'r4rk1/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQ - 1 2'
        assert expected == actual
    
    def test_castle_bQ(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R b KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move('e8', 'c8')
        
        # ASSERT
        actual   = repr(test_state)
        expected = '2kr3r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQ - 1 2'
        assert expected == actual
    
    def test_castle_blocked_by_check(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/p3q2p/8/8/8/8/P6P/R3K2R w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move('e1', 'c1')
        
        # ASSERT
        actual   = repr(test_state)
        expected = test_FEN
        assert expected == actual
    
    def test_castle_blocked_by_piece_in_between(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/p3q2p/8/8/8/8/P6P/R2PK2R w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move('e1', 'c1')
        
        # ASSERT
        actual   = repr(test_state)
        expected = test_FEN
        assert expected == actual
    
    def test_castle_blocked_by_sliding_piece_attacking_piece_in_between(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/p2q3p/8/8/8/8/P6P/R3K2R w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move('e1', 'c1')
        
        # ASSERT
        actual   = repr(test_state)
        expected = test_FEN
        assert expected == actual
    
    def test_undo_castle(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        test_state.make_move('e1', 'c1')
        
        # ACT
        test_state.undo_move()
        
        # ASSERT
        actual   = repr(test_state)
        expected = test_FEN
        assert expected == actual
    
class TestUndoSpecial:
    def test_undo_en_passant(self, tear_down):
        NotImplemented
        
    def test_undo_promotion(self, tear_down):
        NotImplemented

        
    def test_undo_castle(self, tear_down):
        NotImplemented
