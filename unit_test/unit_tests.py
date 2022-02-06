import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from game_state import GameState
import unittest
from test_boards import *

class TestBasicMovement(unittest.TestCase):    
    def test_FEN(self):
        test_state = GameState()
        self.assertEqual(repr(test_state), starting_board)
        
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