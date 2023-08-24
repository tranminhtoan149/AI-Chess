class Move:
    def __init__(self, init_move, final_move):
        self.init_move = init_move
        self.final_move = final_move

    def __str__(self):
        s = ''
        s += f'({self.init_move.col},{self.init_move.row})'
        s += f'-> ({self.final_move.col},{self.final_move.row})'
        return s

    def __eq__(self, value):
        return self.init_move == value.init_move and self.final_move == value.final_move
