import os


class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.moves = []
        self.moved = False
        self.texture = texture
        self.set_texture()
        self.texture_rect = texture_rect

    def set_texture(self):
        self.texture = os.path.join(
            f'images/{self.color}_{self.name}.png'
        )

    def add_move(self, move):
        self.moves.append(move)

    def clear_moves(self):
        self.moves = []

    def get_value(self):
        return self.value


class Pawn(Piece):
    def __init__(self, color):
        # black is go down and white is go up
        self.en_passant = False
        if color == 'white':
            self.direction = -1
            self.pos_scores = [[8, 8, 8, 8, 8, 8, 8, 8],
                               [8, 8, 8, 8, 8, 8, 8, 8],
                               [5, 6, 6, 7, 7, 6, 6, 5],
                               [2, 3, 3, 5, 5, 3, 3, 2],
                               [1, 2, 3, 4, 4, 3, 2, 1],
                               [1, 1, 2, 3, 3, 2, 1, 1],
                               [1, 1, 1, 0, 0, 1, 1, 1],
                               [0, 0, 0, 0, 0, 0, 0, 0]]
        else:
            self.direction = 1
            self.pos_scores = [[0, 0, 0, 0, 0, 0, 0, 0],
                               [1, 1, 1, 0, 0, 1, 1, 1],
                               [1, 1, 2, 3, 3, 2, 1, 1],
                               [1, 2, 3, 4, 4, 3, 2, 1],
                               [2, 3, 3, 5, 5, 3, 3, 2],
                               [5, 6, 6, 7, 7, 6, 6, 5],
                               [8, 8, 8, 8, 8, 8, 8, 8],
                               [8, 8, 8, 8, 8, 8, 8, 8]]
        super().__init__('pawn', color, 1)


class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3)
        self.pos_scores = [[1, 1, 1, 1, 1, 1, 1, 1],
                           [1, 2, 2, 2, 2, 2, 2, 1],
                           [1, 2, 3, 3, 3, 3, 2, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 2, 3, 3, 3, 3, 2, 1],
                           [1, 2, 2, 2, 2, 2, 2, 1],
                           [1, 1, 1, 1, 1, 1, 1, 1]]


class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3)
        self.pos_scores = [[4, 3, 2, 1, 1, 2, 3, 4],
                           [3, 4, 3, 2, 2, 3, 4, 3],
                           [2, 3, 4, 3, 3, 4, 3, 2],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [2, 3, 4, 3, 3, 4, 3, 2],
                           [3, 4, 3, 2, 2, 3, 4, 3],
                           [4, 3, 2, 1, 1, 2, 3, 4]]


class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5)
        self.pos_scores = [[4, 3, 4, 4, 4, 4, 3, 4],
                           [4, 4, 4, 4, 4, 4, 4, 4],
                           [1, 1, 2, 3, 3, 2, 1, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 2, 3, 4, 4, 3, 2, 1],
                           [1, 1, 2, 2, 2, 2, 1, 1],
                           [4, 4, 4, 4, 4, 4, 4, 4],
                           [4, 3, 4, 4, 4, 4, 3, 4]]


class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9)
        self.pos_scores = [[1, 1, 1, 3, 1, 1, 1, 1],
                           [1, 2, 3, 3, 3, 1, 1, 1],
                           [1, 4, 3, 3, 3, 4, 2, 1],
                           [1, 2, 3, 3, 3, 2, 2, 1],
                           [1, 2, 3, 3, 3, 2, 2, 1],
                           [1, 4, 3, 3, 3, 4, 2, 1],
                           [1, 1, 2, 3, 3, 1, 1, 1],
                           [1, 1, 1, 3, 1, 1, 1, 1]]


class King(Piece):
    def __init__(self, color):
        self.left_rook = None
        self.right_rook = None
        super().__init__('king', color, 10000)
