import chess
board = chess.Board()
board.push_san("Nh3")
board.push_san("a5")
board.push_san("b4")
board.push_san("axb4")
print(board)