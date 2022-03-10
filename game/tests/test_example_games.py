import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

import util.PGN as PGN_util
from example_games import *


class TestExampleGames:
    @classmethod
    def check_PGN_to_FEN(cls, PGN, FEN):
        # ARRANGE
        pgn_string = PGN
        test_state = game_state.GameState()

        # ACT
        PGN_util.PGN.load_moves_from_PGN(test_state, pgn_string)

        # ASSERT
        expected = FEN
        actual = repr(test_state)
        assert expected == actual
        
    def test_game_1(self, tear_down):
        PGN = PGN_1
        FEN = FEN_1
        
        self.check_PGN_to_FEN(PGN, FEN)
        
    def test_game_2(self, tear_down):
        PGN = PGN_2
        FEN = FEN_2
        
        self.check_PGN_to_FEN(PGN, FEN)
        
    def test_game_3(self, tear_down):
        PGN = PGN_3
        FEN = FEN_3
        
        self.check_PGN_to_FEN(PGN, FEN)
        
    def test_game_4(self, tear_down):
        PGN = PGN_4
        FEN = FEN_4
        
        self.check_PGN_to_FEN(PGN, FEN)
        
    def test_game_5(self, tear_down):
        PGN = PGN_5
        FEN = FEN_5
        
        self.check_PGN_to_FEN(PGN, FEN)
    
    def test_game_6(self, tear_down):
        PGN = PGN_6
        FEN = FEN_6
        
        self.check_PGN_to_FEN(PGN, FEN)
        
    def test_game_7(self, tear_down):
        PGN = PGN_7
        FEN = FEN_7
        
        self.check_PGN_to_FEN(PGN, FEN)
