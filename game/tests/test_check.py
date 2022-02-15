import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from testing_constants import *

import game_state
import move

class TestAttackingSquares:
    def test_attacking_squares_1(self):
        test_state = game_state.GameState()
        attacked_squares_list = move.Move.get_attacked_squares(test_state)
        assert len(attacked_squares_list) == 8
        
    def test_attacking_squares_2(self):
        test_state = game_state.GameState()
        # Pawn to d4
        test_state.make_move(11, 27)
        attacked_squares_list = move.Move.get_attacked_squares(test_state)
        assert len(attacked_squares_list) == 14
        
        
    def test_attacking_squares_3(self):
        test_state = game_state.GameState()
        test_state.make_move(11, 27) # Pawn to d4
        test_state.make_move(51, 35) # Pawn to d5
        test_state.make_move(12, 20) # Pawn to e3
        attacked_squares_list = move.Move.get_attacked_squares(test_state)
        assert len(attacked_squares_list) == 19



class TestSlidingPiecePinnedAttribute:
    def test_nothing_pinned(self):
        test_state = game_state.GameState()
        actual = test_state.pinned_lines
        expected = []
        assert actual == expected
    
    def test_one_pin(self):
        test_state = game_state.GameState('rnb1kbnr/pppppppp/4q3/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        actual = test_state.pinned_lines
        expected = [[36, 28, 20, 12]]
        assert actual == expected
        
    def test_two_pin(self):
        test_state = game_state.GameState('rnb1k1nr/pppppppp/8/8/1b5q/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        actual = test_state.pinned_lines
        expected = [[18, 11], [22, 13]]
        assert actual == expected
        
    def test_pinned_pawn_cant_move_forward(self):
        test_fen = 'rnbqk1nr/pppppppp/8/8/1b1P4/2P1P3/PP3PPP/RNBQKBNR w KQkq - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('c3', 'c4')
        actual = repr(test_state)
        expected = test_fen
        assert actual == expected
        
    def test_pinned_pawn_with_broken_pin_can_move_forward(self):
        test_fen = 'rnbqk1nr/pppppppp/8/8/1bPP4/4P3/PP1B1PPP/RN1QKBNR b KQkq - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('c3', 'c4')
        actual = repr(test_state)
        expected = test_fen
        assert actual == expected
        
        
        
        
class TestCheck:
    def test_check_displayed_in_move_object_PGN(self):
        test_FEN = 'rnbqkbnr/ppp2ppp/3Pp3/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        test_state.make_move(43, 51)
        assert str(test_state.move_history[-1]) == 'd7+'
    
    def test_legal_moves_when_in_check(self):
        NotImplemented
        
    def test_pinned(self):
        NotImplemented
        
    def test_discovered(self):
        NotImplemented
        
    def test_cannot_castle(self):
        NotImplemented
        
        
class TestCheckMate:
    def test_checkmate_displayed_in_move_object_PGN(self):
        NotImplemented