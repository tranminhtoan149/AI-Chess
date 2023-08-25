import sunfish
import math
import random
import sys

class Minimax:
    def __init__(self,depth):
        self.depth = depth
        self.best_move = -9999
        self.second_best = -9999
        self.third_best = -9999
    def minimax_root(self,depth, board,is_maximizing):
        possibleMoves = board.legal_moves
        bestMoveFinal = None
        for x in possibleMoves:
            move = chess.Move.from_uci(str(x))
            board.push(move)
            value = max(self.best_move, self.minimax(depth - 1, board, not is_maximizing))
            board.pop()
            if( value > self.best_move):
                print("Best score: " ,str(self.best_move))
                print("Best move: ",str(bestMoveFinal))
                print("Second best: ", str(self.second_best))
                self.third_best = self.second_best
                self.second_best = self.best_move
                self.best_move = value
                bestMoveFinal = move
        return bestMoveFinal

    def minimax(self, depth, board, is_maximizing):
        if(depth == 0):
            return - self.evaluation(board)
        possibleMoves = board.legal_moves
        if(is_maximizing):
            bestMove = -9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMove = max(bestMove,minimax(depth - 1, board, not is_maximizing))
                board.pop()
            return bestMove
        else:
            bestMove = 9999
            for x in possibleMoves:
                move = chess.Move.from_uci(str(x))
                board.push(move)
                bestMove = min(bestMove, minimax(depth - 1, board, not is_maximizing))
                board.pop()
            return bestMove

    def evaluation(board):
        i = 0
        evaluation = 0
        x = True
        try:
            x = bool(board.piece_at(i).color)
        except AttributeError as e:
            x = x
        while i < 63:
            i += 1
            evaluation = evaluation + (getPieceValue(str(board.piece_at(i))) if x else -getPieceValue(str(board.piece_at(i))))
        return evaluation


    def getPieceValue(self, piece):
        if(piece == None):
            return 0
        value = 0
        if piece == "P" or piece == "p":
            value = 10
        if piece == "N" or piece == "n":
            value = 30
        if piece == "B" or piece == "b":
            value = 30
        if piece == "R" or piece == "r":
            value = 50
        if piece == "Q" or piece == "q":
            value = 90
        if piece == 'K' or piece == 'k':
            value = 900
        #value = value if (board.piece_at(place)).color else -value
        return value

def main():
    board = chess.Board()
    n = 0
    print(board)
    while n < 100:
        if n%2 == 0:
            move = input("Enter move: ")
            move = chess.Move.from_uci(str(move))
            board.push(move)
        else:
            print("Computers Turn:")
            move = minimaxRoot(4,board,True)
            move = chess.Move.from_uci(str(move))
            board.push(move)
        print(board)
        n += 1
