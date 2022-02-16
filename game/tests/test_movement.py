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
        test_state.make_move(11, 19)
        assert repr(test_state) == forward_pawn_FEN
        
    def test_pawn_capture(self):
        # Standard pawn capture
        test_state = game_state.GameState(pawn_capture_FEN_1)
        test_state.make_move(35, 42)
        assert repr(test_state) == pawn_capture_FEN_2


class TestMovementWithCoordinates:
    def test_pawn_forward(self):
        # Forward pawn movement
        test_state = game_state.GameState()
        test_state.make_move('d2', 'd3')
        assert repr(test_state) == forward_pawn_FEN


import logging

LOGGER = logging.getLogger(__name__)        

import util.utils as util

class TestAllMoves:
    @classmethod
    def possible_board_states_count(cls, game_state, depth):
        legal_moves = []
        for index, legal_move_list in game_state.legal_moves.items():
            for move in legal_move_list:
                legal_moves.append([index, move])
                
        possible_move_count = 0
        for move in legal_moves:
            start = move[0]
            end = move[1]
            game_state.make_move(start, end)
            
            if depth == 1:
                possible_move_count += 1
                LOGGER.warning('After moving {} on {} to {}, resulting board state \n {}'.format(game_state.get_square(start).get_piece(), 
                                                                                util.index_to_coordinate(start), 
                                                                                util.index_to_coordinate(end), 
                                                                                repr(game_state)))
            else:
                LOGGER.warning('{}{} to {}'.format(depth * '---', start, end))
                possible_move_count += TestAllMoves.possible_board_states_count(game_state, depth - 1)
            game_state.undo_move()

        
        return possible_move_count

    
    def test_move_count_depth_1(self):
        test_state = game_state.GameState()
        possible_move_count = TestAllMoves.possible_board_states_count(test_state, 1)
            
        expected = 20
        actual = possible_move_count
        assert expected == actual
        
    def test_move_count_depth_2(self):
        test_state = game_state.GameState()
        possible_move_count = TestAllMoves.possible_board_states_count(test_state, 2)
            
        expected = 400
        actual = possible_move_count
        assert expected == actual
        
    def test_move_count_depth_3(self):
        test_state = game_state.GameState()
        possible_move_count = TestAllMoves.possible_board_states_count(test_state, 3)
            
        expected = 8902
        actual = possible_move_count
        assert expected == actual
        
    def test_move_count_depth_4(self):
        test_state = game_state.GameState()
        possible_move_count = TestAllMoves.possible_board_states_count(test_state, 4)
            
        expected = 197281
        actual = possible_move_count
        assert expected == actual
        
    def test_move_count_depth_5(self):
        test_state = game_state.GameState()
        possible_move_count = TestAllMoves.possible_board_states_count(test_state, 5)
            
        expected = 4865609
        actual = possible_move_count
        assert expected == actual
            
