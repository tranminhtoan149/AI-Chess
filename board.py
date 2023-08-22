from const import *
from square import Square
from piece import *


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
            (row-2, col+1), (row-2, col+1),
            (row+2, col+1), (row+2, col-1),
            (row-1, col+2), (row-1, col-2),
            (row+1, col+2), (row+1, col-2)]

        for move in knight_possible_moves:
            move_row, move_col = move
            # check the valid position is empty or has enemy
            if self.valid_pos(move_row, move_col):
                if self.squares[move_row][move_col].is_empty_or_has_enemy_piece(piece.color):
                    pass

    def all_possible_moves(self, piece, col, row):
        if piece.name == 'pawn':
            pass
        elif piece.name == 'knight':
            pass
        elif piece.name == 'bishop':
            pass
        elif piece.name == 'rook':
            pass
        elif piece.name == 'queen':
            pass
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
