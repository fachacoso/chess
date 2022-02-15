import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from testing_constants import *

import game_state
import move


def get_attacked_squares_list(attacked_squares_dictionary):
    attacked_squares_list = []
    for key, value in attacked_squares_dictionary.items():
        attacked_squares_list.extend(value)
    return set(attacked_squares_list)
class TestAttackingSquares:
    def test_attacking_squares_1(self):
        test_state = game_state.GameState()
        attacked_squares_dictionary = move.Move.get_attacked_squares(test_state)
        attacked_squares_list = get_attacked_squares_list(attacked_squares_dictionary)
        assert len(attacked_squares_list) == 8
        
    def test_attacking_squares_2(self):
        test_state = game_state.GameState()
        # Pawn to d4
        test_state.make_move(11, 27)
        attacked_squares_dictionary = move.Move.get_attacked_squares(test_state)
        attacked_squares_list = get_attacked_squares_list(attacked_squares_dictionary)
        assert len(attacked_squares_list) == 14
        
        
    def test_attacking_squares_3(self):
        test_state = game_state.GameState()
        test_state.make_move(11, 27) # Pawn to d4
        test_state.make_move(51, 35) # Pawn to d5
        test_state.make_move(12, 20) # Pawn to e3
        attacked_squares_dictionary = move.Move.get_attacked_squares(test_state)
        attacked_squares_list = get_attacked_squares_list(attacked_squares_dictionary)
        assert len(attacked_squares_list) == 19



class TestSlidingPiecePinnedAttribute:
    def test_nothing_pinned(self):
        test_state = game_state.GameState()
        actual = test_state.pinned_lines
        expected = {}
        assert actual == expected
    
    def test_one_pin(self):
        test_state = game_state.GameState('rnb1kbnr/pppppppp/4q3/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        actual = test_state.pinned_lines
        expected = {44: [36, 28, 20, 12]}
        assert actual == expected
        
    def test_two_pin(self):
        test_state = game_state.GameState('rnb1k1nr/pppppppp/8/8/1b5q/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
        actual = test_state.pinned_lines
        expected = {25: [18, 11], 31: [22, 13]}
        assert actual == expected
        
    def test_pinned_pawn_cant_move_forward(self):
        test_fen = 'rnbqk1nr/pppppppp/8/8/1b1P4/2P1P3/PP3PPP/RNBQKBNR w KQkq - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('c3', 'c4')
        actual = repr(test_state)
        expected = test_fen
        assert actual == expected
        
    def test_pinned_pawn_with_broken_pin_can_move_forward(self):
        test_fen = 'rnbqk1nr/pppppppp/8/8/1bPP4/4P3/PP1B1PPP/RN1QKBNR b KQkq - 0 1'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('c3', 'c4')
        actual = repr(test_state)
        expected = test_fen
        assert actual == expected
        
        
        
        
class TestCheck:
    def test_check_displayed_in_move_object_PGN(self):
        test_FEN = 'rnbqkbnr/ppp2ppp/3Pp3/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        test_state.make_move(43, 51)
        assert type(test_state.checking_piece_index) == int
        assert str(test_state.move_history[-1]) == 'd7+'
    
    def test_cant_move_defended(self):
        test_fen = '8/k7/1Q6/2K5/8/8/8/8 b - - 0 1'
        test_state = game_state.GameState(test_fen)

        actual = test_state.legal_moves
        expected = {48: [56]}
        assert actual == expected
        
    def test_in_check_either_move_or_block(self):
        test_fen = 'rnbqkbnr/ppp2ppp/8/1B1pp3/3PP3/8/PPP2PPP/RNBQK1NR b KQkq - 1 3'
        test_state = game_state.GameState(test_fen)
        actual = test_state.legal_moves
        expected = {50: [42], 57: [42, 51], 58: [51], 59: [51], 60: [52]}
        assert actual == expected
    
    def test_pinned(self):
        test_fen = 'rnbqkbnr/pp3ppp/2p5/1B1pp3/3PP3/8/PPP2PPP/RNBQK1NR b KQkq - 1 3'
        test_state = game_state.GameState(test_fen)
        assert not test_state.make_move('c6', 'c5')
        
    def test_discovered(self):
        test_fen = 'rnbqkbnr/pp3ppp/2p5/1B1pp3/3PP3/8/PPP2PPP/RNBQK1NR w KQkq - 1 3'
        test_state = game_state.GameState(test_fen)
        test_state.make_move('b5', 'c6')
        assert type(test_state.checking_piece_index) == int
        
        
    def test_cannot_castle(self):
        NotImplemented
        
        
        