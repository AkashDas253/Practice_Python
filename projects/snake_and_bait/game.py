import pygame
import random
import sys

# Game settings
GAME_WIDTH, GAME_HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = GAME_WIDTH // CELL_SIZE
GRID_HEIGHT = GAME_HEIGHT // CELL_SIZE
FPS = 10

MAIN_WIDTH, MAIN_HEIGHT = 700, 550  # Larger main window
GAME_X, GAME_Y = 50, 80  # Position of game area inside main window

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
BORDER_COLOR = (100, 100, 100)
BUTTON_COLOR = (70, 130, 180)
BUTTON_TEXT_COLOR = WHITE


def draw_grid(surface):
    for x in range(0, GAME_WIDTH, CELL_SIZE):
        pygame.draw.line(surface, WHITE, (GAME_X + x, GAME_Y), (GAME_X + x, GAME_Y + GAME_HEIGHT))
    for y in range(0, GAME_HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, WHITE, (GAME_X, GAME_Y + y), (GAME_X + GAME_WIDTH, GAME_Y + y))


def draw_buttons(surface, font, running, restart_rect, start_stop_rect):
    # Draw Restart button
    pygame.draw.rect(surface, BUTTON_COLOR, restart_rect)
    restart_text = font.render('Restart', True, BUTTON_TEXT_COLOR)
    surface.blit(restart_text, (restart_rect.x + 20, restart_rect.y + 10))
    # Draw Start/Stop button
    pygame.draw.rect(surface, BUTTON_COLOR, start_stop_rect)
    start_stop_text = font.render('Stop' if running else 'Start', True, BUTTON_TEXT_COLOR)
    surface.blit(start_stop_text, (start_stop_rect.x + 30, start_stop_rect.y + 10))


def main():
    pygame.init()
    screen = pygame.display.set_mode((MAIN_WIDTH, MAIN_HEIGHT))
    pygame.display.set_caption('Snake and Bait (Pygame)')
    clock = pygame.time.Clock()

    snake = [(GRID_HEIGHT // 2, GRID_WIDTH // 2)]
    direction = (0, 1)
    bait = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
    score = 0
    running = True
    paused = False
    game_over = False

    font = pygame.font.SysFont(None, 36)
    button_font = pygame.font.SysFont(None, 32)
    restart_rect = pygame.Rect(MAIN_WIDTH // 2 - 160, MAIN_HEIGHT - 65, 120, 40)
    start_stop_rect = pygame.Rect(MAIN_WIDTH // 2 + 40, MAIN_HEIGHT - 65, 120, 40)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if not paused and not game_over:
                    if event.key == pygame.K_UP and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_DOWN and direction != (-1, 0):
                        direction = (1, 0)
                    elif event.key == pygame.K_LEFT and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_RIGHT and direction != (0, -1):
                        direction = (0, 1)
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                if restart_rect.collidepoint(mx, my):
                    # Restart game
                    snake = [(GRID_HEIGHT // 2, GRID_WIDTH // 2)]
                    direction = (0, 1)
                    bait = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
                    score = 0
                    running = True
                    paused = False
                    game_over = False
                elif start_stop_rect.collidepoint(mx, my):
                    if not game_over:
                        paused = not paused
                        running = not paused

        if running and not paused and not game_over:
            clock.tick(FPS)
            # Move snake
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            # Check collision
            if (
                new_head[0] < 0 or new_head[0] >= GRID_HEIGHT or
                new_head[1] < 0 or new_head[1] >= GRID_WIDTH or
                new_head in snake
            ):
                game_over = True
                running = False
            else:
                snake.insert(0, new_head)
                # Check bait
                if new_head == bait:
                    score += 1
                    while True:
                        bait = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
                        if bait not in snake:
                            break
                else:
                    snake.pop()

        # Draw main window background
        screen.fill(GRAY)
        # Draw game area border
        pygame.draw.rect(screen, BORDER_COLOR, (GAME_X - 3, GAME_Y - 3, GAME_WIDTH + 6, GAME_HEIGHT + 6), 3)
        # Draw game area background
        pygame.draw.rect(screen, BLACK, (GAME_X, GAME_Y, GAME_WIDTH, GAME_HEIGHT))
        # Draw grid
        draw_grid(screen)
        # Draw bait
        bait_rect = pygame.Rect(GAME_X + bait[1] * CELL_SIZE, GAME_Y + bait[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, bait_rect)
        # Draw snake
        for y, x in snake:
            rect = pygame.Rect(GAME_X + x * CELL_SIZE, GAME_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
        # Draw score (top left, outside game area)
        score_surf = font.render(f'Score: {score}', True, BLACK)
        screen.blit(score_surf, (20, 20))
        # Draw buttons
        draw_buttons(screen, button_font, running, restart_rect, start_stop_rect)
        # Draw game over
        if game_over:
            over_font = pygame.font.SysFont(None, 48)
            text = over_font.render('GAME OVER!', True, RED)
            screen.blit(text, (MAIN_WIDTH // 2 - 120, MAIN_HEIGHT // 2 - 24))
        pygame.display.flip()

if __name__ == '__main__':
    main()
