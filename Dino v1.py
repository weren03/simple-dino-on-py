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
pygame.display.set_caption("Динозаврик")
clock = pygame.time.Clock()

# Шрифт
font = pygame.font.SysFont(None, 36)

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

# Кактус (препятствие)
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

# Функция для отображения счета
def draw_score(score):
    text = font.render(f"Счёт: {score}", True, BLACK)
    screen.blit(text, (10, 10))

# Основной цикл игры
def game_loop():
    dino = Dino()
    all_sprites = pygame.sprite.Group()
    cacti = pygame.sprite.Group()

    all_sprites.add(dino)

    score = 0
    spawn_timer = 0

    running = True
    while running:
        clock.tick(FPS)
        screen.fill(WHITE)
        pygame.draw.line(screen, BLACK, (0, GROUND_Y), (WIDTH, GROUND_Y), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dino.jump()

        # Спавн препятствий
        spawn_timer += 1
        if spawn_timer > random.randint(60, 100):
            cactus = Cactus()
            all_sprites.add(cactus)
            cacti.add(cactus)
            spawn_timer = 0

        all_sprites.update()

        # Проверка столкновений
        if pygame.sprite.spritecollideany(dino, cacti):
            print(f"Игра окончена! Ваш счёт: {score}")
            running = False

        # Увеличение счета
        score += 1

        all_sprites.draw(screen)
        draw_score(score // 10)

        pygame.display.flip()

game_loop()
pygame.quit()
