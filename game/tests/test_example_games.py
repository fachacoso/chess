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
        
    def test_game_2(self, tear_down):
        # ARRANGE
        pgn_string = "1. e4 e5 2. d3 Nf6 3. f4 Bc5 { B02 King's Pawn Game: Clam Variation, Radisch Gambit } 4. fxe5 Ng8 5. d4 Bb6 6. Nf3 d6 7. Bf4 dxe5 8. Bxe5 f6 9. Bf4 Nc6 10. Nc3 Bxd4 11. Nxd4 Nxd4 12. Bb5+ c6 13. Bc4 f5 14. Qd3 Nf6 15. exf5 Bxf5 16. Qxf5 Nxf5 17. O-O Kd7 18. Rad1+ Kc8 19. Rxd8+ Rxd8 20. Be6+ Nd7 21. Bxf5 b6 22. Rd1 g6 23. Bxd7+ Rxd7 24. Rxd7 Kxd7 25. h3 Re8 26. Kh2 Re2 27. Na4 Rxc2 28. Bb8 b5 29. Nb6+ Kd8 30. Bxa7 Rxb2 31. Bb8 Rxa2 32. Bd6 Ra6 { Black wins on time. } 0-1"
        test_state = game_state.GameState()

        # ACT
        PGN_util.PGN.load_moves_from_PGN(test_state, pgn_string)

        # ASSERT
        expected = "3k4/7p/rNpB2p1/1p6/8/7P/6PK/8 w - - 2 33"
        actual = repr(test_state)
        assert expected == actual
        
    def test_game_3(self, tear_down):
        # https://lichess.org/ihDKlJo1/black
        # ARRANGE
        pgn_string = "1. d3 e5 2. e4 { C20 King's Pawn Game: Leonardis Variation } Nf6 3. Nc3 Bc5 4. Be3 d6 5. Bxc5 dxc5 6. Nd5 Ng4 7.  h3 Nf6 8. Nxf6+ Qxf6 9. Qf3 Nd7 10. Qxf6 Nxf6 11. Nf3 Bd7 12. Nxe5 Be6 13. Be2 g6 14. Ng4 Nxg4 15. Bxg4 O-O 16. Bxe6 fxe6 17. O-O Rad8 18. f3 c4 19. Rad1 b5 20. dxc4 bxc4 21. Rxd8 Rxd8 22. Kh2 Rd2 23. Rc1 c5 24. b3 cxb3 25. axb3 a5 26. c4 Rb2 27. Rc3 Rd2 28. Kg3 Rd8 29. Kf4 h5 30. Ke5 Kf7 31. g4 Ra8 { Black wins on time. } 0-1"
        test_state = game_state.GameState()

        # ACT
        PGN_util.PGN.load_moves_from_PGN(test_state, pgn_string)

        # ASSERT
        expected = "r7/5k2/4p1p1/p1p1K2p/2P1P1P1/1PR2P1P/8/8 w - - 1 32"
        actual = repr(test_state)
        assert expected == actual
        
    def test_game_4(self, tear_down):
        # https://lichess.org/r2DWsqyX/white
        # ARRANGE
        pgn_string = "1. e4 e5 2. Nf3 Nc6 3. Bc4 h6 { C50 Italian Game: Anti-Fried Liver Defense } 4. d4 Bb4+?! { (0.85 → 1.90) Inaccuracy. exd4 was best. } (4... exd4 5. Nxd4 Nf6 6. Nc3 Bb4 7. Nxc6 bxc6 8. O-O O-O 9. e5) 5. c3 Bd6 6. h4? { (2.16 → 0.65) Mistake. O-O was best. } (6. O-O Nge7 7. Bb3 O-O 8. Nxe5 Nxe5 9. dxe5 Bc5 10. Bf4 b5) 6... Na5?? { (0.65 → 5.07) Blunder. Nf6 was best. } (6... Nf6) 7. Bd3?? { (5.07 → 2.39) Blunder. Bxf7+ was best. } (7. Bxf7+ Kxf7 8. dxe5 Bc5 9. Qd5+ Ke8 10. Qxc5 b6 11. Qb5 Qe7 12. Qe2 Nc6 13. Bf4 a5) 7... Nf6?? { (2.39 → 7.14) Blunder. Nc6 was best. } (7... Nc6 8. O-O) 8. dxe5 Bxe5 9. Nxe5 Qe7 10. Nc4 Nxc4 11. Bxc4 d6 12. Nd2 O-O 13. Qf3?! { (7.07 → 4.97) Inaccuracy. O-O was best. } (13. O-O Re8 14. Bb3 d5 15. exd5 Bg4 16. f3 Bh5 17. Rf2 Rad8 18. Nf1 Nxd5 19. Bxd5 c6) 13... Be6?! { (4.97 → 7.15) Inaccuracy. d5 was best. } (13... d5) 14. b3?! { (7.15 → 5.25) Inaccuracy. Bxe6 was best. } (14. Bxe6 Qxe6) 14... Bxc4 15. Nxc4 Rad8 16. Ba3?! { (6.61 → 4.90) Inaccuracy. O-O was best. } (16. O-O Rfe8) 16... Nxe4 17. O-O-O Nxc3? { (4.76 → 9.00) Mistake. f5 was best. } (17... f5 18. Ne3 b5 19. Nxf5 Qe6 20. Rhe1 Rde8 21. Rd4 Rxf5 22. Rdxe4 Rxf3 23. Rxe6 Rxe6 24. Rxe6) 18. Qxc3 d5 19. Ne3?! { (16.69 → 5.54) Inaccuracy. Bxe7 was best. } (19. Bxe7 dxc4 20. Bxd8 cxb3 21. Qxb3 b6 22. Bxc7 g6 23. Rd7 Kg7 24. Qd5 Kg8 25. g3 h5) 19... d4?! { (5.54 → 16.07) Inaccuracy. Qxa3+ was best. } (19... Qxa3+ 20. Kb1) 20. Rxd4 Rxd4 21. Qxd4 Qxa3+ 22. Kb1 Re8 23. Qb2 Qd6 24. Rd1 Qf4 25. Nd5?! { (7.17 → 5.23) Inaccuracy. g3 was best. } (25. g3) 25... Qxh4 26. Nxc7? { (4.95 → 3.02) Mistake. Ne3 was best. } (26. Ne3 h5) 26... Re7?? { (3.02 → 6.31) Blunder. Rd8 was best. } (26... Rd8) 27. Nd5 Rd7 28. Ka1 Qe4 29. Nc3?? { (5.91 → 0.94) Blunder. Qd4 was best. } (29. Qd4 Qe6) 29... Qxg2?? { (0.94 → 9.36) Blunder. Rxd1+ was best. } (29... Rxd1+ 30. Nxd1 Qxg2 31. Qe2 Qd5 32. Ne3 Qe4 33. Kb2 g6 34. Kc1 h5 35. Kd2 Qb1 36. Nc2) 30. Rxd7 Qf1+ 31. Nb1 Qb5 32. Rxb7?? { (9.69 → 2.84) Blunder. Qd4 was best. } (32. Qd4 a6 33. Nc3 Qc6 34. Kb2 b5 35. Ra7 Qe6 36. Rb7 f6 37. Rb6 Qe5 38. Qxe5 fxe5) 32... Qa6?? { (2.84 → 9.84) Blunder. Qxb7 was best. } (32... Qxb7 33. Qd4) 33. Rb4 Qa5 34. Rd4 Qc5 35. Rd1 Qh5 36. Rc1 Qg5 37. a3 Qe7 38. a4 a5 39. Rc5?? { (10.00 → 3.13) Blunder. Nd2 was best. } (39. Nd2 Qd6 40. Rc8+ Kh7 41. Nc4 Qf4 42. Ra8 Qe4 43. Ra7 f6 44. Rxa5 Qd3 45. Ra7 Qd1+) 39... Qb7?? { (3.13 → 10.20) Blunder. Qxc5 was best. } (39... Qxc5 40. Qc3 Qf5 41. Nd2 h5 42. Kb2 h4 43. Qf3 Qe5+ 44. Kc2 g5 45. Kd3 Kg7 46. Qg4) 40. Rxa5 Qb6 41. Rb5 Qe6 42. Ka2 Qd6 43. Rb8+ Kh7 44. Rb4?! { (13.97 → 6.51) Inaccuracy. Qc2+ was best. } (44. Qc2+) 44... Qe7?! { (6.51 → 10.46) Inaccuracy. Qxb4 was best. } (44... Qxb4 45. Qd2) 45. a5 { White wins on time. } 1-0"
        test_state = game_state.GameState()

        # ACT
        PGN_util.PGN.load_moves_from_PGN(test_state, pgn_string)

        # ASSERT
        expected = "8/4qppk/7p/P7/1R6/1P6/KQ3P2/1N6 b - - 0 45"
        actual = repr(test_state)
        assert expected == actual