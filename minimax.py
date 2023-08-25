from board import Board
import copy


class Minimax:
    def __init__(self,depth):
        self.depth = depth
        self.best_move = -9999
        self.second_best = -9999
        self.third_best = -9999

    def minimax_root(self, board:Board, is_maximizing):
        possibleMoves = board.get_all_possible_moves()
        print(possibleMoves)
        bestMoveFinal = possibleMoves[0]
        for x in possibleMoves:
            board_temp = copy.deepcopy(board)
            board_temp.move(x)
            value = max(self.best_move, self.minimax(self.depth - 1, board_temp, not is_maximizing))
            del board_temp
            if( value > self.best_move):
                print("Best score: " ,str(self.best_move))
                print("Best move: ",str(bestMoveFinal))
                print("Second best: ", str(self.second_best))
                self.third_best = self.second_best
                self.second_best = self.best_move
                self.best_move = value
                bestMoveFinal = x
        return bestMoveFinal

    def minimax(self, depth, board:Board, is_maximizing):
        if(depth == 0):
            return - self.evaluation(board)
        possibleMoves = board.get_all_possible_moves()
        if(is_maximizing):
            bestMove = -9999
            for move in possibleMoves:
                board_temp = copy.deepcopy(board)
                board_temp.move(move)
                bestMove = max(bestMove, self.minimax(depth - 1, board_temp, not is_maximizing))
                del board_temp
            return bestMove
        else:
            bestMove = 9999
            for move in possibleMoves:
                board_temp = copy.deepcopy(board)
                board_temp.move(move)
                bestMove = min(bestMove, self.minimax(depth - 1, board_temp, not is_maximizing))
                del board_temp
            return bestMove

    def evaluation(self, board: Board):
        evaluation = 0
        x = True
        for i in range(8):
            for j in range(8):
                x = board.get_piece(i, j)
                if x.has_piece():
                    evaluation += -x.piece.get_value()
        return evaluation

# def main():
#     board = Board()
#     n = 0
#     print(board)
#     while n < 100:
#         if n%2 == 0:
#             move = input("Enter move: ")
#             move = Board.move(move)
#             board.push(move)
#         else:
#             print("Computers Turn:")
#             move = minimaxRoot(4,board,True)
#             move = chess.Move.from_uci(str(move))
#             board.push(move)
#         print(board)
#         n += 1
