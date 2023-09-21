import pygame
from chess_engine import *
import random
import os

pygame.init()

# CONSTANTS

HEIGHT = 650
WIDTH = 800
CELL_SIZE = min(WIDTH, HEIGHT) / 10
X_OFFSET = (WIDTH - 8 * CELL_SIZE) / 2
Y_OFFSET = (HEIGHT - 8 * CELL_SIZE) / 2
FPS = 60
RUNNING = True
BACKGROUND_COLOR = (40 + 195*random.randint(0, 1), 40 + 195*random.randint(0, 1), 40 + 195*random.randint(0, 1))

window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Loading Piece images

piece_names = ["PAWN_W", "PAWN_B", "ROOK_B", "ROOK_W", "BISHOP_W", "BISHOP_B", "KNIGHT_B", "KNIGHT_W", "KING_W", "KING_B", "QUEEN_B", "QUEEN_W"]
piece_images = {}

# Game related variables

highlighted = [[False for j in range(0, 8)] for i in range(0, 8)]
selected_piece_pos = (-1, -1)

for name in piece_names:
	piece_images[name] = pygame.transform.scale(pygame.image.load(os.path.join("images/"+name+".png")), (CELL_SIZE, CELL_SIZE))
	
# Functions

def clear_highlighted():
	for i in range(0, 8):
		for j in range(0, 8):
			highlighted[i][j] = False

def handle_event(event):
	global selected_piece_pos
	global RUNNING
	# print(event)
	if(event.type == pygame.QUIT):
		RUNNING = False
	if(event.type == pygame.MOUSEBUTTONDOWN):
		row = int((event.pos[1] - Y_OFFSET)/CELL_SIZE)
		column = int((event.pos[0] - X_OFFSET)/CELL_SIZE)
		if not is_empty(row, column):
			selected_piece_pos = (row, column)
			for cell in get_moves(row, column):
				highlighted[cell[0]][cell[1]] = True
		elif highlighted[row][column]:
			clear_highlighted()
			move_piece(selected_piece_pos, (row, column))
	

def update_window():
	# Backgroud color
	window.fill(BACKGROUND_COLOR)

	# Board
	for i in range(0, 8):
		for j in range(0, 8):
			color = (0, 0, 230) if ( i + j ) % 2 == 0 else (255, 255, 255)
			if(highlighted[i][j]):
				color = (color[0]/2, color[1]/2 + 120, color[2]/5)
			x = X_OFFSET + j * CELL_SIZE
			y = Y_OFFSET + i * CELL_SIZE
			pygame.draw.rect(window, color , pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 0)
			if not is_empty(i, j):
				window.blit(piece_images[get_piece_name(i, j)], (x, y))
			

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
				