
import pygame
import time



#define size of the item
DISPLAY_HEIGHT = 600
DISPLAY_WIDTH = 600
BLOCK_HEIGHT = 50*1.5
BLOCK_WIDTH = 50*1.5
FACTOR = 25 * 1.5

#define color
COLORED_BLOCK = (175,194,225)
COLOR_WHITE_BLOCK = (255,255,255)


#define piece ranking
PAWN = 0
KNIGHT = 1
BISHOP = 2
ROOK = 3
KING = 4
QUEEN = 5
BLANK = -1

BLACK_FAMILY = 'black'
WHITE_FAMILY = 'white'

class Piece:
    x = 0  # x coordinate
    y = 0  # y coordinate
    rank = 0  # rank of the piece
    life = True  # is the piece dead or alive
    family = ""
    def __init__(self, x_position, y_position, p_rank, p_family):
        self.x = x_position
        self.y = y_position
        self.rank = p_rank
        self.family = p_family

initial_board = [[ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK],
                 [PAWN, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [BLANK, ] * 8,
                 [PAWN, ] * 8,
                 [ROOK, KNIGHT, BISHOP, QUEEN, KING, BISHOP, KNIGHT, ROOK]]

        
class ChessGUI:
    def __init__(self):
        pygame.init()
        self.game_display = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pygame.display.update()
        self.clock = pygame.time.Clock()
        self.pieces = []
        
    def initialize_piece(self):
        for y,row in  enumerate(initial_board):
            for x,piece in enumerate(row):
                family = WHITE_FAMILY if y in [0,1] else BLACK_FAMILY
                if piece == BLANK:
                    continue
                elif piece == PAWN:
                    self.pieces.append(Piece(x, y, piece, family))
                    img = pygame.image.load('images/pawn_'+ family +'.png')
                elif piece == KNIGHT:
                    self.pieces.append(Piece(x, y, piece, family))
                    img = pygame.image.load('images/knight_'+ family +'.png')
                elif piece == BISHOP:
                    self.pieces.append(Piece(x, y, piece, family))
                    img = pygame.image.load('images/bishop_'+ family +'.png')
                elif piece == ROOK:
                    self.pieces.append(Piece(x, y, piece, family))
                    img = pygame.image.load('images/rook_'+ family +'.png')
                elif piece == QUEEN:
                    self.pieces.append(Piece(x, y, piece, family))
                    img = pygame.image.load('images/queen_'+ family +'.png')
                elif piece == KING:
                    self.pieces.append(Piece(x, y, piece, family))
                    img = pygame.image.load('images/king_'+ family +'.png')
                self.game_display.blit(img, ((2 * x) * FACTOR, ((2 *y) * FACTOR)))
    def board_draw(self):
        self.game_display.fill(COLORED_BLOCK)
        for i in range(8):
            if i % 2 == 0:
                j = 0
            else:
                j = 1
            while j < 8:
                pygame.draw.rect(self.game_display, COLOR_WHITE_BLOCK, (i * 50 * 1.5, j * 50 *1.5, BLOCK_WIDTH, BLOCK_HEIGHT))
                j += 2
        self.initialize_piece()
    def game(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
            self.board_draw()
            pygame.display.update()
                
                
chess_board = ChessGUI().game()