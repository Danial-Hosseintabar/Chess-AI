import pygame

pygame.init()

HEIGHT = 650
WIDTH = 800
CELL_SIZE = min(WIDTH, HEIGHT)/10
X_OFFSET = (WIDTH-8*CELL_SIZE)/2
Y_OFFSET = (HEIGHT-8*CELL_SIZE)/2
window = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
FPS = 60
RUNNING = True

window.fill((255, 255, 0))

def handle_event(event):
	global RUNNING
	print(event.type)
	print(pygame.QUIT)
	if(event.type == pygame.QUIT):
		RUNNING = False
	if(event.type == pygame.MOUSEBUTTONUP):
		update_window()

def update_window():
	print("update")
	for i in range(0, 8):
		for j in range(0, 8):
			color = (0, 0, 0) if ( i + j ) % 2 == 0 else (255, 255, 255)
			pygame.draw.rect(window, color , pygame.Rect(X_OFFSET + i*CELL_SIZE, Y_OFFSET + j*CELL_SIZE, CELL_SIZE, CELL_SIZE), 0)
	pygame.display.update()

def main():

	while(RUNNING):
			clock.tick(60)
			for event in pygame.event.get() :
				handle_event(event)
	
	pygame.quit()


if __name__ == "__main__":
	main()
				