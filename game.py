import pygame
from game_state import game_state, INITIAL_BOARD_STATE


WIDTH, HEIGHT = 500, 500
SQUARE_SIZE = WIDTH // 8
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess")

# Colors
WHITE = (241, 254, 198) 
GRAY = (100, 100, 100)
BLACK = (84, 106, 118)

ROWS = COLS = 8


def main():
    pygame.init()
    WINDOW.fill(GRAY)
    initialize_board()
    load_pieces()
    draw_piece()
    
    
    
    run = True
    while run:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False 
        pygame.event.get()
        pygame.display.update()
        
        
    pygame.display.quit()  
    pygame.quit()
    exit()
        
        
def initialize_board():
    for i in range(64):
        white_square = (i % 2 == 0) == ((i // 8) % 2 == 0)
        pygame.draw.rect(WINDOW, WHITE if white_square else BLACK, pygame.Rect(square_by_index(i)))
    
    
IMAGES = {}
def load_pieces():
    pieces = ['bP', 'bR', 'bN', 'bK', 'bB', 'bQ', 'bK', 'wP', 'wR', 'wN', 'wK', 'wB', 'wQ', 'wK']
    for piece in pieces:
        IMAGES[piece] = pygame.transform.scale(pygame.image.load('images/' + piece + ".png"), (SQUARE_SIZE, SQUARE_SIZE))
        
def draw_piece():
    for i in range(len(INITIAL_BOARD_STATE)):
        piece = INITIAL_BOARD_STATE[i]
        if piece != '--':
            img = IMAGES[piece]
            WINDOW.blit(img, (getX(i) * SQUARE_SIZE, getY(i) * SQUARE_SIZE))
        
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

def update_highlight():
    NotImplemented
    
main()