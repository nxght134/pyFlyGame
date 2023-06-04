# Simple pygame program

# Import and initialize the pygame library
import pygame
import random
import pygame_widgets
from pygame_widgets.button import Button
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.image = pygame.image.load('D:/versions/python/pyGame/sprite/jet45.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 3, self.image.get_height() / 3))
        self.rect = self.image.get_rect()
        self.speed = 5

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -self.speed)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, self.speed)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    score = 0

    def __init__(self):
        super(Enemy, self).__init__()
        self.image = pygame.image.load('D:/versions/python/pyGame/sprite/rocket.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 8, self.image.get_height() / 8))
        self.rect = self.image.get_rect(
            center=(random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(5, 10)
        self.sound_collision = pygame.mixer.Sound("D:/versions/python/pyGame/music/stolknovenie.wav")
        self.sound_collision.set_volume(0.5)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            Enemy.score += 1
            self.sound_collision.play()
            self.kill()


class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.image = pygame.image.load('D:/versions/python/pyGame/sprite/cloud.png')
        self.image = pygame.transform.scale(self.image, (self.image.get_width() / 4, self.image.get_height() / 4))
        self.rect = self.image.get_rect(
            center=(random.randint(SCREEN_WIDTH + 60, SCREEN_WIDTH + 100), random.randint(0, SCREEN_HEIGHT)))
        self.speed = random.randint(2, 3)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


pygame.init()
pygame.mixer.init()
clock = pygame.time.Clock()

# Set up the drawing window
SCREEN_WIDTH = 1300
SCREEN_HEIGHT = 700
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

current_scene = None


def switch_scene(scene):
    global current_scene
    current_scene = scene


def menu():
    pygame.mixer.music.load("D:/versions/python/pyGame/music/menu.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.5)
    image = pygame.image.load("D:/versions/python/pyGame/sprite/image.png")
    rect = image.get_rect()
    screen.blit(image, rect)
    PRESSED_BUTTON = pygame.USEREVENT + 3
    button_height = 150
    button_width = 350
    font_button = pygame.font.Font("D:/versions/python/pyGame/sprite/text.ttf", 50)
    button = Button(screen, (SCREEN_WIDTH - button_width) / 2, SCREEN_HEIGHT / 2, button_width, button_height,
                    inactiveColour=(255, 153, 0), pressedColour=(166, 106, 17), hoverColour=(166, 106, 17),
                    onClick=pygame.time.set_timer, onClickParams=(PRESSED_BUTTON, 10), text="НАЧАТЬ", font=font_button,
                    radius=10)

    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                switch_scene(None)
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    switch_scene(None)
                    running = False
            elif event.type == PRESSED_BUTTON:
                switch_scene(game)
                running = False
                pygame.time.set_timer(PRESSED_BUTTON, 0)
                pygame_widgets.WidgetHandler._widgets.clear()
        pygame_widgets.update(events)
        pygame.display.flip()


def game():
    sound_exploision = pygame.mixer.Sound("D:/versions/python/pyGame/music/explosion.ogg")
    sound_exploision.set_volume(0.5)
    ADD_ENEMY = pygame.USEREVENT + 1
    ADD_CLOUD = pygame.USEREVENT + 2
    pygame.time.set_timer(ADD_ENEMY, 500)
    pygame.time.set_timer(ADD_CLOUD, 800)
    # Run until the user asks to quit
    player = Player()
    clouds = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    font_score = pygame.font.Font("D:/versions/python/pyGame/sprite/text.ttf", 50)

    running = True
    while running:

        for event in pygame.event.get():
            if event.type == QUIT:
                switch_scene(None)
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    switch_scene(None)
                    running = False
            elif event.type == ADD_ENEMY:
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADD_CLOUD:
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        score = Enemy.score
        clouds.update()

        screen.fill((128, 166, 255))
        text_score = font_score.render("Score: " + str(score), True, (0, 0, 0))
        screen.blit(text_score, (20, 25))
        for entity in all_sprites:
            screen.blit(entity.image, entity.rect)
        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            pygame.mixer.music.stop()
            sound_exploision.play()
            switch_scene(lose)
            running = False
        pygame.display.flip()
        clock.tick(90)


def lose():
    pygame.mixer.music.load("D:/versions/python/pyGame/music/lose.mp3")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(0.5)
    image = pygame.image.load("D:/versions/python/pyGame/sprite/image2.png")
    rect = image.get_rect()
    screen.blit(image, rect)
    RETURN_BUTTON = pygame.USEREVENT + 4
    button_height = 75
    button_width = 150
    font_button = pygame.font.Font("D:/versions/python/pyGame/sprite/text.ttf", 50)
    button_return = Button(screen, (SCREEN_WIDTH - button_width) / 2 - 85, SCREEN_HEIGHT / 1.5, button_width,
                           button_height,
                           inactiveColour=(255, 153, 0), pressedColour=(166, 106, 17), hoverColour=(166, 106, 17),
                           onClick=pygame.time.set_timer, onClickParams=(RETURN_BUTTON, 10), text="ЗАНОВО",
                           font=font_button,
                           radius=10)
    button_exit = Button(screen, (SCREEN_WIDTH - button_width) / 2 + 85, SCREEN_HEIGHT / 1.5, button_width,
                         button_height,
                         inactiveColour=(255, 153, 0), pressedColour=(166, 106, 17), hoverColour=(166, 106, 17),
                         onClick=pygame.time.set_timer, onClickParams=(QUIT, 10), text="ВЫЙТИ", font=font_button,
                         radius=10)
    text_score = font_button.render("Score: " + str(Enemy.score), True, (0, 0, 0))
    screen.blit(text_score, ((SCREEN_WIDTH - text_score.get_width()) / 2, SCREEN_HEIGHT / 1.5 - 150))
    Enemy.score = 0
    running = True
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == QUIT:
                switch_scene(None)
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    switch_scene(None)
                    running = False
            elif event.type == RETURN_BUTTON:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("D:/versions/python/pyGame/music/menu.mp3")
                pygame.mixer.music.play(loops=-1)
                pygame.mixer.music.set_volume(0.5)
                switch_scene(game)
                pygame.time.set_timer(RETURN_BUTTON, 0)
                pygame_widgets.WidgetHandler._widgets.clear()
                running = False

        pygame.display.flip()
        pygame_widgets.update(events)


switch_scene(menu)
while current_scene is not None:
    current_scene()

# Done! Time to quit.
pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()
