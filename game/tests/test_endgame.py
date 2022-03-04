import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

class TestEndgame:
    def test_checkmate(self, tear_down):
        # ARRANGE
        test_fen = '1k6/8/8/8/8/r7/1q6/4K3 b - - 0 1'
        test_state = game_state.GameState(test_fen)
        
        # ACT
        test_state.make_move('a3', 'a1')
        
        # ASSERT
        assert test_state.game_over == 'Checkmate'
        
    def test_stalemate(self, tear_down):
        # ARRANGE
        test_fen = '7k/8/5K2/6Q1/8/8/8/8 w - - 0 1'
        test_state = game_state.GameState(test_fen)
        
        # ACT
        test_state.make_move('g5', 'g6')
        
        # ASSERT
        assert test_state.game_over == 'Stalemate'
        
    def test_draw_only_kings(self, tear_down):
        # ARRANGE
        NotImplemented
        
    def test_draw_repitition(self, tear_down):
        # ARRANGE
        NotImplemented