import pygame
import numpy
from game_state import GameState
from constants import *

BOARD_SIZE = 1000
SQUARE_SIZE = BOARD_SIZE // 8
WINDOW = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Chess")

# Colors
LIGHT = (145, 130, 109)
DARK = (108, 82, 59)


def main():
    pygame.init()
    load_pieces()
    game_state = GameState()

    # Game loop
    selected_index = None
    run = True
    while run:
        for e in pygame.event.get():
            # Quits game
            if e.type == pygame.QUIT:
                run = False
            # Mouse listening
            mouse_pos = pygame.mouse.get_pos()
            index_hovered = get_index(mouse_pos)
            square_hovered = game_state.get_square(index_hovered)
            if e.type == pygame.MOUSEBUTTONDOWN:
                # If clicked on occupied square, hold selected piece (NEED TO ADD PLAYER CHECK)
                if not square_hovered.is_empty():
                    piece = square_hovered.get_piece()
                    if piece.player == game_state.turn:
                        reset_square(index_hovered)
                        selected_index = index_hovered

            # Lets go of piece
            if e.type == pygame.MOUSEBUTTONUP and type(selected_index) == int:
                if index_hovered != selected_index:
                    game_state.move(selected_index, index_hovered)
                selected_index = None


        # Updates each frame
        update_view(game_state, selected_index, mouse_pos)
        pygame.display.update()


    pygame.display.quit()
    pygame.quit()
    exit()


# Creates board
def draw_board():
    for square_index in range(SQUARE_COUNT):
        reset_square(square_index)

# Redraws an empty square
def reset_square(index):
    light_square = (index % 2 == 0) == ((index // 8) % 2 == 0)
    pygame.draw.rect(WINDOW, LIGHT if light_square else DARK, pygame.Rect(square_by_index(index)))



IMAGES = {}
# Load all .png's of pieces
def load_pieces():
    pieces = ['bP', 'bR', 'bN', 'bK', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('../images/' + piece + ".png").convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))

def update_view(game_state, selected_index, mouse_pos):
    draw_board()
    for square_index in range(SQUARE_COUNT):

        # Skip drawing piece selected/being held
        if type(selected_index) == int:
            if square_index == selected_index:
                continue
        square = game_state.get_square(square_index)
        if not square.is_empty():
            draw_piece(game_state, square_index)

    # Draw selected/held piece on top of board and pieces
    if type(selected_index) == int:
        draw_piece(game_state, selected_index, mouse_pos)

# Helper functions

def draw_piece(game_state, square_index, mouse_pos = None):
    """Takes square and draws piece in it. If there is a mouse_pos, draw piece centered on mouse."""
    square = game_state.get_square(square_index)
    piece = square.get_piece()
    piece_player = piece.player
    piece_notation = piece.notation
    img = IMAGES[piece_player + piece_notation]
    if mouse_pos:
        WINDOW.blit(img, (numpy.subtract(mouse_pos, (SQUARE_SIZE / 2, SQUARE_SIZE / 2))))
    else:
        WINDOW.blit(img, (get_x(square_index) * SQUARE_SIZE, get_y(square_index) * SQUARE_SIZE))
        
    
def get_x(index):
    return index % 8

def get_y(index):
    return 7 - index // 8   
    
def square_by_index(index):
    x = get_x(index)
    y = get_y(index)
    x_start = x * SQUARE_SIZE
    y_start = y * SQUARE_SIZE
    x_end = y_end = SQUARE_SIZE
    return x_start, y_start, x_end, y_end

def get_index(coordinate):
    col = coordinate[0] // SQUARE_SIZE
    row = 7 - coordinate[1] // SQUARE_SIZE
    index = col + row * 8
    return index


def update_highlight():
    NotImplemented


main()
