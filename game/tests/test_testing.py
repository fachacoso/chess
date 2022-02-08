import pytest

import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from testing_constants import *

class TestFEN:
    def test_game_state_returns_expected_FEN(self):
        test_state = game_state.GameState()
        assert repr(test_state) == starting_FEN
        
        test_state = game_state.GameState(test_FEN_1)
        assert repr(test_state) == test_FEN_1
        
        test_state = game_state.GameState(test_FEN_2)
        assert repr(test_state) == test_FEN_2
        
        
        
class TestMovement:
    def test_pawn_moves(self):
        # Forward pawn movement
        test_state = game_state.GameState()
        test_state.move(11, 19)
        assert repr(test_state) == test_board_1
        
        # Double forward pawn movement and en passant updating
        test_state = game_state.GameState()
        test_state.move(11, 27)
        assert repr(test_state) == test_board_2