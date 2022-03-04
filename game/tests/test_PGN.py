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
        # ARRANGE
        test_fen   = 'rnbqkbnr/pppp1ppp/8/4p3/8/3N1N2/PPPPPPPP/R1BQKB1R w KQkq - 0 1'
        test_state = game_state.GameState(test_fen)
        
        # ACT
        test_state.make_move('f3', 'e5')
        
        # ASSERT
        expected = 'Nfxe5'
        actual   = str(test_state.move_history[-1])
        assert expected == actual
        
        # ARRANGE
        test_state.undo_move()
        
        # ACT    
        test_state.make_move('d3', 'e5')
        
        # ASSERT
        expected = 'Ndxe5'
        actual   = str(test_state.move_history[-1])
        assert expected == actual
        
        
        
    def test_check(self, tear_down):
        # ARRANGE
        test_FEN   = 'rnbqkbnr/ppp2ppp/3Pp3/8/8/8/PPP1PPPP/RNBQKBNR w KQkq - 0 1'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        test_state.make_move(43, 51)
        assert len(test_state.checking_pieces) > 0
        
        # ASSERT
        expected = 'd7+'
        actual   = str(test_state.move_history[-1])
        assert expected == actual
        
    def test_checkmate_displayed_in_move_object_PGN(self, tear_down):
        # ARRANGE
        test_fen   = '1k6/8/8/8/8/r7/1q6/4K3 b - - 0 1'
        test_state = game_state.GameState(test_fen)
        
        # ACT
        test_state.make_move('a3', 'a1')
        
        # ASSERT
        assert '#' in str(test_state.move_history[0])
        
    def test_stalemate_displayed_in_move_object_PGN(self, tear_down):
        # ARRANGE
        test_fen   = '7k/8/5K2/6Q1/8/8/8/8 w - - 0 1'
        test_state = game_state.GameState(test_fen)
        
        # ACT
        test_state.make_move('g5', 'g6')
        
        # ASSERT
        assert '$' in str(test_state.move_history[0])
        
