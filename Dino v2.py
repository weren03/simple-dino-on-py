import pygame
import random
import sys

# Инициализация pygame
pygame.init()

# Размеры окна
WIDTH = 800
HEIGHT = 300
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GROUND_Y = 250

# Создаем окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("DINO")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont(None, 36)
big_font = pygame.font.SysFont(None, 64)

# Динозаврик
class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((100, 100, 100))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = GROUND_Y - self.rect.height
        self.vel_y = 0
        self.jump_power = -15
        self.gravity = 1
        self.on_ground = True

    def update(self):
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        if self.rect.y >= GROUND_Y - self.rect.height:
            self.rect.y = GROUND_Y - self.rect.height
            self.vel_y = 0
            self.on_ground = True

    def jump(self):
        if self.on_ground:
            self.vel_y = self.jump_power
            self.on_ground = False

# Кактус
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 40))
        self.image.fill((34, 139, 34))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 100)
        self.rect.y = GROUND_Y - self.rect.height
        self.speed = 7

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

# Функция для отображения текста
def draw_text(text, font, color, x, y, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    screen.blit(surface, rect)

# Основной цикл игры
def game_loop():
    dino = Dino()
    all_sprites = pygame.sprite.Group()
    cacti = pygame.sprite.Group()
    all_sprites.add(dino)

    score = 0
    spawn_timer = 0
    game_over = False

    while True:
        clock.tick(FPS)
        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if not game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()
            if game_over and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game_loop()  # рестарт игры

        if not game_over:
            spawn_timer += 1
            if spawn_timer > random.randint(60, 100):
                cactus = Cactus()
                all_sprites.add(cactus)
                cacti.add(cactus)
                spawn_timer = 0

            all_sprites.update()

            if pygame.sprite.spritecollideany(dino, cacti):
                game_over = True

            score += 1

        all_sprites.draw(screen)
        draw_text(f"Счёт: {score // 10}", font, BLACK, 10, 10)
        draw_text(f"SPACE - прыжок", font, BLACK, 10, 40)

        if game_over:
            draw_text("Игра окончена", big_font, BLACK, WIDTH // 2, HEIGHT // 2 - 30, center=True)
            draw_text(f"Cчёт: {score // 10}", font, BLACK, WIDTH // 2, HEIGHT // 2 + 20, center=True)
            draw_text("Нажмите R чтобы перезапустить", font, BLACK, WIDTH // 2, HEIGHT // 2 + 60, center=True)

        pygame.display.flip()

game_loop()
