from enum import Enum

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

INF = 1000000

piece_score = {"KING": 0, "PAWN": 1, "QUEEN": 9, "KNIGHT": 3, "BISHOP": 3, "ROOK": 5}

class ChessGame:
    def __init__(self):
            
        self.board = []
        self.turn = 0
        self.is_checked = False

        # Initial settings on board

        self.relative_score = 0

        for i in range(0, 8):
            self.board.append([])

        for row_number in range(2, 6):
            for j in range(0, 8):
                self.board[row_number].append((Piece.EMPTY, -1))

        for row_number in [1, 6]:
            for j in range(0, 8):
                self.board[row_number].append((Piece.PAWN, Player.BLACK if row_number == 1 else Player.WHITE ))

        self.board[0] = [(Piece.ROOK, Player.BLACK),
                    (Piece.KNIGHT, Player.BLACK),
                    (Piece.BISHOP, Player.BLACK),
                    (Piece.KING, Player.BLACK),
                    (Piece.QUEEN, Player.BLACK),
                    (Piece.BISHOP, Player.BLACK),
                    (Piece.KNIGHT, Player.BLACK),
                    (Piece.ROOK, Player.BLACK)]

        self.board[7] = [(Piece.ROOK, Player.WHITE),
                    (Piece.KNIGHT, Player.WHITE),
                    (Piece.BISHOP, Player.WHITE),
                    (Piece.KING, Player.WHITE),
                    (Piece.QUEEN, Player.WHITE),
                    (Piece.BISHOP, Player.WHITE),
                    (Piece.KNIGHT, Player.WHITE),
                    (Piece.ROOK, Player.WHITE)]

        self.wking_pos = (7, 3)
        self.bking_pos = (0, 3)

    # Functions

    def set_board(self, new_board):
        self.board = new_board

    def get_turn(self):
        return Player.WHITE if self.turn % 2 == 0 else Player.BLACK

    def change_turn(self):
        self.turn += 1

    def is_empty(self, row, column):
        return self.board[row][column][0] == Piece.EMPTY

    def get_piece_name(self, row, column):
        return self.board[row][column][0].name + "_" + ( "W" if self.board[row][column][1] == Player.WHITE else "B")

    def get_board(self):
        return self.board

    def valid_pos(self, row, column):
        return 0 <= row and row < 8 and column < 8 and column >= 0


    def update_is_check(self):
        
        opposite_side = Player.WHITE if self.turn % 2 == 1 else Player.BLACK
        our_side = Player.WHITE if self.turn % 2 == 0 else Player.BLACK
        
        # checking for horizontal/vertical checks by queens or rooks
        
        king_row, king_column = self.wking_pos if self.turn % 2 == 0 else self.bking_pos
        
        for delta_r, delta_c in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            row, column = king_row, king_column
            while(self.valid_pos(row + delta_r, column + delta_c)):
                if self.board[row + delta_r][column + delta_c][0] != Piece.EMPTY :
                    if self.board[row + delta_r][column + delta_c][1] == opposite_side and self.board[row + delta_r][column + delta_c][0] in [Piece.ROOK, Piece.QUEEN]:
                        print("CHECK!")
                        self.is_checked = True
                        return True
                    break
                row += delta_r
                column += delta_c
        
        # checking for diagonal checks from bishops or queens

        for delta_r, delta_c in [(-1, 1), (1, -1), (-1, -1), (1, 1)]:
            row, column = king_row, king_column
            while(self.valid_pos(row + delta_r, column + delta_c)):
                if self.board[row + delta_r][column + delta_c][0] != Piece.EMPTY :
                    if self.board[row + delta_r][column + delta_c][1] == opposite_side and self.board[row + delta_r][column + delta_c][0] in [Piece.BISHOP, Piece.QUEEN]:
                        print(str(our_side) + " IS CHECKED!")
                        self.is_checked = True
                        return True
                    break
                row += delta_r
                column += delta_c

        print("NO CHECK FOUND")
        self.is_checked = False
        return False


    def get_rook_moves(self, row, column, max_distance):
        moves = []
        attacks = []

        for each in [[0, 1], [1, 0], [-1, 0], [0, -1]]:
            row_increment = each[0]
            column_increment = each[1]
            row_delta = row_increment
            column_delta = column_increment
            while(max(abs(row_delta), abs(column_delta)) <= max_distance and self.valid_pos(row + row_delta, column + column_delta) and self.board[row + row_delta][column + column_delta][0] == Piece.EMPTY):
                moves.append((row + row_delta, column + column_delta))
                row_delta += row_increment
                column_delta += column_increment

            if(self.valid_pos(row + row_delta, column + column_delta) and max(abs(row_delta), abs(column_delta)) <= max_distance):
                if(self.board[row + row_delta][column + column_delta][1] != self.board[row][column][1]):
                    attacks.append((row + row_delta, column + column_delta))

        return moves, attacks

    def get_bishop_moves(self, row, column, max_distance):
        moves = []
        attacks = []
        
        for row_increment in [-1, +1]:
            for column_increment in [-1, +1]:
                row_delta = row_increment
                column_delta = column_increment
                while(abs(row_delta) <= max_distance and self.valid_pos(row + row_delta, column + column_delta) and self.board[row + row_delta][column + column_delta][0] == Piece.EMPTY):
                    moves.append((row + row_delta, column + column_delta))
                    row_delta += row_increment
                    column_delta += column_increment

                if(self.valid_pos(row + row_delta, column + column_delta) and abs(row_delta) <= max_distance):
                    if(self.board[row + row_delta][column + column_delta][1] != self.board[row][column][1]):
                        attacks.append((row + row_delta, column + column_delta))

        return moves, attacks

    def get_knight_moves(self, row, column):
        moves = []
        attacks = []

        for i in [1, -1]:
            for j in [2, -2]:
                if not self.valid_pos(row + i, column + j):
                    continue
                if self.board[row + i][column + j][0] == Piece.EMPTY:
                    moves.append((row + i, column + j))
                elif self.board[row + i][column + j][1] != self.board[row][column][1]:
                    attacks.append((row + i, column + j))
        
        for i in [1, -1]:
            for j in [2, -2]:
                if not self.valid_pos(row + j, column + i):
                    continue
                if self.board[row + j][column + i][0] == Piece.EMPTY:
                    moves.append((row + j, column + i))
                elif self.board[row + j][column + i][1] != self.board[row][column][1]:
                    attacks.append((row + j, column + i))
        
        return moves, attacks

    def get_moves(self, row, column):
        ret = []

        # PAWN

        if(self.board[row][column][0] == Piece.PAWN):
            next_row = row + 1 if self.board[row][column][1] == Player.BLACK else row - 1
            next_next_row = row + 2 if self.board[row][column][1] == Player.BLACK else row - 2
            is_first_move = (self.board[row][column][1] == Player.WHITE and row == 6) or (row == 1 and self.board[row][column][1] == Player.BLACK)
            
            if self.valid_pos(next_row, column) and self.board[next_row][column][0] == Piece.EMPTY:
                ret.append((next_row, column))
            else:
                return ret

            if not self.valid_pos(next_next_row, column):
                return ret
            elif self.board[next_next_row][column][0] == Piece.EMPTY and is_first_move :
                ret.append((next_next_row, column))


        # ROOK

        if(self.board[row][column][0] == Piece.ROOK):
            for cell in self.get_rook_moves(row, column, INF)[0]:
                ret.append(cell)
        
        # BISHOP

        if(self.board[row][column][0] == Piece.BISHOP):
            for cell in self.get_bishop_moves(row, column, INF)[0]:
                ret.append(cell)

        # QUEEN

        if(self.board[row][column][0] == Piece.QUEEN):
            for cell in self.get_bishop_moves(row, column, INF)[0]:
                ret.append(cell)
            
            for cell in self.get_rook_moves(row, column, INF)[0]:
                ret.append(cell)
        
        # KNIGHT

        if(self.board[row][column][0] == Piece.KNIGHT):
            for cell in self.get_knight_moves(row, column)[0]:
                ret.append(cell)

        # KING

        if(self.board[row][column][0] == Piece.KING):
            for cell in self.get_bishop_moves(row, column, 1)[0]:
                ret.append(cell)
            
            for cell in self.get_rook_moves(row, column, 1)[0]:
                ret.append(cell)
            
        return ret

    def move_piece(self, last_pos, new_pos):
        self.board[new_pos[0]][new_pos[1]] = self.board[last_pos[0]][last_pos[1]]
        self.board[last_pos[0]][last_pos[1]] = (Piece.EMPTY, -1)
        self.change_turn()
        self.update_is_check()

    def get_attacks(self, row, column):
        ret = []
        # PAWN
        if(self.board[row][column][0] == Piece.PAWN):
            # regular attack
            for i in [-1, 1]:
                x = row + (1 if self.board[row][column][1] == Player.BLACK else -1)
                y = column + i
                if self.valid_pos(x, y) and self.board[x][y][1] != self.board[row][column][1] and self.board[x][y][0] != Piece.EMPTY:
                    ret.append((x, y))
        
        # ROOK
        if(self.board[row][column][0] == Piece.ROOK):
            for each in self.get_rook_moves(row, column, INF)[1]:
                ret.append(each)
        
        # BISHOP
        if(self.board[row][column][0] == Piece.BISHOP):
            for each in self.get_bishop_moves(row, column, INF)[1]:
                ret.append(each)

        # KNIGHT
        if(self.board[row][column][0] == Piece.KNIGHT):
            for each in self.get_knight_moves(row, column)[1]:
                ret.append(each)

        # QUEEN
        if(self.board[row][column][0] == Piece.QUEEN):
            for each in self.get_bishop_moves(row, column, INF)[1]:
                ret.append(each)
            for each in self.get_rook_moves(row, column, INF)[1]:
                ret.append(each)
        
        # KING
        if(self.board[row][column][0] == Piece.KING):
            for each in self.get_bishop_moves(row, column, 1)[1]:
                ret.append(each)
            for each in self.get_rook_moves(row, column, 1)[1]:
                ret.append(each)
            
        return ret

    def attack_piece(self, first, second):
        lost_score = piece_score[self.board[second[0]][second[1]][0].name]
        if self.board[second[0]][second[1]][1] == Player.BLACK:
            self.relative_score += lost_score
        else:
            self.relative_score -= lost_score
        self.move_piece(first, second)

    # TODO: en passant
    # TODO: castle
    # TODO: check mate