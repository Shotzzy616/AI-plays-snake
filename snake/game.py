import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
window_width, window_height = 640, 480
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Snake Game')
fps = 10

# Set up colors
black = (0, 0, 0)
green = (0, 255, 0)
red = (255, 0, 0)

# Set up the clock
clock = pygame.time.Clock()

# Set up the font
font = pygame.font.Font(None, 36)


class Snake:
    def __init__(self, size):
        self.size = size
        self.x_pos = window_width // 2
        self.y_pos = window_height // 2
        self.x_vel = self.size
        self.y_vel = 0
        self.body = []
        self.length = 1
        self.can_change_direction = True

    def check_collision(self):
        head = (self.x_pos, self.y_pos)

        # Check collision with the boundaries of the window
        if self.x_pos < 0 or self.x_pos >= window_width or self.y_pos < 0 or self.y_pos >= window_height:
            return True

        # Check collision with the snake's body
        if head in self.body[:-1]:
            return True

        return False

    def update(self):
        if not self.can_change_direction:
            self.can_change_direction = True
        self.x_pos += self.x_vel
        self.y_pos += self.y_vel

        self.body.append((self.x_pos, self.y_pos))
        if len(self.body) > self.length:
            del self.body[0]

        if self.check_collision():
            return False

        return True


    def move_up(self):
        if self.can_change_direction and self.y_vel != self.size:
            self.x_vel = 0
            self.y_vel = -self.size
            self.can_change_direction = False

    def move_down(self):
        if self.can_change_direction and self.y_vel != -self.size:
            self.x_vel = 0
            self.y_vel = self.size
            self.can_change_direction = False

    def move_left(self):
        if self.can_change_direction and self.x_vel != self.size:
            self.x_vel = -self.size
            self.y_vel = 0
            self.can_change_direction = False

    def move_right(self):
        if self.can_change_direction and self.x_vel != -self.size:
            self.x_vel = self.size
            self.y_vel = 0
            self.can_change_direction = False

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, green, (segment[0], segment[1], self.size, self.size))


class Food:
    def __init__(self, size):
        self.size = size
        self.x = random.randint(0, window_width - self.size) // self.size * self.size
        self.y = random.randint(0, window_height - self.size) // self.size * self.size

    def generate(self):
        self.x = random.randint(0, window_width - self.size) // self.size * self.size
        self.y = random.randint(0, window_height - self.size) // self.size * self.size

    def draw(self, window):
        pygame.draw.rect(window, red, (self.x, self.y, self.size, self.size))


# Create the snake and food
snake = Snake(20)
food = Food(20)

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.move_up()
            elif event.key == pygame.K_DOWN:
                snake.move_down()
            elif event.key == pygame.K_LEFT:
                snake.move_left()
            elif event.key == pygame.K_RIGHT:
                snake.move_right()

    if not snake.update() or snake.check_collision():
        running = False

    if snake.x_pos == food.x and snake.y_pos == food.y:
        food.generate()

    window.fill(black)
    snake.draw(window)
    food.draw(window)

    score_text = font.render(f"Score: {snake.length - 1}", True, (255, 255, 255))
    window.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
