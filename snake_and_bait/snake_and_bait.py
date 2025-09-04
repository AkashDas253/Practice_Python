import pygame
import random
import sys

# Game settings
WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
GRID_WIDTH = WIDTH // CELL_SIZE
GRID_HEIGHT = HEIGHT // CELL_SIZE
FPS = 10

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


def draw_grid(surface):
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(surface, WHITE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(surface, WHITE, (0, y), (WIDTH, y))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Snake and Bait (Pygame)')
    clock = pygame.time.Clock()

    snake = [(GRID_HEIGHT // 2, GRID_WIDTH // 2)]
    direction = (0, 1)
    bait = (random.randint(0, GRID_HEIGHT - 1), random.randint(0, GRID_WIDTH - 1))
    score = 0

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != (1, 0):
                    direction = (-1, 0)
                elif event.key == pygame.K_DOWN and direction != (-1, 0):
                    direction = (1, 0)
                elif event.key == pygame.K_LEFT and direction != (0, 1):
                    direction = (0, -1)
                elif event.key == pygame.K_RIGHT and direction != (0, -1):
                    direction = (0, 1)
                elif event.key == pygame.K_q:
                    running = False

        # Move snake
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
        # Check collision
        if (
            new_head[0] < 0 or new_head[0] >= GRID_HEIGHT or
            new_head[1] < 0 or new_head[1] >= GRID_WIDTH or
            new_head in snake
        ):
            running = False
            continue
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

        # Draw everything
        screen.fill(BLACK)
        draw_grid(screen)
        # Draw bait
        bait_rect = pygame.Rect(bait[1] * CELL_SIZE, bait[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, RED, bait_rect)
        # Draw snake
        for y, x in snake:
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, GREEN, rect)
        # Draw score
        font = pygame.font.SysFont(None, 36)
        score_surf = font.render(f'Score: {score}', True, WHITE)
        screen.blit(score_surf, (10, 10))
        pygame.display.flip()

    # Game over
    font = pygame.font.SysFont(None, 48)
    text = font.render('GAME OVER!', True, RED)
    screen.blit(text, (WIDTH // 2 - 120, HEIGHT // 2 - 24))
    pygame.display.flip()
    pygame.time.wait(2000)
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
