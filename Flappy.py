import pygame
import random
import pyfirmata
import time

# Setup Pygame
pygame.init()

# Game constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
BIRD_WIDTH = 20
BIRD_HEIGHT = 20
GRAVITY = 0.8
FLAP_STRENGTH = -15
PIPE_WIDTH = 70
PIPE_GAP = 350
PIPE_VELOCITY = 4
GAME_SPEED = 30  # Frames per second (FPS)

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird with Push Button")

# Setup colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Bird class
class Bird:
    def __init__(self):
        self.x = SCREEN_WIDTH // 4
        self.y = SCREEN_HEIGHT // 2
        self.width = BIRD_WIDTH
        self.height = BIRD_HEIGHT
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_STRENGTH

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.width, self.height))

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.width = PIPE_WIDTH

    def move(self):
        self.x -= PIPE_VELOCITY

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, (self.x, 0, self.width, self.height))
        pygame.draw.rect(screen, GREEN, (self.x, self.height + PIPE_GAP, self.width, SCREEN_HEIGHT - self.height - PIPE_GAP))

    def off_screen(self):
        return self.x < -self.width

    def collide(self, bird):
        if bird.x + bird.width > self.x and bird.x < self.x + self.width:
            if bird.y < self.height or bird.y + bird.height > self.height + PIPE_GAP:
                return True
        return False

# Setup Firmata and Arduino
board = pyfirmata.Arduino('COM7')  # Replace with your correct port
it = pyfirmata.util.Iterator(board)
it.start()

# Read push button value (from digital pin 2)
button_pin = board.get_pin('d:4:i')  # Input pin for push button (digital pin 2)

# Game loop
def game_loop():
    bird = Bird()
    pipes = [Pipe()]
    score = 0
    clock = pygame.time.Clock()
    running = True

    while running:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Check if the button is pressed (button_pin is HIGH when pressed)
        button_pressed = button_pin.read()
        if button_pressed is not None and button_pressed == 0:  # Button pressed
            bird.flap()

        # Move bird
        bird.move()

        # Move and add new pipes
        for pipe in pipes:
            pipe.move()
            if pipe.off_screen():
                pipes.remove(pipe)
                pipes.append(Pipe())
                score += 1

        # Check for collisions
        for pipe in pipes:
            if pipe.collide(bird):
                running = False

        # Draw objects
        bird.draw(screen)
        for pipe in pipes:
            pipe.draw(screen)

        # Draw score
        font = pygame.font.SysFont('Arial', 30)
        score_text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Update the screen
        pygame.display.flip()

        # Control game speed
        clock.tick(GAME_SPEED)

    pygame.quit()
    board.exit()

# Run the game loop
game_loop()
