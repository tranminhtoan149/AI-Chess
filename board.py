from const import *
from square import Square
from piece import *
from move import Move


class Board:
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self._create()
        self._add_pieces('white')
        self._add_pieces('black')

    def valid_pos(self, *args):
        for arg in args:
            if arg < 0 or arg > 7:
                return False
        return True

    def knight_moves(self, piece, row, col):
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
                    final_move = Square(move_row, move_col)
                    move = Move(init_move, final_move)
                    piece.add_move(move)

    def pawn_moves(self, piece, row, col):
        steps = 1 if piece.moved else 2
        start = row + piece.direction
        end = row + (piece.direction * (1 + steps))
        for move_row in range(start, end, piece.direction):
            if self.valid_pos(move_row):
                if self.squares[move_row][col].is_empty():
                    init_move = Square(row, col)
                    final_move = Square(move_row, col)
                    move = Move(init_move, final_move)
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
                    final_move = Square(possible_move_row, possible_move_col)
                    move = Move(init_move, final_move)
                    piece.add_move(move)

    def straight_moves(self, piece, row, col, increments):
        for increment in increments:
            row_incr, col_incr = increment
            possible_move_row = row + row_incr
            possible_move_col = col + col_incr
            while self.valid_pos(possible_move_row, possible_move_col):
                init_move = Square(row, col)
                final_move = Square(possible_move_row, possible_move_col)
                move = Move(init_move, final_move)

                # empty square
                if self.squares[possible_move_row][possible_move_col].is_empty():
                    piece.add_move(move)

                # stop if there is enemy but add move
                if self.squares[possible_move_row][possible_move_col].has_enemy(piece.color):
                    piece.add_move(move)
                    break

                # stop if there is team but not add move
                if self.squares[possible_move_row][possible_move_col].has_team(piece.color):
                    break
                possible_move_row = possible_move_row + row_incr
                possible_move_col = possible_move_col + col_incr

    def king_moves(self, piece, row, col):
        pass

    def all_possible_moves(self, piece, row, col):
        if piece.name == 'pawn':
            self.pawn_moves(piece, row, col)
        elif piece.name == 'knight':
            self.knight_moves(piece, row, col)
        elif piece.name == 'bishop':
            self.straight_moves(piece, row, col, [
                (1, 1),     # down-right
                (1, -1),    # down-left
                (-1, 1),    # up-right
                (-1, -1)    # up-left
            ])
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
            ])
        elif piece.name == 'king':
            pass

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
