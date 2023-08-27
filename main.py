import sys
import pygame

from const import *
from game import Game
from square import Square
from move import Move
from minimax import Minimax
import win32api


class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("BTL2-CHESS-AI")
        self.game = Game()
        self.auto = Minimax(2)

    def mainloop(self):
        game = self.game
        screen = self.screen
        selector = self.game.selector
        board = self.game.board
        while True:
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_moves(screen)
            game.show_piece_selected(screen)
            game.show_pieces(screen)
            if game.next_player == 'black':
                if len(board.get_all_possible_moves(game.next_player)) == 0:
                    win32api.MessageBox(0, "Game is finished")
                move = self.auto.minimax_root(board, True)
                piece = board.get_piece(
                    move.final_move.row, move.final_move.col).piece

                board.move(move)
                board.set_true_en_passant(piece)
                game.show_bg(screen)
                game.show_last_move(screen)
                game.show_moves(screen)
                game.show_pieces(screen)
                game.next_turn()
                if len(board.get_all_possible_moves(game.next_player)) == 0:
                    win32api.MessageBox(0, "Game is finished")
            else:
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
                                if piece.color == game.next_player:
                                    board.all_possible_piece_moves(
                                        piece, row_selected, col_selected, True)
                                    selector.save_initial(event.pos)
                                    selector.select_piece(piece)
                                    game.show_bg(screen)
                                    game.show_moves(screen)
                                    game.show_piece_selected(screen)
                                    game.show_pieces(screen)

                        else:
                            selector.update_mouse(event.pos)
                            move_row = selector.mouse_y // SQSIZE
                            move_col = selector.mouse_x // SQSIZE
                            # possible move
                            initial = Square(selector.initial_row,
                                             selector.initial_col)
                            final = Square(move_row,
                                           move_col)
                            move = Move(initial, final)
                            if board.valid_move(selector.piece, move):
                                board.move(move)
                                board.set_true_en_passant(selector.piece)
                                game.show_bg(screen)
                                game.show_last_move(screen)
                                game.show_moves(screen)
                                game.show_pieces(screen)
                                game.next_turn()

                            selector.piece.clear_moves()
                            selector.unselect_piece()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            game.reset()
                            game = self.game
                            selector = self.game.selector
                            board = self.game.board

            pygame.display.update()


main = Main()
main.mainloop()
