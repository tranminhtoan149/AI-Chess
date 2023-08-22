class Piece:
    WHITE = 'W'
    BLACK = 'B'
    def __init__(self, x, y, color, type, value):
        self.x = x
        self.y = y
        self.color = color
        self.type = type
        self.value = value
    def possible_diagonal_moves(self, board):
        moves = []
        