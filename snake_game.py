import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
CELL_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game settings
TARGET_SCORE = 10

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Snake Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()

class Snake:
    def __init__(self, color, start_pos):
        self.color = color
        self.body = [start_pos]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.score = 0

    def move(self):
        head_x, head_y = self.body[0]
        dir_x, dir_y = self.direction
        new_head = (head_x + dir_x * CELL_SIZE, head_y + dir_y * CELL_SIZE)
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        tail = self.body[-1]
        self.body.append(tail)

    def change_direction(self, new_direction):
        if (self.direction[0] * new_direction[0] == 0 and
            self.direction[1] * new_direction[1] == 0):
            self.direction = new_direction

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (*segment, CELL_SIZE, CELL_SIZE))

def place_apple(snake1, snake2):
    while True:
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        apple_pos = (x, y)
        if apple_pos not in snake1.body and apple_pos not in snake2.body:
            return apple_pos

def main():
    snake1 = Snake(BLUE, (WIDTH // 4, HEIGHT // 2))
    snake2 = Snake(GREEN, (3 * WIDTH // 4, HEIGHT // 2))
    apple = place_apple(snake1, snake2)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    snake1.change_direction(UP)
                elif event.key == pygame.K_s:
                    snake1.change_direction(DOWN)
                elif event.key == pygame.K_a:
                    snake1.change_direction(LEFT)
                elif event.key == pygame.K_d:
                    snake1.change_direction(RIGHT)
                elif event.key == pygame.K_UP:
                    snake2.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake2.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake2.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake2.change_direction(RIGHT)

        snake1.move()
        snake2.move()

        if snake1.body[0] == apple:
            snake1.grow()
            snake1.score += 1
            apple = place_apple(snake1, snake2)

        if snake2.body[0] == apple:
            snake2.grow()
            snake2.score += 1
            apple = place_apple(snake1, snake2)

        # Check for collisions
        for snake in [snake1, snake2]:
            head = snake.body[0]
            if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or
                head in snake.body[1:]):
                running = False

        screen.fill(BLACK)
        snake1.draw(screen)
        snake2.draw(screen)
        pygame.draw.rect(screen, RED, (*apple, CELL_SIZE, CELL_SIZE))

        # Display scores
        font = pygame.font.Font(None, 36)
        score_text1 = font.render(f"Player 1 Score: {snake1.score}", True, WHITE)
        score_text2 = font.render(f"Player 2 Score: {snake2.score}", True, WHITE)
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (WIDTH - score_text2.get_width() - 10, 10))

        pygame.display.flip()
        clock.tick(10)

        if snake1.score >= TARGET_SCORE or snake2.score >= TARGET_SCORE:
            running = False

    winner = "Player 1" if snake1.score >= TARGET_SCORE else "Player 2"
    print(f"{winner} wins!")

if __name__ == "__main__":
    main()
