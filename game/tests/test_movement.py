import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

class TestPawnMovement:
    def test_pawn_forward(self, tear_down):
        # ARRANGE
        test_state = game_state.GameState()
        
        # ACT
        test_state.make_move(11, 19)
        
        # ASSERT
        assert repr(test_state) == forward_pawn_FEN
        
    def test_pawn_capture(self, tear_down):
        # ARRANGE
        test_state = game_state.GameState(pawn_capture_FEN_1)
        
        # ACT
        test_state.make_move('d5', 'c6')
        
        # ASSERT
        assert repr(test_state) == pawn_capture_FEN_2


class TestMovementWithCoordinates:
    def test_pawn_forward(self, tear_down):
        # ARRANGE
        test_state = game_state.GameState()
        
        # ACT
        test_state.make_move('d2', 'd3')
        
        # ASSERT
        assert repr(test_state) == forward_pawn_FEN

