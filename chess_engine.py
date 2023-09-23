from enum import Enum

INF = 100

board = []
turn = 0

# Enums

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

# Initial settings on board

for i in range(0, 8):
    board.append([])

for row_number in range(2, 6):
    for j in range(0, 8):
        board[row_number].append((Piece.EMPTY, -1))

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

# Functions

def get_turn():
    return Player.WHITE if turn % 2 == 0 else Player.BLACK

def change_turn():
    global turn
    turn += 1

def is_empty(row, column):
    return board[row][column][0] == Piece.EMPTY

def get_piece_name(row, column):
    return board[row][column][0].name + "_" + ( "W" if board[row][column][1] == Player.WHITE else "B")

def get_board():
    return board

def valid_pos(row, column):
    return 0 <= row and row < 8 and column < 8 and column >= 0

def get_rook_moves(row, column, max_distance):
    moves = []
    attacks = []

    delta = 1
    while(delta <= max_distance and valid_pos(row + delta, column) and board[row+delta][column][0] == Piece.EMPTY):
        moves.append((row + delta, column))
        delta += 1
    
    if(delta <= max_distance and valid_pos(row + delta, column)):
        if(board[row+delta][column][1] != board[row][column][1]):
            attacks.append((row + delta, column))


    delta = 1
    while(delta <= max_distance and valid_pos(row - delta, column) and board[row - delta][column][0] == Piece.EMPTY):
        moves.append((row - delta, column))
        delta += 1
    
    if(delta <= max_distance and valid_pos(row - delta, column)):
        if(board[row-delta][column][1] != board[row][column][1]):
            attacks.append((row - delta, column))


    delta = 1
    while(delta <= max_distance and valid_pos(row, column + delta) and board[row][column + delta][0] == Piece.EMPTY):
        moves.append((row, column + delta))
        delta += 1
    
    if(delta <= max_distance and valid_pos(row, column+delta)):
        if(board[row][column+delta][1] != board[row][column][1]):
            attacks.append((row, column+delta))


    delta = 1
    while(delta <= max_distance and valid_pos(row, column - delta) and board[row][column - delta][0] == Piece.EMPTY):
        moves.append((row, column - delta))
        delta += 1
    
    if(delta <= max_distance and valid_pos(row, column-delta)):
        if(board[row][column-delta][1] != board[row][column][1]):
            attacks.append((row, column-delta))

    return moves, attacks

def get_bishop_moves(row, column, max_distance):
    moves = []
    attacks = []
    
    delta = 1
    while(delta <= max_distance and valid_pos(row + delta, column + delta) and board[row + delta][column + delta][0] == Piece.EMPTY):
        moves.append((row + delta, column + delta))
        delta += 1

    if(valid_pos(row + delta, column + delta) and delta <= max_distance):
        if(board[row + delta][column + delta][1] != board[row][column][1]):
            attacks.append((row + delta, column + delta))

    delta = 1
    while(delta <= max_distance and valid_pos(row - delta, column + delta) and board[row - delta][column + delta][0] == Piece.EMPTY):
        moves.append((row - delta, column + delta))
        delta += 1
    
    if(valid_pos(row - delta, column + delta) and delta <= max_distance):
        if(board[row - delta][column + delta][1] != board[row][column][1]):
            attacks.append((row - delta, column + delta))

    delta = 1
    while(delta <= max_distance and valid_pos(row + delta, column - delta) and board[row + delta][column - delta][0] == Piece.EMPTY):
        moves.append((row + delta, column - delta))
        delta += 1

    if(valid_pos(row + delta, column - delta) and delta <= max_distance):
        if(board[row + delta][column - delta][1] != board[row][column][1]):
            attacks.append((row + delta, column - delta))


    delta = 1
    while(delta <= max_distance and valid_pos(row - delta, column - delta) and board[row - delta][column - delta][0] == Piece.EMPTY):
        moves.append((row - delta, column - delta))
        delta += 1

    if(valid_pos(row - delta, column - delta) and delta <= max_distance):
        if(board[row - delta][column - delta][1] != board[row][column][1]):
            attacks.append((row - delta, column - delta))

    return moves, attacks

