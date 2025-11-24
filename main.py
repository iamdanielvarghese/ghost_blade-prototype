import pygame
import sys

# Initialize pygame
pygame.init()

# Create the game window
WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero Prototype")

# Set FPS control
clock = pygame.time.Clock()

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Fill background
    screen.fill((30, 30, 30))  # dark grey
    # Load hero sprite
    hero_img = pygame.image.load("hero_idle.png").convert_alpha()

    # Scale DOWN to the size you want on screen
    hero_img = pygame.transform.scale(hero_img, (70, 70))

    # Draw hero at position (x, y)
    screen.blit(hero_img, (100, 300))

    # Update display
    pygame.display.flip()
    clock.tick(60)
