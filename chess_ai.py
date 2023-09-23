import chess_engine

board = []
game = chess_engine.ChessGame()

def set_board(_board, _game):
    global board
    global game
    board = _board
    game = _game
    game.set_board(_board)

def count_moves():
    ret = 0
    for i in range(0, 8):
        for j in range(0, 8):
            if game.board[i][j][1] != game.get_turn():
                continue
            ret += len(game.get_moves(i, j))
            ret += len(game.get_attacks(i, j))
    print("available moves:", ret)
    return ret