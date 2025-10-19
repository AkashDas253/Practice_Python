import pygame
from tetris import (
    create_grid, convert_shape_format, valid_space, check_lost, get_shape, clear_rows, COLUMNS, ROWS, BLACK, Tetromino
)

# UI/game constants
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
FPS = 60


def draw_grid(surface, grid):
    for y in range(ROWS):
        for x in range(COLUMNS):
            pygame.draw.rect(surface, grid[y][x], (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
    # Draw grid lines
    for y in range(ROWS):
        pygame.draw.line(surface, GRAY, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))
    for x in range(COLUMNS):
        pygame.draw.line(surface, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    # Draw border
    pygame.draw.rect(surface, WHITE, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 4)


def draw_next_piece(surface, piece):
    font = pygame.font.SysFont('comicsans', 24, bold=True)
    label = font.render('Next:', 1, WHITE)
    sx = SCREEN_WIDTH + 20
    sy = 60
    surface.blit(label, (sx, sy - 30))
    shape = piece.shape
    for i, line in enumerate(shape):
        for j, column in enumerate(line):
            if column:
                pygame.draw.rect(surface, piece.color, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(surface, GRAY, (sx + j * BLOCK_SIZE, sy + i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_window(surface, grid, score=0, next_piece=None):
    surface.fill(BLACK)
    draw_grid(surface, grid)
    # Draw score
    font = pygame.font.SysFont('comicsans', 32, bold=True)
    label = font.render(f'Score: {score}', 1, WHITE)
    surface.blit(label, (10, 10))
    # Draw next piece preview
    if next_piece:
        draw_next_piece(surface, next_piece)


def show_game_over(surface, score):
    font = pygame.font.SysFont('comicsans', 48, bold=True)
    label = font.render('Game Over', 1, (255, 0, 0))
    surface.blit(label, (SCREEN_WIDTH // 2 - label.get_width() // 2, SCREEN_HEIGHT // 2 - 60))
    font2 = pygame.font.SysFont('comicsans', 32)
    label2 = font2.render(f'Final Score: {score}', 1, WHITE)
    surface.blit(label2, (SCREEN_WIDTH // 2 - label2.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.update()
    pygame.time.delay(2000)

def main():
    pygame.init()
    # Make room for next piece preview
    win = pygame.display.set_mode((SCREEN_WIDTH + 150, SCREEN_HEIGHT))
    pygame.display.set_caption('Tetris')
    clock = pygame.time.Clock()
    locked_positions = {}
    grid = create_grid(locked_positions)
    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    fall_time = 0
    fall_speed = 0.5
    score = 0
    game_over = False

    while run:
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime() / 1000
        clock.tick(FPS)

        if fall_time >= fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not valid_space(current_piece, grid) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()
                    if not valid_space(current_piece, grid):
                        for _ in range(3):
                            current_piece.rotate()
                elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    run = False

        shape_pos = convert_shape_format(current_piece)
        for x, y in shape_pos:
            if y > -1:
                grid[y][x] = current_piece.color

        if change_piece:
            for pos in shape_pos:
                p = (pos[0], pos[1])
                locked_positions[p] = current_piece.color
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += clear_rows(grid, locked_positions) * 10

        draw_window(win, grid, score, next_piece)
        pygame.display.update()

        if check_lost(locked_positions):
            show_game_over(win, score)
            run = False

    pygame.quit()


if __name__ == '__main__':
    main()
