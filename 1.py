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

    # ---- Hero Class -----

    class Hero:
        def _init(self, x, y):
            self.image = hero_img
            self.rect = self.image.get.rect()
            self.rect.topleft = (x, y)

            self.vel_y = 0
            self.speed = 4
            self.on_ground = False

        def handle_input(self):
            keys = pygame.key.get_pressed()

            # Move left
            if keys[pygame.K_a] or keys[pygame.K_LEFT]:
                self.rect.x -= self.speed

            # Move right
            if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                self.rect.x += self.speed

             # Jump
            if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
                self.vel_y = -12
                self.on_ground = False

        def apply_gravity(self):
            self.vel_y += 0.5  # gravity force
            if self.vel_y > 10:
                self.vel_y = 10
                self.rect.y += self.vel_y

    def check_ground(self):
        ground_y = 350  # ground level

        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.vel_y = 0
            self.on_ground = True

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.check_ground()

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Create the hero
hero = Hero(200, 200)

# Update display
pygame.display.flip()
clock.tick(60)
