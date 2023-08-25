from const import *
from square import Square
from piece import *
from move import Move
import copy
from typing import List


class Board(object):
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for _ in range(COLS)]
        self.last_move = None
        self.is_game_over = False
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def valid_pos(self, *args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    def get_piece(self, x, y):
        return self.squares[x][y]

    def knight_moves(self, piece, row, col, bool=False):
        knight_possible_moves = [
            (row-2, col+1), (row-2, col-1),
            (row+2, col+1), (row+2, col-1),
            (row-1, col+2), (row-1, col-2),
            (row+1, col+2), (row+1, col-2)]

        for move in knight_possible_moves:
            move_row, move_col = move
            # check the valid position is empty or has enemy
            if self.valid_pos(move_row, move_col):
                if self.squares[move_row][move_col].is_empty_or_has_enemy_piece(piece.color):
                    init_move = Square(row, col)
                    final_piece = self.squares[move_row][move_col].piece
                    final_move = Square(move_row, move_col, final_piece)
                    move = Move(init_move, final_move)
                    # check move
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                        else:
                            break
                    else:
                        piece.add_move(move)

    def pawn_moves(self, piece, row, col, bool=False):
        steps = 1 if piece.moved else 2
        start = row + piece.direction
        end = row + (piece.direction * (1 + steps))
        for move_row in range(start, end, piece.direction):
            if self.valid_pos(move_row):
                if self.squares[move_row][col].is_empty():
                    init_move = Square(row, col)
                    final_move = Square(move_row, col)
                    move = Move(init_move, final_move)
                    # check move
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                else:
                    break
            else:
                break
        # diagonal move
        possible_move_row = row + piece.direction
        possible_moves_col = [col-1, col+1]
        for possible_move_col in possible_moves_col:
            if self.valid_pos(possible_move_col, possible_move_row):
                if self.squares[possible_move_row][possible_move_col].has_enemy(piece.color):
                    init_move = Square(row, col)
                    final_piece = self.squares[possible_move_row][possible_move_col].piece
                    final_move = Square(possible_move_row,
                                        possible_move_col, final_piece)
                    move = Move(init_move, final_move)
                    # check move
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)

        # en passant moves
        r = 3 if piece.color == 'white' else 4
        fr = 2 if piece.color == 'white' else 5
        # left en pessant
        if self.valid_pos(col-1) and row == r:
            if self.squares[row][col-1].has_enemy(piece.color):
                p = self.squares[row][col-1].piece
                if isinstance(p, Pawn):
                    if p.en_passant:
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(fr, col-1, p)
                        # create a new move
                        move = Move(initial, final)

                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

        # right en pessant
        if self.valid_pos(col+1) and row == r:
            if self.squares[row][col+1].has_enemy(piece.color):
                p = self.squares[row][col+1].piece
                if isinstance(p, Pawn):
                    if p.en_passant:
                        # create initial and final move squares
                        initial = Square(row, col)
                        final = Square(fr, col+1, p)
                        # create a new move
                        move = Move(initial, final)
                        # check potencial checks
                        if bool:
                            if not self.in_check(piece, move):
                                # append new move
                                piece.add_move(move)
                        else:
                            # append new move
                            piece.add_move(move)

    def straight_moves(self, piece, row, col, increments, bool=False):
        for increment in increments:
            row_incr, col_incr = increment
            possible_move_row = row + row_incr
            possible_move_col = col + col_incr
            while self.valid_pos(possible_move_row, possible_move_col):
                init_move = Square(row, col)
                final_piece = self.squares[possible_move_row][possible_move_col].piece
                final_move = Square(possible_move_row,
                                    possible_move_col, final_piece)
                move = Move(init_move, final_move)

                # empty square
                if self.squares[possible_move_row][possible_move_col].is_empty():
                    # check move
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)

                # stop if there is enemy but add move
                elif self.squares[possible_move_row][possible_move_col].has_enemy(piece.color):
                   # check move
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                    else:
                        piece.add_move(move)
                    break

                # stop if there is team but not add move
                elif self.squares[possible_move_row][possible_move_col].has_team(piece.color):
                    break
                possible_move_row = possible_move_row + row_incr
                possible_move_col = possible_move_col + col_incr

    def king_moves(self, piece, row, col, bool=False):
        adjs = [
            (row-1, col),  # up
            (row-1, col + 1),  # up right
            (row-1, col - 1),  # up left
            (row+1, col),  # down
            (row+1, col + 1),  # down right
            (row+1, col - 1),  # down left
            (row, col + 1),  # right
            (row, col - 1)  # left
        ]
        for move in adjs:
            move_row, move_col = move
            # check the valid position is empty or has enemy
            if self.valid_pos(move_row, move_col):
                if self.squares[move_row][move_col].is_empty_or_has_enemy_piece(piece.color):
                    init_move = Square(row, col)
                    final_move = Square(move_row, move_col)
                    move = Move(init_move, final_move)
                    if bool:
                        if not self.in_check(piece, move):
                            piece.add_move(move)
                        else:
                            break
                    else:
                        piece.add_move(move)

        if not piece.moved:
            # queen castling
            # check left rook is a rook
            if self.squares[row][0].has_piece():
                left_rook = self.squares[row][0].piece
                if left_rook.name == 'rook' and not left_rook.moved:
                    for c in range(1, 4):
                        if self.squares[row][c].has_piece():
                            break
                        if c == 3:
                            piece.left_rook = left_rook
                            # move rook
                            initial = Square(row, 0)
                            final = Square(row, 3)
                            move_rook = Move(initial, final)
                            # king move
                            initial = Square(row, col)
                            final = Square(row, 2)
                            move_king = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move_king) and not self.in_check(left_rook, move_rook):
                                    left_rook.add_move(move_rook)
                                    piece.add_move(move_king)
                            else:
                                left_rook.add_move(move_rook)
                                piece.add_move(move_king)
            if self.squares[row][7].has_piece():
                right_rook = self.squares[row][7].piece
                if right_rook.name == 'rook' and not right_rook.moved:
                    for c in range(5, 7):
                        if self.squares[row][c].has_piece():
                            break
                        if c == 6:
                            piece.right_rook = right_rook
                            # move rook
                            initial = Square(row, 7)
                            final = Square(row, 5)
                            move_rook = Move(initial, final)
                            # king move
                            initial = Square(row, col)
                            final = Square(row, 6)
                            move_king = Move(initial, final)
                            if bool:
                                if not self.in_check(piece, move_king) and not self.in_check(right_rook, move_rook):
                                    right_rook.add_move(move_rook)
                                    piece.add_move(move_king)
                            else:
                                right_rook.add_move(move_rook)
                                piece.add_move(move_king)

    def move(self, move: Move):
        # print(move)
        init_move = move.init_move
        final_move = move.final_move
        piece = self.squares[init_move.row][init_move.col].piece

        en_passant_empty = self.squares[final_move.row][final_move.col].is_empty(
        )

        # change init and final
        self.squares[init_move.row][init_move.col].piece = None
        self.squares[final_move.row][final_move.col].piece = piece
        if isinstance(piece, Pawn):
            # en passant capture
            diff = final_move.col - init_move.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[init_move.row][init_move.col + diff].piece = None
                self.squares[final_move.row][final_move.col].piece = piece

            # pawn promotion
            else:
                self.check_promotion(piece, final_move)

        # check king castling
        if piece.name == 'king' and self.castling(init_move, final_move):
            diff = final_move.col - init_move.col
            rook = piece.left_rook if (diff < 0) else piece.right_rook
            self.move(rook, rook.moves[-1])
        # move and clear valid move
        piece.moved = True
        piece.clear_moves()
        # check if game is over
        if isinstance(final_move.piece, King):
            self.is_game_over = True

        self.last_move = move

    def valid_move(self, piece, move):
        return move in piece.moves

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)

    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2

    def set_true_en_passant(self, piece):
        if not isinstance(piece, Pawn):
            return
        for row in range(ROWS):
            for col in range(COLS):
                if isinstance(self.squares[row][col].piece, Pawn):
                    self.squares[row][col].piece.en_passant = False

        piece.en_passant = True

    def in_check(self, piece, move):
        temp_board = copy.deepcopy(self)
        temp_board.move(move)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.all_possible_piece_moves(p, row, col, False)
                    for p_move in p.moves:
                        if isinstance(p_move.final_move.piece, King):
                            return True
        return False

    def all_possible_piece_moves(self, piece, row, col, bool=False):
        if piece.name == 'pawn':
            self.pawn_moves(piece, row, col, bool)
        elif piece.name == 'knight':
            self.knight_moves(piece, row, col, bool)
        elif piece.name == 'bishop':
            self.straight_moves(piece, row, col, [
                (1, 1),     # down-right
                (1, -1),    # down-left
                (-1, 1),    # up-right
                (-1, -1)    # up-left
            ], bool)
        elif piece.name == 'rook':
            self.straight_moves(piece, row, col, [
                (1, 0),     # down
                (-1, 0),    # up
                (0, 1),     # right
                (0, -1)     # left
            ])
        elif piece.name == 'queen':
            self.straight_moves(piece, row, col, [
                (1, 0),     # down
                (-1, 0),    # up
                (0, 1),     # right
                (0, -1),    # left
                (1, 1),     # down-right
                (1, -1),    # down-left
                (-1, 1),    # up-right
                (-1, -1)    # up-left
            ], bool)
        elif piece.name == 'king':
            self.king_moves(piece, row, col, bool)

    def _create(self):
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[col][row] = Square(row, col)

    def _add_pieces(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # King
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def get_all_possible_moves(self) -> List[Move]:
        all_possible_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_team('black'):
                    self.all_possible_piece_moves(
                        self.squares[row][col].piece, row, col, True)
                    if len(self.squares[row][col].piece.moves) > 0:
                        all_possible_moves.extend(
                            self.squares[row][col].piece.moves)
        return all_possible_moves
