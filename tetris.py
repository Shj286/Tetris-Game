import pygame
import random

# Initialize Pygame
pygame.init()
pygame.font.init()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Game dimensions
BLOCK_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
SCREEN_WIDTH = BLOCK_SIZE * GRID_WIDTH
SCREEN_HEIGHT = BLOCK_SIZE * GRID_HEIGHT + 50  # Extra 50 for score display

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]]
]

COLORS = [CYAN, YELLOW, MAGENTA, RED, GREEN, BLUE, ORANGE]

# Set up the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris")

clock = pygame.time.Clock()

def create_grid():
    return [[BLACK for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]

def draw_grid(grid):
    for i in range(GRID_HEIGHT):
        for j in range(GRID_WIDTH):
            pygame.draw.rect(screen, grid[i][j], (j * BLOCK_SIZE, i * BLOCK_SIZE + 50, BLOCK_SIZE, BLOCK_SIZE), 0)

def new_piece():
    shape = random.choice(SHAPES)
    color = random.choice(COLORS)
    return {
        'shape': shape,
        'color': color,
        'x': GRID_WIDTH // 2 - len(shape[0]) // 2,
        'y': 0
    }

def get_ghost_piece(grid, piece):
    ghost = piece.copy()
    while valid_move(grid, ghost, ghost['x'], ghost['y'] + 1):
        ghost['y'] += 1
    return ghost

def draw_piece(piece, alpha=255):
    for i, row in enumerate(piece['shape']):
        for j, cell in enumerate(row):
            if cell:
                color = list(piece['color'])
                color.append(alpha)
                pygame.draw.rect(screen, color,
                                 ((piece['x'] + j) * BLOCK_SIZE,
                                  (piece['y'] + i) * BLOCK_SIZE + 50,
                                  BLOCK_SIZE, BLOCK_SIZE), 0)

def valid_move(grid, piece, x, y):
    for i, row in enumerate(piece['shape']):
        for j, cell in enumerate(row):
            if cell:
                if (y + i >= GRID_HEIGHT or
                    x + j < 0 or
                    x + j >= GRID_WIDTH or
                    grid[y + i][x + j] != BLACK):
                    return False
    return True

def merge_piece(grid, piece):
    for i, row in enumerate(piece['shape']):
        for j, cell in enumerate(row):
            if cell:
                grid[piece['y'] + i][piece['x'] + j] = piece['color']

def remove_completed_rows(grid):
    full_rows = [i for i, row in enumerate(grid) if all(cell != BLACK for cell in row)]
    for row in full_rows:
        del grid[row]
        grid.insert(0, [BLACK for _ in range(GRID_WIDTH)])
    return len(full_rows)

def draw_score_and_level(score, level):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 120, 10))

def main():
    grid = create_grid()
    current_piece = new_piece()
    score = 0
    level = 1
    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if valid_move(grid, current_piece, current_piece['x'] - 1, current_piece['y']):
                        current_piece['x'] -= 1
                if event.key == pygame.K_RIGHT:
                    if valid_move(grid, current_piece, current_piece['x'] + 1, current_piece['y']):
                        current_piece['x'] += 1
                if event.key == pygame.K_DOWN:
                    if valid_move(grid, current_piece, current_piece['x'], current_piece['y'] + 1):
                        current_piece['y'] += 1
                if event.key == pygame.K_SPACE:
                    while valid_move(grid, current_piece, current_piece['x'], current_piece['y'] + 1):
                        current_piece['y'] += 1

        if valid_move(grid, current_piece, current_piece['x'], current_piece['y'] + 1):
            current_piece['y'] += 1
        else:
            merge_piece(grid, current_piece)
            rows_cleared = remove_completed_rows(grid)
            score += rows_cleared * 100
            level = (score // 1000) + 1  # Level increases every 1000 points
            current_piece = new_piece()
            if not valid_move(grid, current_piece, current_piece['x'], current_piece['y']):
                game_over = True

        screen.fill(BLACK)
        draw_grid(grid)
        
        ghost_piece = get_ghost_piece(grid, current_piece)
        if ghost_piece:
            draw_piece(ghost_piece, alpha=128)  # Semi-transparent ghost piece
        draw_piece(current_piece)  # Solid current piece

        draw_score_and_level(score, level)

        pygame.display.flip()
        clock.tick(5 + level)  # Increase speed based on level

    print(f"Game Over! Final Score: {score}, Level: {level}")
    pygame.quit()
    
if __name__ == "__main__":
    main()