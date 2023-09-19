from enum import Enum

INF = 100

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
        board[row_number].append((Piece.PAWN, Player.BLACK if row_number == 1 else Player.WHITE ))

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


def valid_pos(row, column, max_distance):
    return 0 <= row and row < 8 and column < 8 and column >= 0

def get_rook_moves(row, column, max_distance):
    ret = []
    delta = 1
    while(delta <= max_distance and valid_pos(row + delta, column) and board[row+delta][column][0] == Piece.EMPTY):
        ret.append((row + delta, column))
        delta += 1

    delta = 1
    while(delta <= max_distance and valid_pos(row - delta, column) and board[row - delta][column][0] == Piece.EMPTY):
        ret.append((row - delta, column))
        delta += 1
    
    delta = 1
    while(delta <= max_distance and valid_pos(row, column + delta) and board[row][column + delta][0] == Piece.EMPTY):
        ret.append((row, column + delta))
        delta += 1
    
    delta = 1
    while(delta <= max_distance and valid_pos(row, column - delta) and board[row][column - delta][0] == Piece.EMPTY):
        ret.append((row, column - delta))
        delta += 1
    
    return ret

def get_bishop_moves(row, column, max_distance):
    ret = []

    delta = 1
    while(delta <= max_distance and valid_pos(row + delta, column + delta) and board[row + delta][column + delta][0] == Piece.EMPTY):
        ret.append((row + delta, column + delta))
        delta += 1

    delta = 1
    while(delta <= max_distance and valid_pos(row - delta, column - delta) and board[row - delta][column - delta][0] == Piece.EMPTY):
        ret.append((row - delta, column - delta))
        delta += 1

    delta = 1
    while(delta <= max_distance and valid_pos(row + delta, column - delta) and board[row + delta][column - delta][0] == Piece.EMPTY):
        ret.append((row + delta, column - delta))
        delta += 1

    delta = 1
    while(delta <= max_distance and valid_pos(row - delta, column + delta) and board[row - delta][column + delta][0] == Piece.EMPTY):
        ret.append((row - delta, column + delta))
        delta += 1

    return ret

def get_moves(row, column):
    ret = []

    # pawn

    if(board[row][column][0] == Piece.PAWN):
        next_row = row + 1 if board[row][column][1] == Player.BLACK else row - 1
        next_next_row = row + 2 if board[row][column][1] == Player.BLACK else row - 2
        
        if not valid_pos(next_row, column):
            return ret
        elif board[next_row][column][0] == Piece.EMPTY:
            ret.append((next_row, column))
        
        if not valid_pos(next_next_row, column):
            return ret
        elif board[next_next_row][column][0] == Piece.EMPTY:
            ret.append((next_next_row, column))

        return ret


    # rook

    if(board[row][column][0] == Piece.ROOK):
        for cell in get_rook_moves(row, column, INF):
            ret.append(cell)
        return ret
    
    # bishop

    if(board[row][column][0] == Piece.BISHOP):
        for cell in get_bishop_moves(row, column, INF):
            ret.append(cell)
        return ret

    # queen

    if(board[row][column][0] == Piece.QUEEN):
        for cell in get_bishop_moves(row, column, INF):
            ret.append(cell)
        
        for cell in get_rook_moves(row, column, INF):
            ret.append(cell)
        
        return ret
    
    # king

    if(board[row][column][0] == Piece.KING):
        for cell in get_bishop_moves(row, column, 1):
            ret.append(cell)
        
        for cell in get_rook_moves(row, column, 1):
            ret.append(cell)
        
        return ret

