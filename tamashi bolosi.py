import pygame
import random
pygame.init()

# Screen dimensions
width, height = 400, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Tetris Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Block properties
block_size = 20
cols, rows = width // block_size, height // block_size

# Game variables
board = [[BLACK for _ in range(cols)] for _ in range(rows)]
shapes = [
    [(0, 0), (1, 0), (0, 1), (1, 1)],  # Square
    [(0, 0), (1, 0), (2, 0), (3, 0)],  # Line
    [(0, 1), (1, 1), (2, 1), (1, 0)],  # T-shape
    [(0, 1), (1, 1), (1, 0), (2, 0)],  # Z-shape
    [(0, 0), (1, 0), (1, 1), (2, 1)]  # S-shape
]

# Initial game state
current_shape = random.choice(shapes)
current_color = random.choice([RED, BLUE, GREEN])
current_pos = [cols // 2, 0]
clock = pygame.time.Clock()
speed = 5  # Falling speed in blocks per second
score = 0


def draw_board():
    screen.fill(BLACK)
    for y in range(rows):
        for x in range(cols):
            pygame.draw.rect(screen, board[y][x], (x * block_size, y * block_size, block_size, block_size))

    for block in current_shape:
        bx, by = block[0] + current_pos[0], block[1] + current_pos[1]
        pygame.draw.rect(screen, current_color, (bx * block_size, by * block_size, block_size, block_size))

    font = pygame.font.SysFont(None, 32)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))


def valid_move(offset):
    for block in current_shape:
        bx, by = block[0] + current_pos[0] + offset[0], block[1] + current_pos[1] + offset[1]
        if bx < 0 or bx >= cols or by >= rows or (by >= 0 and board[by][bx] != BLACK):
            return False
    return True


def lock_shape():
    global current_shape, current_color, current_pos, score, speed
    for block in current_shape:
        bx, by = block[0] + current_pos[0], block[1] + current_pos[1]
        if by >= 0:
            board[by][bx] = current_color

    clear_rows()
    current_shape = random.choice(shapes)
    current_color = random.choice([RED, BLUE, GREEN])
    current_pos = [cols // 2, 0]

    if not valid_move((0, 0)):
        return False  # Game Over

    return True


def clear_rows():
    global score, speed
    cleared = 0
    for y in range(rows):
        if all(block != BLACK for block in board[y]):
            del board[y]
            board.insert(0, [BLACK for _ in range(cols)])
            cleared += 1

    score += cleared * 10
    if cleared > 0:
        speed += 0.5  # Increase speed as rows are cleared


def rotate_shape():
    global current_shape
    rotated = [(-block[1], block[0]) for block in current_shape]
    if valid_move((0, 0)):
        current_shape = rotated


def display_game_over():
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 72)
    game_over_text = font.render("Game Over!", True, RED)
    text_rect = game_over_text.get_rect(center=(width // 2, height // 2))
    screen.blit(game_over_text, text_rect)
    pygame.display.flip()
    pygame.time.wait(3000)  # Wait for 3 seconds before quitting


# Game loop
running = True
fall_time = 0
while running:
    dt = clock.tick(60) / 1000.0  # Amount of time passed in seconds
    fall_time += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and valid_move((-1, 0)):
                current_pos[0] -= 1
            if event.key == pygame.K_RIGHT and valid_move((1, 0)):
                current_pos[0] += 1
            if event.key == pygame.K_DOWN and valid_move((0, 1)):
                current_pos[1] += 1
            if event.key == pygame.K_UP:
                rotate_shape()

    if fall_time >= 1 / speed:
        fall_time = 0
        if valid_move((0, 1)):
            current_pos[1] += 1
        else:
            if not lock_shape():
                display_game_over()
                running = False

    draw_board()
    pygame.display.flip()

pygame.quit()
