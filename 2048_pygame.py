import pygame
import random
import sys

# Initialize constants
WIDTH, HEIGHT = 400, 400
TILE_SIZE = 100
GRID_SIZE = 4
BACKGROUND_COLOR = (187, 173, 160)
TILE_COLORS = {
    0: (204, 192, 179),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}
FONT_COLOR = (119, 110, 101)
FONT = None
SCREEN = None

def initialize_board():
    board = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
    add_new_tile(board)
    add_new_tile(board)
    return board

def add_new_tile(board):
    empty_tiles = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if board[i][j] == 0]
    if empty_tiles:
        i, j = random.choice(empty_tiles)
        board[i][j] = 2 if random.random() < 0.9 else 4

def slide_row_left(row):
    new_row = [i for i in row if i != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    for i in range(GRID_SIZE - 1):
        if new_row[i] == new_row[i + 1] and new_row[i] != 0:
            new_row[i] *= 2
            new_row[i + 1] = 0
    new_row = [i for i in new_row if i != 0]
    new_row += [0] * (GRID_SIZE - len(new_row))
    return new_row

def move_left(board):
    return [slide_row_left(row) for row in board]

def rotate_board(board):
    return [list(row) for row in zip(*board[::-1])]

def move_right(board):
    rotated_board = rotate_board(rotate_board(board))
    moved_board = move_left(rotated_board)
    return rotate_board(rotate_board(moved_board))

def move_up(board):
    rotated_board = rotate_board(rotate_board(rotate_board(board)))
    moved_board = move_left(rotated_board)
    return rotate_board(moved_board)

def move_down(board):
    rotated_board = rotate_board(board)
    moved_board = move_left(rotated_board)
    return rotate_board(rotate_board(rotate_board(moved_board)))

def can_move(board):
    for row in board:
        if 0 in row:
            return True
    for row in board + rotate_board(board):
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1]:
                return True
    return False

def draw_board(board, score):
    SCREEN.fill(BACKGROUND_COLOR)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            value = board[i][j]
            color = TILE_COLORS.get(value, (60, 58, 50))
            pygame.draw.rect(SCREEN, color, (j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if value != 0:
                text = FONT.render(str(value), True, FONT_COLOR)
                text_rect = text.get_rect(center=(j * TILE_SIZE + TILE_SIZE / 2, i * TILE_SIZE + TILE_SIZE / 2))
                SCREEN.blit(text, text_rect)
    pygame.display.update()

def game_loop():
    board = initialize_board()
    score = 0
    running = True

    while running:
        draw_board(board, score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    new_board = move_left(board)
                elif event.key == pygame.K_RIGHT:
                    new_board = move_right(board)
                elif event.key == pygame.K_UP:
                    new_board = move_up(board)
                elif event.key == pygame.K_DOWN:
                    new_board = move_down(board)
                else:
                    continue

                if new_board != board:
                    board = new_board
                    add_new_tile(board)
                    score += sum(sum(row) for row in board)

                if not can_move(board):
                    draw_board(board, score)
                    pygame.time.wait(2000)
                    running = False
                    break

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pygame.init()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2048")
    FONT = pygame.font.SysFont("arial", 40)
    game_loop()
