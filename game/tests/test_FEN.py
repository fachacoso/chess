import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

class TestFEN:
    def test_game_state_returns_default_FEN(self):
        # ARRANGE + ACT
        test_state = game_state.GameState()
        
        # ASSERT
        assert repr(test_state) == starting_FEN
        
    def test_game_state_returns_custom_FEN(self):
        # ARRANGE
        test_FEN_list = []
        for test_FEN in test_FEN_list:
            
            # ACT
            test_state = game_state.GameState(test_FEN)
            
            # ASSERT
            assert repr(test_state) == test_FEN
            
    def test_game_state_board_is_same_object_as_fen_board(self, tear_down):
        # ARRANGE + ACT
        test_state = game_state.GameState()
        
        # ASSERT
        assert test_state.board == test_state.current_FEN.board

class TestUndoFEN:
    def test_game_state_board_is_same_object_as_fen_history_boards(self):
        # ARRANGE
        test_state = game_state.GameState()
        assert test_state.board == test_state.current_FEN.board
        
        # ACT
        test_state.make_move('c2', 'c4')
        test_state.make_move('c7', 'c5')
        test_state.make_move('d2', 'd3')
        
        # ASSERT
        assert test_state.board == test_state.current_FEN.board
        assert test_state.board == test_state.FEN_history[0].board
        assert test_state.board == test_state.FEN_history[1].board
        assert test_state.board == test_state.FEN_history[2].board
        
        
        
