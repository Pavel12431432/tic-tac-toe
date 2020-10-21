import pygame

col_count, row_count = 3, 3
how_many_to_connect = 3
TILE_SIZE = 128
WIDTH, HEIGHT = col_count * TILE_SIZE, row_count * TILE_SIZE
MAX_FPS = 144
font_color = (37, 37, 37)
font_size = 60


# pygame init
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic-tac-toe')
font = pygame.font.SysFont('impact', font_size)
clock = pygame.time.Clock()

# load images
imgs = [
	pygame.transform.scale(pygame.image.load('sprites/empty.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),
	pygame.transform.scale(pygame.image.load('sprites/cross.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),
	pygame.transform.scale(pygame.image.load('sprites/circle.png').convert_alpha(), (TILE_SIZE, TILE_SIZE)),
	pygame.transform.scale(pygame.image.load('sprites/selected.png').convert_alpha(), (TILE_SIZE, TILE_SIZE))
]


def inp():
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			quit()
		elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
			return pygame.mouse.get_pos()[0] // TILE_SIZE, pygame.mouse.get_pos()[1] // TILE_SIZE


def place_piece(col, row):
	try:
		if not board[col][row]:
			board[col][row] = turn
			return 1
		else:
			return 0
	except (IndexError, TypeError):
		return 0


def winning_move(piece):
	# Check horizontal locations for win
	for c in range(col_count - (how_many_to_connect - 1)):
		for r in range(row_count):
			if min([board[c + i][r] == piece for i in range(how_many_to_connect)]):
				return True

	# Check vertical locations for win
	for c in range(col_count):
		for r in range(row_count - (how_many_to_connect - 1)):
			if min([board[c][r + i] == piece for i in range(how_many_to_connect)]):
				return True

	# Check \ diagonals
	for c in range(col_count - (how_many_to_connect - 1)):
		for r in range(row_count - (how_many_to_connect - 1)):
			if min([board[c + i][r + i] == piece for i in range(how_many_to_connect)]):
				return True

	# check / diagonals
	for c in range(col_count - (how_many_to_connect - 1)):
		for r in range((how_many_to_connect - 1), row_count):
			if min([board[c + i][r - i] == piece for i in range(how_many_to_connect)]):
				return True


def end_game():
	draw()
	text = font.render('Player {} won!'.format(turn), True, font_color)
	text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 3))
	screen.blit(text, text_rect)
	pygame.display.update()
	while True:
		inp()


def draw():
	screen.fill((0, 0, 0))
	for col in range(len(board)):
		for piece in range(len(board[col])):
			p = board[col][piece]
			screen.blit(imgs[p], (col * TILE_SIZE, piece * TILE_SIZE))

	screen.blit(imgs[3], (
		pygame.mouse.get_pos()[0] // TILE_SIZE * TILE_SIZE, pygame.mouse.get_pos()[1] // TILE_SIZE * TILE_SIZE))
	pygame.display.update()


board = [[0 for col in range(row_count)] for piece in range(col_count)]
turn = 1

while True:
	draw()
	if (i := inp()) is not None and place_piece(*i):
		if winning_move(turn):
			print('end')
			end_game()
		turn = 2 if turn == 1 else 1
	clock.tick(MAX_FPS)