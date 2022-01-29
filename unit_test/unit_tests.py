import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from game_state import GameState
import unittest
from test_boards import *



class TestBasicMovement(unittest.TestCase):
    
    def test_mov(self):
        test_state = GameState()
        self.assertEqual(str(test_state.board), test_board)
        test_state.board.move(8, 16)
        self.assertEqual(str(test_state.board), test_board_1)
        test_state.board.move(16, 24)
        self.assertEqual(str(test_state.board), test_board_2)


if __name__ == '__main__':
    unittest.main()