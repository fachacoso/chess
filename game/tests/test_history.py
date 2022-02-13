import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from testing_constants import *

class TestUndoMove:
    def test_undo_pawn_forward(self):
        test_state = game_state.GameState()
        test_state.make_move(11, 19)
        test_state.undo_move()
        assert repr(test_state) == starting_FEN
        
        
    def test_undo_pawn_forward_another_time(self):
        test_state = game_state.GameState()
        test_state.make_move(11, 19)
        test_state.undo_move()
        test_state.make_move(11, 19)
        test_state.undo_move()
        assert repr(test_state) == starting_FEN
        
    def test_undo_decrements_piece_move_count(self):
        test_state = game_state.GameState()
        test_state.make_move(11, 19)
        test_state.undo_move()
        test_state.make_move(11, 27)
        test_state.undo_move()
        assert repr(test_state) == starting_FEN
    
