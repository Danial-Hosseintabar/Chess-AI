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

piece_names = ["PAWN_W", "PAWN_B", "ROOK_B", "ROOK_W", "BISHOP_W", "BISHOP_B", "KNIGHT_B", "KNIGHT_W", "KING_W", "KING_B", "QUEEN_B", "QUEEN_W"]
piece_images = {}

for name in piece_names:
	piece_images[name] = pygame.transform.scale(pygame.image.load(os.path.join("images/"+name+".png")), (CELL_SIZE, CELL_SIZE))
	
# Functions

def handle_event(event):
	global RUNNING
	# print(event)
	if(event.type == pygame.QUIT):
		RUNNING = False
	if(event.type == pygame.MOUSEBUTTONUP):
		update_window()

def update_window():
	print("----UPDATE----")
	window.fill(BACKGROUND_COLOR)

	for i in range(0, 8):
		for j in range(0, 8):
			color = (0, 0, 230) if ( i + j ) % 2 == 0 else (255, 255, 255)
			x = X_OFFSET + j * CELL_SIZE
			y = Y_OFFSET + i * CELL_SIZE
			pygame.draw.rect(window, color , pygame.Rect(x, y, CELL_SIZE, CELL_SIZE), 0)
			if not is_empty(i, j):
				print("name : " + get_piece_name(i, j) + ", i , j " + str(i) + " " + str(j) )
				window.blit(piece_images[get_piece_name(i, j)], (x, y))
			

	pygame.display.update()

def main():
	update_window()
	while(RUNNING):
			clock.tick(60)
			for event in pygame.event.get() :
				handle_event(event)
	pygame.quit()


if __name__ == "__main__":
	main()
				