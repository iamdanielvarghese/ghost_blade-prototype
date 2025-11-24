import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero Prototype")

clock = pygame.time.Clock()

# Load & scale hero sprite
hero_img = pygame.image.load("hero_idle.png").convert_alpha()
hero_img = pygame.transform.scale(hero_img, (48, 48))

# --- HERO CLASS ---


class Hero:
    def __init__(self, x, y):
        self.image = hero_img
        self.rect = self.image.get_rect()
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

# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((30, 30, 30))

    hero.update()
    hero.draw(screen)

    pygame.display.flip()
    clock.tick(60)
