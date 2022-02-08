import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from testing_constants import *

class TestFEN:
    def test_game_state_returns_default_FEN(self):
        test_state = game_state.GameState()
        assert repr(test_state) == starting_FEN
        
    def test_game_state_returns_custom_FEN(self):
        test_FEN_list = []
        for test_FEN in test_FEN_list:
            test_state = game_state.GameState(test_FEN)
            assert repr(test_state) == test_FEN
        
        
        
