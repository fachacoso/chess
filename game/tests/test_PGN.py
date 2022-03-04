import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

import util.PGN as PGN_util

class TestPGN:
        
    def test_capture_piece_with_knight_both_attacking(self, tear_down):
        test_fen   = 'rnbqkbnr/pppp1ppp/8/4p3/8/3N1N2/PPPPPPPP/R1BQKB1R w KQkq - 0 1'
        test_state = game_state.GameState(test_fen)
        
        test_state.make_move('f3', 'e5')
        
        expected = 'Nfxe5'
        actual   = str(test_state.move_history[-1])
        
        assert expected == actual
        
        test_state.undo_move()
        
        test_state.make_move('d3', 'e5')
        
        expected = 'Ndxe5'
        actual   = str(test_state.move_history[-1])
        
        assert expected == actual
        
        
        
    def test_check(self, tear_down):
        test_FEN   = 'rnbqkbnr/ppp2ppp/3Pp3/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        test_state.make_move(43, 51)
        assert len(test_state.checking_pieces) > 0
        
        expected = 'd7+'
        actual   = str(test_state.move_history[-1])
        
        assert expected == actual
        
    def test_checkmate_displayed_in_move_object_PGN(self, tear_down):
        test_fen   = '1k6/8/8/8/8/r7/1q6/4K3 b - - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('a3', 'a1')
        assert '#' in str(test_state.move_history[0])
        
    def test_stalemate_displayed_in_move_object_PGN(self, tear_down): 
        test_fen   = '7k/8/5K2/6Q1/8/8/8/8 w - - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('g5', 'g6')
        assert '$' in str(test_state.move_history[0])
        
class TestParseMoveFromPGN:
    def test_pawn_move(self, tear_down):
        pgn_string = 'd3'
        
        test_state = game_state.GameState()
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        expected = 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_double_pawn_move(self, tear_down):
        pgn_string = 'd4'
        
        test_state = game_state.GameState()
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        expected = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_knight_move(self, tear_down):
        pgn_string = 'Nc3'
        
        test_state = game_state.GameState()
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        expected = 'rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq - 1 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_two_pieces_same_type_capture_move(self, tear_down):
        test_FEN   = 'rnbqkbnr/pppp1ppp/8/4p3/8/3N1N2/PPPPPPPP/R1BQKB1R w KQkq - 0 1'
        pgn_string = 'Nfxe5'
        
        test_state = game_state.GameState(test_FEN)
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        expected = 'rnbqkbnr/pppp1ppp/8/4N3/8/3N4/PPPPPPPP/R1BQKB1R b KQkq - 0 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_promotion_move(self, tear_down):
        test_FEN   = 'xxx'
        pgn_string = 'xxx'
        
        test_state = game_state.GameState(test_FEN)
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        expected = 'xxx'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_castle_move(self, tear_down):
        test_FEN   = 'xxx'
        pgn_string = 'xxx'
        
        test_state = game_state.GameState(test_FEN)
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        expected = 'xxx'
        actual   = repr(test_state)
        assert expected == actual