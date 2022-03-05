import pytest
import sys
import os

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

import game_state
from tests.testing_constants import *

import util.PGN as PGN_util


class TestExampleGames:
    def test_game_1(self, tear_down):
        # ARRANGE
        pgn_string = "1. d4 d5 2. Bf4 { D00 Queen's Pawn Game: Mason Variation } e6 3. Nf3 Bd6 4. Bg3 Nf6 5. e3 Nc6 6. Bd3 e5 7. dxe5 Nxe5 8. Bxe5 Bg4 9. Nbd2 Bxe5 10. h3 Bxf3 11. Qxf3 Bxb2 12. Rd1 O-O 13. g4 Qd6 14. e4 dxe4 15. Nxe4 Nxe4 16. Bxe4 Qb4+ 17. Kf1 Rad8 18. Qf5 Rxd1+ 19. Kg2 Rxh1 20. Qxh7# { White wins by checkmate. } 1-0"
        test_state = game_state.GameState()

        # ACT
        PGN_util.PGN.load_moves_from_PGN(test_state, pgn_string)

        # ASSERT
        expected = "5rk1/ppp2ppQ/8/8/1q2B1P1/7P/PbP2PK1/7r b - - 0 20"
        actual = repr(test_state)
        assert expected == actual
