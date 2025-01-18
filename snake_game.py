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

# Directions as tuples for easy direction changes
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Game settings, target score to win
TARGET_SCORE = 10

# Initialize the screen with specified width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Two-Player Snake Game")  # Set the window title

# Clock to control the frame rate of the game
clock = pygame.time.Clock()

# Class to represent a Snake
class Snake:
    def __init__(self, color, start_pos):
        self.color = color  # Color of the snake
        self.body = [start_pos]  # Initial position of the snake's body
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])  # Random initial direction
        self.score = 0  # Initial score

    # Method to move the snake
    def move(self):
        head_x, head_y = self.body[0]  # Current head position
        dir_x, dir_y = self.direction  # Current direction
        new_head = (head_x + dir_x * CELL_SIZE, head_y + dir_y * CELL_SIZE)  # Calculate new head position
        self.body = [new_head] + self.body[:-1]  # Update the snake's body

    # Method to grow the snake
    def grow(self):
        tail = self.body[-1]  # Get the current tail position
        self.body.append(tail)  # Append a new segment to the tail

    # Method to change the snake's direction
    def change_direction(self, new_direction):
        # Ensure the new direction is not directly opposite to the current direction
        if (self.direction[0] * new_direction[0] == 0 and
            self.direction[1] * new_direction[1] == 0):
            self.direction = new_direction  # Update the direction

    # Method to draw the snake on the screen
    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, (*segment, CELL_SIZE, CELL_SIZE))  # Draw each segment

# Function to place an apple on the screen
def place_apple(snake1, snake2):
    while True:
        # Generate random apple position
        x = random.randint(0, (WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        y = random.randint(0, (HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        apple_pos = (x, y)
        # Ensure the apple is not placed on either snake
        if apple_pos not in snake1.body and apple_pos not in snake2.body:
            return apple_pos  # Return the valid apple position

# Main function to run the game
def main():
    snake1 = Snake(BLUE, (WIDTH // 4, HEIGHT // 2))  # Initialize Player 1's snake
    snake2 = Snake(GREEN, (3 * WIDTH // 4, HEIGHT // 2))  # Initialize Player 2's snake
    apple = place_apple(snake1, snake2)  # Place the first apple

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()  # Quit the game
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                # Change direction based on key press for Player 1
                if event.key == pygame.K_w:
                    snake1.change_direction(UP)
                elif event.key == pygame.K_s:
                    snake1.change_direction(DOWN)
                elif event.key == pygame.K_a:
                    snake1.change_direction(LEFT)
                elif event.key == pygame.K_d:
                    snake1.change_direction(RIGHT)
                # Change direction based on key press for Player 2
                elif event.key == pygame.K_UP:
                    snake2.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake2.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake2.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake2.change_direction(RIGHT)

        snake1.move()  # Move Player 1's snake
        snake2.move()  # Move Player 2's snake

        # Check if Player 1's snake eats the apple
        if snake1.body[0] == apple:
            snake1.grow()  # Grow the snake
            snake1.score += 1  # Increase the score
            apple = place_apple(snake1, snake2)  # Place a new apple

        # Check if Player 2's snake eats the apple
        if snake2.body[0] == apple:
            snake2.grow()  # Grow the snake
            snake2.score += 1  # Increase the score
            apple = place_apple(snake1, snake2)  # Place a new apple

        # Check for collisions with walls or the snake's own body
        for snake in [snake1, snake2]:
            head = snake.body[0]
            if (head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[1] >= HEIGHT or
                head in snake.body[1:]):
                running = False  # End the game if collision is detected

        screen.fill(BLACK)  # Clear the screen
        snake1.draw(screen)  # Draw Player 1's snake
        snake2.draw(screen)  # Draw Player 2's snake
        pygame.draw.rect(screen, RED, (*apple, CELL_SIZE, CELL_SIZE))  # Draw the apple

        # Display scores
        font = pygame.font.Font(None, 36)
        score_text1 = font.render(f"Player 1 Score: {snake1.score}", True, WHITE)
        score_text2 = font.render(f"Player 2 Score: {snake2.score}", True, WHITE)
        screen.blit(score_text1, (10, 10))
        screen.blit(score_text2, (WIDTH - score_text2.get_width() - 10, 10))

        pygame.display.flip()  # Update the display
        clock.tick(10)  # Control the frame rate

        # Check if any player has reached the target score
        if snake1.score >= TARGET_SCORE or snake2.score >= TARGET_SCORE:
            running = False  # End the game if target score is reached

    # Determine the winner and print the result
    winner = "Player 1" if snake1.score >= TARGET_SCORE else "Player 2"
    print(f"{winner} wins!")

if __name__ == "__main__":
    main()  # Start the game
