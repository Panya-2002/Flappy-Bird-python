import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH = 500
SCREEN_HEIGHT = 400
GROUND_HEIGHT = 100
GRAVITY = 0.25
BIRD_VELOCITY = 0
FLAP_VELOCITY = -5
PIPE_WIDTH = 70
PIPE_HEIGHT = random.randint(150, 250)
PIPE_GAP = 150
PIPE_VELOCITY = -3

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Load images
bg_image = pygame.image.load('background.png').convert()
ground_image = pygame.image.load('ground.png').convert()
bird_image = pygame.image.load('bird.png').convert()
pipe_image = pygame.image.load('pipe.png').convert()

# Resize images
bird_image = pygame.transform.scale(bird_image, (50, 35))
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, GROUND_HEIGHT))

# Bird class
class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0

    def flap(self):
        self.velocity = FLAP_VELOCITY

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def draw(self):
        screen.blit(bird_image, (self.x, self.y))

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, 250)

    def update(self):
        self.x += PIPE_VELOCITY

    def draw(self):
        screen.blit(pipe_image, (self.x, 0))
        screen.blit(pygame.transform.flip(pipe_image, False, True), (self.x, self.height + PIPE_GAP))

# Main game loop
clock = pygame.time.Clock()
bird = Bird(50, SCREEN_HEIGHT // 2)
pipes = [Pipe(SCREEN_WIDTH + i * 300) for i in range(2)]

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()

    # Update game objects
    bird.update()
    for pipe in pipes:
        pipe.update()

    # Check for collisions
    if bird.y > SCREEN_HEIGHT - GROUND_HEIGHT or bird.y < 0:
        pygame.quit()
        quit()

    for pipe in pipes:
        if bird.x + bird_image.get_width() > pipe.x and bird.x < pipe.x + PIPE_WIDTH:
            if bird.y < pipe.height or bird.y + bird_image.get_height() > pipe.height + PIPE_GAP:
                pygame.quit()
                quit()

    # Remove off-screen pipes and add new ones
    pipes = [pipe for pipe in pipes if pipe.x > -PIPE_WIDTH]
    if pipes[-1].x < SCREEN_WIDTH - 300:
        pipes.append(Pipe(SCREEN_WIDTH))

    # Draw everything
    screen.blit(bg_image, (0, 0))
    for pipe in pipes:
        pipe.draw()
    bird.draw()
    screen.blit(ground_image, (0, SCREEN_HEIGHT - GROUND_HEIGHT))
    pygame.display.update()

    # Limit frames per second
    clock.tick(60)
