import pygame
import numpy
from game_state import GameState, INITIAL_BOARD_STATE
from constants import *

WINDOW = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
pygame.display.set_caption("Chess")

# Colors
LIGHT = (145, 130, 109)
DARK = (108,82,59)


def main():
    pygame.init()
    load_pieces()
    game_state = GameState()

    # Game loop
    selected_piece = None
    run = True
    while run:
        for e in pygame.event.get():
            # Quits game
            if e.type == pygame.QUIT:
                run = False
            # Mouse listening
            mouse_pos = pygame.mouse.get_pos()
            index_hovered = get_index(mouse_pos)
            square_hovered = get_square(game_state, index_hovered)
            if e.type == pygame.MOUSEBUTTONDOWN:
                # If clicked on occupied square, hold selected piece (NEED TO ADD PLAYER CHECK)
                if is_piece(square_hovered):
                        reset_square(index_hovered)
                        selected_piece = get_square(game_state, index_hovered)

            # Lets go of piece
            if e.type == pygame.MOUSEBUTTONUP and selected_piece:
                if index_hovered != selected_piece.index:
                    game_state.move(selected_piece.index, index_hovered)
                selected_piece = None


        # Updates each frame
        update_view(game_state, selected_piece, mouse_pos)
        pygame.display.update()


    pygame.display.quit()
    pygame.quit()
    exit()


# Creates board
def initialize_board():
    for i in range(SQUARE_COUNT):
        reset_square(i)

# Redraws an empty square
def reset_square(index):
    light_square = (index % 2 == 0) == ((index // 8) % 2 == 0)
    pygame.draw.rect(WINDOW, LIGHT if light_square else DARK, pygame.Rect(square_by_index(index)))



IMAGES = {}
# Load all .png's of pieces
def load_pieces():
    pieces = ['bP', 'bR', 'bN', 'bK', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('images/' + piece + ".png").convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))

def update_view(game_state, selected, mouse_pos):
    initialize_board()
    for i in range(SQUARE_COUNT):

        # Skip drawing piece selected
        if selected:
            if i == selected.index:
                continue

        square = get_square(game_state, i)

        if is_piece(square):
            piece = repr(square)
            img = IMAGES[piece]
            WINDOW.blit(img, (get_X(i) * SQUARE_SIZE, get_Y(i) * SQUARE_SIZE))

    # Draw selected piece
    if selected:
        piece = repr(selected)
        selected_img = IMAGES[piece]
        WINDOW.blit(selected_img, (numpy.subtract(mouse_pos, (SQUARE_SIZE / 2, SQUARE_SIZE / 2))))


def get_square(game_state, index):
    return game_state.board.board_pos[index]

def is_piece(square):
    return str(square) != '-'

def get_X(index):
    return index % 8

def get_Y(index):
    return index // 8

def square_by_index(index):
    x = get_X(index)
    y = get_Y(index)
    x_start = x * SQUARE_SIZE
    y_start = y * SQUARE_SIZE
    x_end = y_end = SQUARE_SIZE
    return x_start, y_start, x_end, y_end

def get_index(coordinate):
    col = coordinate[0] // SQUARE_SIZE
    row = coordinate[1] // SQUARE_SIZE
    index = col + row * 8
    return index

def update_highlight():
    NotImplemented

main()
