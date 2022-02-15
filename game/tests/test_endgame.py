import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from testing_constants import *

class TestCheckMate:
    def test_checkmate_displayed_in_move_object_PGN(self):
        test_fen = 'rnbqk1nr/pppppppp/8/8/1bPP4/4P3/PP1B1PPP/RN1QKBNR b KQkq - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('c3', 'c4')
        actual = repr(test_state)
        expected = test_fen
        assert actual == expected