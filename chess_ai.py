import chess_engine
import time

INF = 1e9
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

piece_point = {"KING":20, "QUEEN": 9, "ROOK": 5, "KNIGHT": 3, "BISHOP": 3, "PAWN": 1}

def eval():
    # just testing a simple eval function
    return game.relative_score

cnt = 0

def minimax(depth):
    if(depth == 0):
        global cnt
        cnt += 1
        return eval(), None, None
    
    best_piece = (-1, -1)
    best_move = (-1, -1)
    best_score = -INF if (game.turn % 2 == 0) else INF
    c = 1 if game.turn % 2 == 0 else -1

    for i in range(0, 8):
        for j in range(0, 8):
            if game.board[i][j][1] != game.get_turn():
                continue
            # moving
            for next_cell in game.get_moves(i, j):
                game.move_piece((i, j), next_cell)
                tmp = minimax(depth - 1)
                if tmp[0] * c > best_score * c:
                    best_score = tmp[0]
                    best_piece = (i, j)
                    best_move = next_cell
                game.move_piece(next_cell, (i, j))
            # capturing
            for next_cell in game.get_attacks(i, j):
                last = game.board[next_cell[0]][next_cell[1]], game.relative_score
                game.attack_piece((i, j), next_cell)
                tmp = minimax(depth - 1)
                if tmp[0] * c > best_score * c:
                    best_score = tmp[0]
                    best_piece = (i, j)
                    best_move = next_cell
                game.move_piece(next_cell, (i, j))
                game.board[next_cell[0]][next_cell[1]] = last[0]
                game.relative_score = last[1]

    return best_score, best_piece, best_move
