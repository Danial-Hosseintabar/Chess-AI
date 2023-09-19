from enum import Enum

board = []

class Piece(Enum):
    EMPTY = -1
    PAWN = 0
    KING = 1
    QUEEN = 2
    BISHOP = 3
    ROOK = 4
    KNIGHT = 5

class Player(Enum):
    WHITE = 0
    BLACK = 1

# empty : -1
# pawn : 0
# king : 1
# queen : 2
# bishop : 3
# rook : 4
# knight : 5

for i in range(0, 8):
    board.append([])

for row_number in range(2, 6):
    for j in range(0, 8):
        board[row_number].append(-1)

for row_number in [1, 6]:
    for j in range(0, 8):
        board[row_number].append(0)

board[0] = [(Piece.ROOK, Player.BLACK),
            (Piece.KNIGHT, Player.BLACK),
            (Piece.BISHOP, Player.BLACK),
            (Piece.KING, Player.BLACK),
            (Piece.QUEEN, Player.BLACK),
            (Piece.BISHOP, Player.BLACK),
            (Piece.KNIGHT, Player.BLACK),
            (Piece.ROOK, Player.BLACK)]

board[7] = [(Piece.ROOK, Player.WHITE),
            (Piece.KNIGHT, Player.WHITE),
            (Piece.BISHOP, Player.WHITE),
            (Piece.KING, Player.WHITE),
            (Piece.QUEEN, Player.WHITE),
            (Piece.BISHOP, Player.WHITE),
            (Piece.KNIGHT, Player.WHITE),
            (Piece.ROOK, Player.WHITE)]
