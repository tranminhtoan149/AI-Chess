import sys
import pygame

from const import *
from game import Game


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BTL2-CHESS-AI")
        self.game = Game()

    def mainloop(self):
        game = self.game
        screen = self.screen
        selector = self.game.selector
        board = self.game.board
        while True:
            game.show_bg(screen)
            game.show_moves(screen)
            game.show_piece_selected(screen)
            game.show_pieces(screen)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # check if there are any piece selected
                    if selector.selecting == False:
                        selector.update_mouse(event.pos)
                        col_selected = selector.mouse_x // SQSIZE
                        row_selected = selector.mouse_y // SQSIZE
                        # check piece at row, col select
                        if board.squares[row_selected][col_selected].has_piece():
                            piece = board.squares[row_selected][col_selected].piece
                            board.all_possible_moves(
                                piece, row_selected, col_selected)
                            selector.save_initial(event.pos)
                            selector.select_piece(piece)
                            game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_piece_selected(screen)
                            game.show_pieces(screen)

                    else:
                        selector.unselect_piece()

            pygame.display.update()


main = Main()
main.mainloop()