class TestParseMoveFromPGN:
    def test_pawn_move(self, tear_down):
        # ARRANGE
        pgn_string = 'd3'
        test_state = game_state.GameState()
        
        # ACT
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'rnbqkbnr/pppppppp/8/8/8/3P4/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_double_pawn_move(self, tear_down):
        # ARRANGE
        pgn_string = 'd4'
        test_state = game_state.GameState()
        
        # ACT
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_knight_move(self, tear_down):
        # ARRANGE
        pgn_string = 'Nc3'
        test_state = game_state.GameState()
        
        # ACT
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq - 1 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_two_pieces_same_type_capture_move(self, tear_down):
        # ARRANGE
        test_FEN   = 'rnbqkbnr/pppp1ppp/8/4p3/8/3N1N2/PPPPPPPP/R1BQKB1R w KQkq - 0 1'
        pgn_string = 'Nfxe5'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'rnbqkbnr/pppp1ppp/8/4N3/8/3N4/PPPPPPPP/R1BQKB1R b KQkq - 0 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_promotion_move(self, tear_down):
        # ARRANGE
        test_FEN   = 'xxx'
        pgn_string = 'xxx'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'xxx'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_queen_castle_move(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1'
        pgn_string = 'O-O-O'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/2KR3R b kq - 1 1'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_king_castle_move(self, tear_down):
        # ARRANGE
        test_FEN   = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R3K2R w KQkq - 0 1'
        pgn_string = 'O-O'
        test_state = game_state.GameState(test_FEN)
        
        # ACT
        PGN_util.PGN.move_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'r3k2r/pppppppp/8/8/8/8/PPPPPPPP/R4RK1 b kq - 1 1'
        actual   = repr(test_state)
        assert expected == actual
    
class TestParseGameInPGN:
    def test_game_1(self, tear_down):
        # ARRANGE
        pgn_string = '1. e4 e5 2. Nf3 Nc6 3. Bc4  Nb4 4. Nxe5 Qg5 5. Nxf7 Qf6 6. Nxh8 d6 7. Bf7+ Ke7 8. Bxg8 g6 9. Nxg6+ Qxg6 10. Bb3 Qxg2 11. Rf1 Bg4 12. f3 Bxf3 13. Qxf3 Nxc2+'
        test_state = game_state.GameState()
        
        # ACT
        PGN_util.PGN.load_moves_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'r4b2/ppp1k2p/3p4/8/4P3/1B3Q2/PPnP2qP/RNB1KR2 w Q - 0 14'
        actual   = repr(test_state)
        assert expected == actual
        
    def test_game_2_includes_castling(self, tear_down):
        # https://lichess.org/DHRwUqp4/black#54
        # ARRANGE
        pgn_string = "1. e4 e5 2. Nf3 Nf6 3. Nc3 Nc6 4. d4 exd4 { C47 Four Knights Game: Scotch Variation Accepted } 5. Nxd4 Bc5?! { (0.13 → 0.68) Inaccuracy. Bb4 was best. } (5... Bb4 6. Nxc6 bxc6 7. Bd3 d5 8. exd5 cxd5 9. O-O O-O 10. h3) 6. Nxc6 dxc6 7. Na4?? { (0.78 → -14.08) Blunder. Qxd8+ was best. } (7. Qxd8+ Kxd8 8. f3 Re8 9. Bf4 Be6 10. O-O-O+ Kc8 11. a4 a6) 7... Bxf2+ 8. Kxf2 Qxd1 9. Nc3?! { (-15.45 → Mate in 5) Checkmate is now unavoidable. Be2 was best. } (9. Be2) 9... Qxc2+? { (Mate in 5 → -9.71) Lost forced checkmate sequence. Ng4+ was best. } (9... Ng4+ 10. Kg3 Qe1+ 11. Kf4 Qf2+ 12. Kg5 f6+ 13. Kh5 g6#) 10. Be2 Nxe4+ 11. Ke3 Nxc3 12. bxc3 Qxc3+ 13. Ke4?! { (-15.29 → Mate in 8) Checkmate is now unavoidable. Kf2 was best. } (13. Kf2) 13... Qxa1?! { (Mate in 8 → -16.31) Lost forced checkmate sequence. O-O was best. } (13... O-O 14. Kf4 Re8 15. Bh5 Qe5+ 16. Kf3 Qxh5+ 17. Kf2 Qe2+ 18. Kg3 Qg4+ 19. Kf2 Re2+ 20. Kg1) 14. Bh5 Qxa2 15. Be3 Qxg2+ 16. Bf3 Qa2 17. Bd4 Qd5+ 18. Kd3?! { (-18.75 → Mate in 11) Checkmate is now unavoidable. Ke3 was best. } (18. Ke3 Qg5+) 18... Qxf3+ 19. Be3 Qxh1 20. Bf4 Qc1?! { (Mate in 7 → -18.02) Lost forced checkmate sequence. Qf3+ was best. } (20... Qf3+ 21. Kc2 Qxf4 22. h3 Bf5+ 23. Kb3 Rd8 24. Kb2 Rd3 25. Kb1 Rb3+ 26. Ka2 Qa4#) 21. Bxc1 O-O 22. Ba3 Re8 23. Kd2 h5 24. h3 g5 25. h4 gxh4 26. Kd3?! { (-108.70 → Mate in 8) Checkmate is now unavoidable. Bc5 was best. } (26. Bc5 Bf5) 26... h3 27. Bc5 h2"
        test_state = game_state.GameState()
        
        # ACT
        PGN_util.PGN.load_moves_from_PGN(test_state, pgn_string)
        
        # ASSERT
        expected = 'r1b1r1k1/ppp2p2/2p5/2B4p/8/3K4/7p/8 w - - 0 28'
        actual   = repr(test_state)
        assert expected == actual
        