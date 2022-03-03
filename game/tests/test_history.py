import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

class TestUndoMove:
    def test_undo_pawn_forward_shows_correct_FEN(self, tear_down):
        test_state = game_state.GameState()
        test_state.make_move(11, 19)
        test_state.undo_move()
        assert repr(test_state) == starting_FEN
        
        
    def test_undo_two_moves(self, tear_down):
        test_state = game_state.GameState()
        test_state.make_move('c2', 'c4')
        test_state.make_move('c7', 'c5')
        test_state.undo_move()
        test_state.undo_move()
        assert repr(test_state) == starting_FEN
        
    def test_undo_two_moves_then_make_move(self, tear_down):
        test_state = game_state.GameState()
        test_state.make_move('c2', 'c4')
        test_state.make_move('c7', 'c5')
        test_state.undo_move()
        test_state.undo_move()
        test_state.make_move('d2', 'd3')
        assert repr(test_state) == forward_pawn_FEN
        
    def test_undo_pawn_forward_another_time(self, tear_down):
        test_state = game_state.GameState()
        test_state.make_move(11, 19)
        test_state.undo_move()
        test_state.make_move(11, 19)
        test_state.undo_move()
        assert repr(test_state) == starting_FEN
        
    def test_undo_decrements_piece_move_count(self, tear_down):
        test_state = game_state.GameState()
        test_state.make_move(11, 19)
        test_state.undo_move()
        test_state.make_move(11, 27)
        test_state.undo_move()
        assert repr(test_state) == starting_FEN
    
    def test_undo_attribute_attacking_squares(self, tear_down):
        test_state_1 = game_state.GameState()
        test_state_1.make_move(11, 19)
        test_state_1.undo_move()
        
        test_state_2 = game_state.GameState()
        assert test_state_1.__dict__['attacked_squares'] == test_state_2.__dict__['attacked_squares']  
        
    def test_undo_attribute_turn(self, tear_down):
        test_state_1 = game_state.GameState()
        test_state_1.make_move(11, 19)
        test_state_1.undo_move()
        
        test_state_2 = game_state.GameState()
        assert test_state_1.__dict__['turn'] == test_state_2.__dict__['turn']
        
    def test_undo_attribute_board(self, tear_down):
        test_state_1 = game_state.GameState()
        test_state_1.make_move(11, 19)
        test_state_1.undo_move()
        
        test_state_2 = game_state.GameState()
        assert str(test_state_1.__dict__['board']) == str(test_state_2.__dict__['board'])
        
        