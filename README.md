# Chess [ONGOING]
Chess program written in Python for backend and Javascript for frontend.  
Front-end design inspired by lichess.org.

# Features
## Base Game
Game supports all functionalities of chess including basic movement, checks, endgames,
and even special rules including:
- [Castling](https://simple.wikipedia.org/wiki/Castling#:~:text=Castling%20is%20a%20special%20move,where%20the%20king%20has%20moved. "Castling")
- [En Passant Capture](https://en.wikipedia.org/wiki/En_passant "En Passant Capture")
- Pawn Promotion (to queen).

All functionalities thoroughly tested through automated testing using **Pytest**.  
(Pytest files can be found in "/game/tests")
## PGN and FEN Notation
Supports popular notations used to denote the game state of a chess game
### FEN Notation
Import a board state using FEN notation.  FEN notation is used to record piece positioning

Example 1:
`rnbqkbnr/8/8/8/8/8/8/RNBQKBNR w KQkq - 0 1`

Example 2:
`r4b2/ppp1k2p/3p4/8/4P3/1B3Q2/PPnP2qP/RNB1KR2 w Q - 0 14`

More information on FEN notation can be found [here](https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation "here")
### Portable Game Notation (PGN)
Import a board state using PGN.  PGN notation is used for recording chess moves.

Example 1
`1. e4 e5 2. Nf3 Nc6 3. Bc4  Nb4 4. Nxe5 Qg5 5. Nxf7 Qf6 6. Nxh8 d6 7. Bf7+ Ke7 8. Bxg8 g6 9. Nxg6+ Qxg6 10. Bb3 Qxg2 11. Rf1 Bg4 12. f3 Bxf3 13. Qxf3 Nxc2+`

Example 2:
`1. d4 d5 2. Bf4 { D00 Queen's Pawn Game: Mason Variation } e6 3. Nf3 Bd6 4. Bg3 Nf6 5. e3 Nc6 6. Bd3 e5 7. dxe5 Nxe5 8. Bxe5 Bg4 9. Nbd2 Bxe5 10. h3 Bxf3 11. Qxf3 Bxb2 12. Rd1 O-O 13. g4 Qd6 14. e4 dxe4 15. Nxe4 Nxe4 16. Bxe4 Qb4+ 17. Kf1 Rad8 18. Qf5 Rxd1+ 19. Kg2 Rxh1 20. Qxh7# { White wins by checkmate. } 1-0`

More information on PGN notation can be found [here](https://en.wikipedia.org/wiki/Portable_Game_Notation "here")

## AI
Computer has multiple difficulties using algorithms.
- Random move
- Min-Max (varying depths)
- Alpha-beta pruning

# Technologies Used
- **Flask** - Connect Python frontend and Javascript backend
- **Pytest** - Used to test piece functionality and PGN/FEN text parsing
- **Pygame** - Used to prototype game before switching to web application

# Possible Future Features
- Varying AI levels - Explore different algorithms
- Databases - Use a server to hold state of game opening possibilities of data analysis and remote play


# Why Code Chess?
As a new college graduate, I wanted to create a fairly large enough project that was not
some class project I needed to do for a grade. I had learned lots in college and gained
confidence in many skills: data analytics, Al, web development, game development,
general coding, etc. However I wanted to see if I could combine these many separate skills into one specific project, which led to me to coding chess.

I recently got into chess after learning how easy it was play against people online.
Around this time I was trying to figure out the afforementioned idea of combining, and
realized that my new found hobby was a possible solution.

If you're curious to see my chess journey, check out my lichess.org [here](https://lichess.org/@/laidbacknerd "here") containing my history, rank, and some of the many games I used to help out with testing.
