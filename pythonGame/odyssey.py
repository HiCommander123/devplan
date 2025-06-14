import pygame
import asyncio
import platform
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
SHIP_SPEED = 5
ARROW_SPEED = 10
BOMB_SPEED = 5
CYAN = (0, 255, 255)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Setup display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Magellan's Simple Voyage with Arrow and Bomb")
clock = pygame.time.Clock()

# Ship class
class Ship(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        try:
            self.image = pygame.image.load("C:\\Users\\Albert\\Documents\\Juwon\\JuneProject\\pythonGame\\Ship.png").convert_alpha()
            self.image = pygame.transform.scale(self.image, (60, 40))  # Adjust size if needed
            self.image.set_colorkey(WHITE)  # Make white background transparent
        except pygame.error as e:
            print(f"Error loading Ship.png: {e}")
            self.image = pygame.Surface((30, 20), pygame.SRCALPHA)
            pygame.draw.polygon(self.image, WHITE, [(0, 20), (15, 0), (30, 20)])  # Fallback
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.visible = True

    def update(self, keys):
        if self.visible:
            if keys[pygame.K_w] and self.rect.top > 0:
                self.rect.y -= SHIP_SPEED
            if keys[pygame.K_s] and self.rect.bottom < HEIGHT:
                self.rect.y += SHIP_SPEED
            if keys[pygame.K_a] and self.rect.left > 0:
                self.rect.x -= SHIP_SPEED
            if keys[pygame.K_d] and self.rect.right < WIDTH:
                self.rect.x += SHIP_SPEED

# Arrow class
class Arrow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 5), pygame.SRCALPHA)
        pygame.draw.rect(self.image, BLACK, (0, 0, 20, 5))  # Simple black arrow
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = ARROW_SPEED

    def update(self):
        self.rect.x += self.speed  # Move right
        if self.rect.right > WIDTH or self.rect.left < 0:
            self.kill()  # Remove arrow when out of screen

# Bomb class
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(self.image, BLACK, (7, 7), 7)  # Simple black circle for bomb
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = BOMB_SPEED

    def update(self):
        self.rect.y += self.speed  # Move downward
        if self.rect.bottom > HEIGHT or self.rect.top < 0:
            self.kill()  # Remove bomb when out of screen

# Goal class
class Goal(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH - 50, HEIGHT - 50)

# Initialize sprites
all_sprites = pygame.sprite.Group()
arrows = pygame.sprite.Group()
bombs = pygame.sprite.Group()
ship = Ship(WIDTH // 2, HEIGHT // 2)
goal = Goal()
all_sprites.add(ship, goal)

# Font
font = pygame.font.SysFont(None, 36)

async def main():
    running = True
    game_over = False

    while running:
        pygame.event.pump()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Toggle ship visibility
                    ship.visible = not ship.visible
                if event.key == pygame.K_SPACE and ship.visible:  # Space key to drop bomb
                    bomb = Bomb(ship.rect.centerx, ship.rect.bottom)
                    all_sprites.add(bomb)
                    bombs.add(bomb)
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and ship.visible:  # Left click to shoot
                arrow = Arrow(ship.rect.centerx, ship.rect.centery)
                all_sprites.add(arrow)
                arrows.add(arrow)

        if not game_over:
            keys = pygame.key.get_pressed()
            ship.update(keys)

            # Update arrows and bombs
            arrows.update()
            bombs.update()

            # Check collision with goal
            if ship.visible and pygame.sprite.collide_rect(ship, goal):
                game_over = True

        # Draw
        screen.fill(CYAN)  # Sky blue ocean
        all_sprites.draw(screen)
        if not ship.visible:
            ship.image.set_alpha(0)  # Hide ship by setting alpha to 0

        # Game over screen
        if game_over:
            result_text = font.render("Victory! Reached the Philippines!", True, WHITE)
            screen.blit(result_text, (WIDTH // 2 - 200, HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)
        await asyncio.sleep(1.0 / FPS)

    pygame.quit()
    sys.exit()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())