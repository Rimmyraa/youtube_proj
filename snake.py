import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game 🐍")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
RED = (200, 0, 0)

# Clock & speed
clock = pygame.time.Clock()
snake_block = 10
snake_speed = 10

# Fonts
font = pygame.font.SysFont(None, 35)

def show_score(score):
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, [10, 10])

def draw_snake(block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], block, block])

def game_over_screen(score):
    screen.fill(WHITE)
    text1 = font.render("Game Over!", True, RED)
    text2 = font.render(f"Final Score: {score}", True, BLACK)
    text3 = font.render("Press C to Play Again or Q to Quit", True, BLACK)

    screen.blit(text1, [WIDTH / 3, HEIGHT / 4])
    screen.blit(text2, [WIDTH / 3, HEIGHT / 3])
    screen.blit(text3, [WIDTH / 6, HEIGHT / 2])
    pygame.display.update()

def game_loop():
    game_over = False
    game_close = False

    x = WIDTH / 2
    y = HEIGHT / 2
    dx = 0
    dy = 0

    snake_list = []
    length = 1

    food_x = random.randrange(0, WIDTH - snake_block, snake_block)
    food_y = random.randrange(0, HEIGHT - snake_block, snake_block)

    score = 0

    while not game_over:

        while game_close:
            game_over_screen(score)

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c:
                        game_loop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dx = -snake_block
                    dy = 0
                elif event.key == pygame.K_RIGHT:
                    dx = snake_block
                    dy = 0
                elif event.key == pygame.K_UP:
                    dy = -snake_block
                    dx = 0
                elif event.key == pygame.K_DOWN:
                    dy = snake_block
                    dx = 0

        # Wall collision
        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT:
            game_close = True

        x += dx
        y += dy
        screen.fill(WHITE)
        pygame.draw.rect(screen, RED, [food_x, food_y, snake_block, snake_block])

        snake_head = [x, y]
        snake_list.append(snake_head)

        if len(snake_list) > length:
            del snake_list[0]

        # Self collision
        for block in snake_list[:-1]:
            if block == snake_head:
                game_close = True

        draw_snake(snake_block, snake_list)
        show_score(score)

        pygame.display.update()

        # Food collision
        if x == food_x and y == food_y:
            food_x = random.randrange(0, WIDTH - snake_block, snake_block)
            food_y = random.randrange(0, HEIGHT - snake_block, snake_block)
            length += 1
            score += 1

        clock.tick(snake_speed + score // 5)

    pygame.quit()

game_loop()
