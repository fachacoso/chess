import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from testing_constants import *

class TestPawnMovement:
    def test_pawn_forward(self):
        # Forward pawn movement
        test_state = game_state.GameState()
        test_state.move(11, 19)
        assert repr(test_state) == forward_pawn_FEN
        
    def test_pawn_double_forward(self):
        # Double forward pawn movement and en passant updating
        test_state = game_state.GameState()
        test_state.move(11, 27)
        assert repr(test_state) == forward_double_pawn_FEN
        
    def test_pawn_capture(self):
        # Standard pawn capture
        test_state = game_state.GameState()
        test_state.move(43, 50)
        assert repr(test_state) == pawn_capture_FEN_2
        
    def test_pawn_en_passant(self):
        # Standard pawn capture
        test_state = game_state.GameState()
        test_state.move(43, 50)
        assert repr(test_state) == pawn_en_passant_FEN
        