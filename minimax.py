from board import Board
import copy


class Minimax:
    def __init__(self, depth):
        self.depth = depth
        self.current_player = 'black'

    def minimax_root(self, board: Board, is_maximizing):
        self.current_player = 'black'
        possible_moves = board.get_all_possible_moves(self.current_player)
        best_move = -9999
        second_best = -9999
        third_best = -9999
        best_move_final = None
        for x in possible_moves:
            board_temp = copy.deepcopy(board)
            board_temp.move(x)
            value = self.minimax_function(
                self.depth - 1, board_temp, -10000, 10000, not is_maximizing)
            del board_temp
            if (value >= best_move):
                print("Best move: ", str(best_move_final))
                print("Best score: ", str(best_move))
                print("Second best: ", str(second_best))
                print("Third best: ", str(third_best))
                third_best = second_best
                second_best = best_move
                best_move = value
                best_move_final = x
        return best_move_final

    def minimax_function(self, depth, board: Board, alpha, beta, is_maximizing):
        self.current_player = 'white'
        if (depth == 0):
            return -self.evaluation(board)
        possible_moves = board.get_all_possible_moves(self.current_player)
        if (is_maximizing):
            best_move = -9999
            for move in possible_moves:
                board_temp = copy.deepcopy(board)
                board_temp.move(move, testing=True)
                best_move = max(best_move, self.minimax_function(
                    depth - 1, board_temp, alpha, beta, not is_maximizing))
                del board_temp
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    return best_move
            return best_move
        else:
            best_move = 9999
            for move in possible_moves:
                board_temp = copy.deepcopy(board)
                board_temp.move(move, testing=True)
                best_move = min(best_move, self.minimax_function(
                    depth - 1, board_temp, alpha, beta, not is_maximizing))
                del board_temp
                beta = min(beta, best_move)
                if beta <= alpha:
                    return best_move
            return best_move

    def evaluation(self, board: Board):
        evaluation = 0
        x = True
        for i in range(8):
            for j in range(8):
                x = board.get_piece(i, j)
                if x.has_piece():
                    pos_value = 0
                    if x.piece.name != 'king':
                        s = -1 if x.piece.color == 'black' else 1
                        pos_value = x.piece.pos_scores[i][j] * s
                    evaluation += x.piece.get_value() + pos_value
        return evaluation
