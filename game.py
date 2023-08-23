import pygame

from const import *

from board import Board
from selector import Selector


class Game:
    def __init__(self):
        self.board = Board()
        self.selector = Selector()

    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200)
                else:
                    color = (119, 154, 88)
                rect = (col * SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    img = pygame.image.load(piece.texture)
                    img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                    piece.texture_rect = img.get_rect(center=img_center)
                    surface.blit(img, piece.texture_rect)

    def show_moves(self, surface):
        if self.selector.selecting:
            piece = self.selector.piece
            for move in piece.moves:
                color = '#C86464' if (
                    move.final_move.row + move.final_move.col) % 2 == 0 else '#C84646'
                rect = (move.final_move.col * SQSIZE,
                        move.final_move.row*SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)

    def show_piece_selected(self, surface):
        if self.selector.selecting:
            rect = (self.selector.initial_col * SQSIZE,
                    self.selector.initial_row*SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, '#FDAC53', rect)
