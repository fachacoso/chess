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
            
    def test_game_state_board_is_same_object_as_fen_board(self):
        test_state = game_state.GameState()
        assert test_state.board == test_state.current_FEN.board

class TestUndoFEN:
    def test_game_state_board_is_same_object_as_fen_history_boards(self):
        test_state = game_state.GameState()
        assert test_state.board == test_state.current_FEN.board
        test_state.make_move('c2', 'c4')
        assert test_state.board == test_state.current_FEN.board
        assert test_state.board == test_state.FEN_history[0].board
        test_state.make_move('c7', 'c5')
        assert test_state.board == test_state.current_FEN.board
        assert test_state.board == test_state.FEN_history[0].board
        assert test_state.board == test_state.FEN_history[1].board
        test_state.make_move('d2', 'd3')
        assert test_state.board == test_state.current_FEN.board
        assert test_state.board == test_state.FEN_history[0].board
        assert test_state.board == test_state.FEN_history[1].board
        assert test_state.board == test_state.FEN_history[2].board
        
        
        
