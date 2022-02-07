import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from game_state import GameState
import unittest
from test_boards import *

class TestBasicMovement(unittest.TestCase):    
    def test_FEN(self):
        test_state_1 = GameState()
        self.assertEqual(repr(test_state_1), starting_FEN)
        test_state_2 = GameState(test_FEN_1)
        self.assertEqual(repr(test_state_2), test_FEN_1)
        test_state_3 = GameState(test_FEN_2)
        self.assertEqual(repr(test_state_3), test_FEN_2)
        
        
    def test_pawn_moves(self):
        # Forward pawn movement
        test_state = GameState()
        test_state.move(11, 19)
        self.assertEqual(repr(test_state), test_board_1)
        
        # Double forward pawn movement and en passant updating
        test_state = GameState()
        test_state.move(11, 27)
        self.assertEqual(repr(test_state), test_board_2)
        

if __name__ == '__main__':
    unittest.main()