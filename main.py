import pygame
import chess_engine
import chess_ai as ai
import random
import os
import time

pygame.init()
game = chess_engine.ChessGame()
ai.set_board(game.get_board(), game)

# CONSTANTS

HEIGHT = 650
WIDTH = 800
CELL_SIZE = min(WIDTH, HEIGHT) / 10
X_OFFSET = (WIDTH - 8 * CELL_SIZE) / 6
Y_OFFSET = (HEIGHT - 8 * CELL_SIZE) / 2
FPS = 60
RUNNING = True
TEXT_COLOR = (10, 200, 150)
BACKGROUND_COLOR = (100, 100, 100)
FONT = pygame.font.Font("./fonts/RobotoMono-Bold.ttf", 20)

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
ai_situation = "bored"

# Loading Piece images

piece_names = ["PAWN_W", "PAWN_B", "ROOK_B", "ROOK_W", "BISHOP_W", "BISHOP_B", "KNIGHT_B", "KNIGHT_W", "KING_W", "KING_B", "QUEEN_B", "QUEEN_W"]
piece_images = {}

# Game related variables

can_move = [[False for j in range(0, 8)] for i in range(0, 8)]
can_attack = [[False for j in range(0, 8)] for i in range(0, 8)]
selected_piece_pos = (-1, -1)

for name in piece_names:
	piece_images[name] = pygame.transform.scale(pygame.image.load(os.path.join("images/"+name+".png")), (CELL_SIZE, CELL_SIZE))
	
# Functions

def use_ai():
	global ai_situation
	ai_situation = "thinking"
	update_window()
	ai.cnt = 0
	last_time = time.time()
	ai_situation = "bored"
	score, from_cell, to_cell = ai.minimax(4, -ai.INF, ai.INF, False)
	if(game.is_empty(to_cell[0], to_cell[1])):
		game.move_piece(from_cell, to_cell)
	else:
		game.attack_piece(from_cell, to_cell)
	print("")
	print("")
	print("checked positions count: ", ai.cnt)
	print("from_cell, to_cell", from_cell, to_cell)
	print("relative_score: ", game.relative_score)
	print("time:", round(time.time() - last_time, 2), "(s)")
	


def clear_highlightes():
	for i in range(0, 8):
		for j in range(0, 8):
			can_move[i][j] = False
			can_attack[i][j] = False

def handle_event(event):
	global selected_piece_pos
	global RUNNING
	
	if(event.type == pygame.QUIT):
		RUNNING = False
	
	if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE :
		use_ai()

	if(event.type == pygame.MOUSEBUTTONDOWN):
		row = int((event.pos[1] - Y_OFFSET)/CELL_SIZE)
		column = int((event.pos[0] - X_OFFSET)/CELL_SIZE)
		if not game.valid_pos(row, column):
			return
		
		if not game.is_empty(row, column) and not can_attack[row][column] and game.board[row][column][1] == game.get_turn():
			if(selected_piece_pos != (row, column)):
				clear_highlightes()
			selected_piece_pos = (row, column)
			for cell in game.get_moves(row, column):
				can_move[cell[0]][cell[1]] = True
			for cell in game.get_attacks(row, column):
				can_attack[cell[0]][cell[1]] = True
		
		elif can_move[row][column]:
			clear_highlightes()
			game.move_piece(selected_piece_pos, (row, column))
			use_ai()
		
		elif can_attack[row][column]:
			clear_highlightes()
			game.attack_piece(selected_piece_pos, (row, column))
			use_ai()

		else:
			clear_highlightes()

def update_window():
	global FONT
	global ai_situation

	# Backgroud color
	window.fill(BACKGROUND_COLOR)

	# Texts

	texts = [FONT.render("score: " + str(game.relative_score), True, TEXT_COLOR, BACKGROUND_COLOR),
		  	FONT.render("AI : " + str(ai_situation), True, TEXT_COLOR, BACKGROUND_COLOR),]
	textRect = [texts[i].get_rect() for i in range(0, len(texts))]
	for i in range(0, len(texts)):
		textRect[i].center = (31*WIDTH/36, HEIGHT/5 + i * 25)
	for i in range(0, len(texts)):
		window.blit(texts[i], textRect[i])

	# Board
	for i in range(0, 8):
		for j in range(0, 8):
			color = (0, 0, 230) if ( i + j ) % 2 == 0 else (255, 255, 255)
			if can_move[i][j]:
				color = (color[0]/2, color[1]/2 + 120, color[2]/5)
			if can_attack[i][j]:
				color = (255, 0, 0)
			x = X_OFFSET + j * CELL_SIZE
			y = Y_OFFSET + i * CELL_SIZE
			pygame.draw.rect(window, color , pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 0)
			if not game.is_empty(i, j):
				window.blit(piece_images[game.get_piece_name(i, j)], (x, y))
			

	pygame.display.update()

def main():
	update_window()
	while(RUNNING):
			clock.tick(60)
			update_window()
			for event in pygame.event.get() :
				handle_event(event)
	pygame.quit()

if __name__ == "__main__":
	main()
				