def get_knight_moves(row, column):
    moves = []
    attacks = []

    for i in [1, -1]:
        for j in [2, -2]:
            if not valid_pos(row + i, column + j):
                continue
            if board[row + i][column + j][0] == Piece.EMPTY:
                moves.append((row + i, column + j))
            elif board[row + i][column + j][1] != board[row][column][1]:
                attacks.append((row + i, column + j))
    
    for i in [1, -1]:
        for j in [2, -2]:
            if not valid_pos(row + j, column + i):
                continue
            if board[row + j][column + i][0] == Piece.EMPTY:
                moves.append((row + j, column + i))
            elif board[row + j][column + i][1] != board[row][column][1]:
                attacks.append((row + j, column + i))
    
    return moves, attacks

def get_moves(row, column):
    ret = []

    # PAWN

    if(board[row][column][0] == Piece.PAWN):
        next_row = row + 1 if board[row][column][1] == Player.BLACK else row - 1
        next_next_row = row + 2 if board[row][column][1] == Player.BLACK else row - 2
        is_first_move = (board[row][column][1] == Player.WHITE and row == 6) or (row == 1 and board[row][column][1] == Player.BLACK)
        
        if valid_pos(next_row, column) and board[next_row][column][0] == Piece.EMPTY:
            ret.append((next_row, column))
        else:
            return ret

        if not valid_pos(next_next_row, column):
            return ret
        elif board[next_next_row][column][0] == Piece.EMPTY and is_first_move :
            ret.append((next_next_row, column))


    # ROOK

    if(board[row][column][0] == Piece.ROOK):
        for cell in get_rook_moves(row, column, INF)[0]:
            ret.append(cell)
    
    # BISHOP

    if(board[row][column][0] == Piece.BISHOP):
        for cell in get_bishop_moves(row, column, INF)[0]:
            ret.append(cell)

    # QUEEN

    if(board[row][column][0] == Piece.QUEEN):
        for cell in get_bishop_moves(row, column, INF)[0]:
            ret.append(cell)
        
        for cell in get_rook_moves(row, column, INF)[0]:
            ret.append(cell)
    
    # KNIGHT

    if(board[row][column][0] == Piece.KNIGHT):
        for cell in get_knight_moves(row, column)[0]:
            ret.append(cell)

    # KING

    if(board[row][column][0] == Piece.KING):
        for cell in get_bishop_moves(row, column, 1)[0]:
            ret.append(cell)
        
        for cell in get_rook_moves(row, column, 1)[0]:
            ret.append(cell)
        
    return ret

def move_piece(last_pos, new_pos):
    board[new_pos[0]][new_pos[1]] = board[last_pos[0]][last_pos[1]]
    board[last_pos[0]][last_pos[1]] = (Piece.EMPTY, -1)
    change_turn()

def get_attacks(row, column):
    ret = []
    # PAWN
    if(board[row][column][0] == Piece.PAWN):
        # regular attack
        for i in [-1, 1]:
            x = row + (1 if board[row][column][1] == Player.BLACK else -1)
            y = column + i
            if valid_pos(x, y) and board[x][y][1] != board[row][column][1] and board[x][y][0] != Piece.EMPTY:
                ret.append((x, y))
    
    # ROOK
    if(board[row][column][0] == Piece.ROOK):
        for each in get_rook_moves(row, column, INF)[1]:
            ret.append(each)
    
    # BISHOP
    if(board[row][column][0] == Piece.BISHOP):
        for each in get_bishop_moves(row, column, INF)[1]:
            ret.append(each)

    # KNIGHT
    if(board[row][column][0] == Piece.KNIGHT):
        for each in get_knight_moves(row, column)[1]:
            ret.append(each)

    # QUEEN
    if(board[row][column][0] == Piece.QUEEN):
        for each in get_bishop_moves(row, column, INF)[1]:
            ret.append(each)
        for each in get_rook_moves(row, column, INF)[1]:
            ret.append(each)
    
    # KING
    if(board[row][column][0] == Piece.KING):
        for each in get_bishop_moves(row, column, 1)[1]:
            ret.append(each)
        for each in get_rook_moves(row, column, 1)[1]:
            ret.append(each)
        
    return ret

def attack_piece(first, second):
    move_piece(first, second)

# TODO: en passant
# TODO: castle