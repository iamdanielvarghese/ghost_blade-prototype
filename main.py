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

    def check_ground(self, platform_list):
        self.on_ground = False

        for plat in platform_list:
            # Check only if hero is falling
            if self.vel_y > 0 and self.rect.colliderect(plat):
                # Hero stands on the platform
                self.rect.bottom = plat.top
                self.vel_y = 0
                self.on_ground = True

    def update(self):
        self.handle_input()
        self.apply_gravity()
        self.check_ground(platforms)

       # Keep hero inside screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def draw(self, surface):
        surface.blit(self.image, self.rect)


# Background
background = pygame.image.load("background.png").convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

# ---- PLATFORMS ----
platforms = [
    pygame.Rect(0, 350, 800, 50)

]


# Create the hero
hero = Hero(200, 200)

# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.blit(background, (0, 0))

    hero.update()

    hero.draw(screen)

    pygame.display.flip()
    clock.tick(60)
