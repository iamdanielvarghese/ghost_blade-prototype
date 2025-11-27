import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hero Prototype")

clock = pygame.time.Clock()

# Load & scale hero sprite
hero_img = pygame.image.load("hero_idle.png").convert_alpha()
hero_img = pygame.transform.scale(hero_img, (64, 64))

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
            self.vel_y = -9
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += 0.7  # gravity force
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

# ----- ENEMY CLASS -----


class Enemy:
    def __init__(self, x, y):
        self.image = pygame.Surface((40, 60))  # temporary placeholder body
        self.image.fill((200, 50, 50))  # red enemy for now
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.alert = False
        self.speed = 2
        self.direction = 1  # 1 = right , -1 = left

    def update(self, detected, hero_rect):
        if detected:
            self.alert = True
            self.speed = 0  # stop moving

        # Face the hero
            if hero_rect.centerx > self.rect.centerx:
                self.direction = 1
            else:
                self.direction = -1
        else:
            self.alert = False
            self.speed = 2  # normal patrol
            self.rect.x += self.speed * self.direction

        # Flip direction on screen borders
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.direction *= -1
        if self.rect.left < 0:
            self.rect.left = 0
            self.direction *= -1

    def draw_vision_cone(self, surface, detected):
        cone_length = 200  # how far the enemy can see
        cone_width = 80  # spread angle width

        # Points of the triangle
        if self.direction == 1:  # facing right
            p1 = (self.rect.centerx, self.rect.centery - 20)
            p2 = (self.rect.centerx + cone_length,
                  self.rect.centery - 20 - cone_width // 2)
            p3 = (self.rect.centerx + cone_length,
                  self.rect.centery - 20 + cone_width // 2)
        else:
            p1 = (self.rect.centerx, self.rect.centery - 20)
            p2 = (self.rect.centerx - cone_length,
                  self.rect.centery - 20 - cone_width // 2)
            p3 = (self.rect.centerx - cone_length,
                  self.rect.centery - 20 + cone_width // 2)

        # choose cone color
        color = (255, 0, 0, 60) if detected else (255, 255, 0, 60)
        # Transparent surface
        cone_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        pygame.draw.polygon(cone_surface, color, (p1, p2, p3))

        surface.blit(cone_surface, (0, 0))

        return (p1, p2, p3)  # return points for detection check

    def draw(self, surface):
        surface.blit(self.image, self.rect)

    def draw_alert(self, surface):
        if self.alert:
            font = pygame.font.SysFont("Arial", 28, bold=True)
            text = font.render("!", True, (255, 0, 0))
            surface.blit(text, (self.rect.centerx - 5, self.rect.top - 25))


# ---- PLATFORMS ----
platforms = [
    pygame.Rect(0, 380, 800, 50)
]


# Create the hero
hero = Hero(200, 200)

# Creat the enemy
enemy = Enemy(300, 320)


def point_in_triangle(pt, v1, v2, v3):
    def sign(p1, p2, p3):
        return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

    b1 = sign(pt, v1, v2) < 0.0
    b2 = sign(pt, v1, v3) < 0.0
    b3 = sign(pt, v2, v3) < 0.0

    return ((b1 == b2) and (b2 == b3))


# --- MAIN GAME LOOP ---
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    hero.update()

# --- calculate detection BEFORE updating enemy ---
    (p1, p2, p3) = enemy.draw_vision_cone(screen, False)
    hero_center = hero.rect.center
    detected = point_in_triangle(hero_center, p1, p2, p3)

# Direction-based filtering
    if enemy.direction == 1 and hero.rect.centerx < enemy.rect.centerx:
        detected = False
    if enemy.direction == -1 and hero.rect.centerx > enemy.rect.centerx:
        detected = False

# --- now enemy knows whether hero is detected ---
    enemy.update(detected, hero.rect)

# --- draw everything ---
    screen.blit(background, (0, 0))
    enemy.draw_vision_cone(screen, detected)
    enemy.draw(screen)
    enemy.draw_alert(screen)
    hero.draw(screen)
    pygame.display.flip()
    clock.tick(60)
