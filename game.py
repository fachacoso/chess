import pygame
import numpy
from game_state import GameState, INITIAL_BOARD_STATE


WIDTH, HEIGHT = 1000, 1000
SQUARE_COUNT = 64
SQUARE_SIZE = WIDTH // 8
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Colors
WHITE = (145, 130, 109) 
GRAY = (100, 100, 100)
BLACK = (108,82,59)

ROWS = COLS = 8


def main():
    pygame.init()
    WINDOW.fill(GRAY)
    load_pieces()
    game_state = GameState()
    selected_piece = None
    
    
    
    run = True
    while run:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                run = False 
            #mouse listening
            mouse_pos = pygame.mouse.get_pos()
            index_hovered = get_index(mouse_pos)
            square_hovered = get_square(game_state, index_hovered)
            left_click = pygame.mouse.get_pressed()[0]
            if e.type == pygame.MOUSEBUTTONDOWN:
                # If clicked on occupied square (NEED TO ADD PLAYER CHECK)
                if get_type(square_hovered) != '-':
                        reset_square(index_hovered)
                        selected_piece = get_square(game_state, index_hovered)

            if e.type == pygame.MOUSEBUTTONUP and selected_piece:
                if index_hovered != selected_piece.index:       
                    game_state.move(selected_piece.index, index_hovered)
                selected_piece = None
            
            
                    
        update_view(game_state, selected_piece, mouse_pos)
        pygame.display.update()
        
        
    pygame.display.quit()  
    pygame.quit()
    exit()
        
        
def initialize_board():
    for i in range(64):
        reset_square(i)
        
def reset_square(index):
    white_square = (index % 2 == 0) == ((index // 8) % 2 == 0)
    pygame.draw.rect(WINDOW, WHITE if white_square else BLACK, pygame.Rect(square_by_index(index)))
    
    
    
IMAGES = {}
def load_pieces():
    pieces = ['bP', 'bR', 'bN', 'bK', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('images/' + piece + ".png").convert_alpha(), (SQUARE_SIZE, SQUARE_SIZE))
        
def update_view(game_state, selected, mouse_pos):
    initialize_board()
    for i in range(SQUARE_COUNT):
        piece = get_type(get_square(game_state, i))
        
        # Skip drawing piece selected
        if selected:
            if i == selected.index:
                continue
        
        if piece != '-':
            img = IMAGES[piece]
            WINDOW.blit(img, (getX(i) * SQUARE_SIZE, getY(i) * SQUARE_SIZE))
            
    # Draw selected piece board+pieces
    if selected:
        piece = str(selected)
        selected_img = IMAGES[piece]
        WINDOW.blit(selected_img, (numpy.subtract(mouse_pos, (SQUARE_SIZE / 2, SQUARE_SIZE / 2))))
            
            
def mouseClick():
    NotImplemented

                
                
def get_square(game_state, index):
    return game_state.board.board_pos[index]

def get_type(square):
    return str(square)
    
    
                   
            
            
    
    
def selectPiece():
    NotImplemented
        
"""def move_piece(index, piece):
    img = IMAGES[piece]
    pygame.blit(img, getX(index), getY(index))"""

def getX(index):
    return index % COLS

def getY(index):
    return index // ROWS
    
def square_by_index(index):
    x = getX(index)
    y = getY(index)
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