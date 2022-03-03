import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

class TestCheckmate:
    def test_checkmate_displayed_in_move_object_PGN(self):
        test_fen = '1k6/8/8/8/8/r7/1q6/4K3 b - - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('a3', 'a1')
        assert '#' in str(test_state.move_history[0])
        
class TestStalemate:
    def test_stalemate_displayed_in_move_object_PGN(self):
        test_fen = '7k/8/5K2/6Q1/8/8/8/8 w - - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('g5', 'g6')
        assert '$' in str(test_state.move_history[0])