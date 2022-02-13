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
        
        
class TestCheck:
    def test_check_displayed_in_move_object(self):
        NotImplemented
    
    def test_check(self):
        NotImplemented
        
    def test_pinned(self):
        NotImplemented
        
    def test_discovered(self):
        NotImplemented
        
    def test_cannot_castle(self):
        NotImplemented