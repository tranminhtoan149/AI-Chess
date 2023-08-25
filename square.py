from piece import Piece


class Square:
    def __init__(self, row, col, piece:Piece=None):
        self.row = row
        self.col = col
        self.piece = piece

    def __eq__(self, value):
        return self.row == value.row and self.col == value.col

    def has_piece(self):
        return self.piece != None

    def is_empty(self):
        return self.piece == None

    def has_enemy(self, color):
        return self.has_piece() and self.piece.color != color

    def has_team(self, color):
        return self.has_piece() and self.piece.color == color

    def is_empty_or_has_enemy_piece(self, color):
        return self.is_empty() or self.has_enemy(color)
