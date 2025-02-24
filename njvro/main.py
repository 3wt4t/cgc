import pygame
import time
import random
import os
import sys

pygame.init()
pygame.key.set_repeat(200, 70)
clock = pygame.time.Clock()
STEP = 50
running = True
size = WIDTH, HEIGHT = width, height = 550, 550
screen = pygame.display.set_mode(size)
pygame.display.set_caption('ZOPYJ')

FPS = 50


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def terminate():
    pygame.quit()
    sys.exit()


def final_screen(f):
    filename = "data/" + 'record.txt'
    global guh
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    intro_text = ["ZOPYJ",
                  'the end',
                  "время: " + str(f),
                  'монет: ' + str(guh),
                  "предыдущий рекорд: " + level_map[0]]
    if f < int(level_map[0]):
        with open(filename, 'w') as mapFile:
            mapFile.write(str(f))
    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    controlling_screen()
                    terminate()
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_s:
                    return 'wd'
        pygame.display.flip()
        clock.tick(FPS)

def contng_screen():
    intro_text = ["ZOPYJ",
                  "монета"]

    fon = pygame.transform.scale(load_image('coin.png'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_s:
                    return 'wd'
        pygame.display.flip()
        clock.tick(FPS)


def start_screen():
    intro_text = ["ZOPYJ",
                  'начать [s]',
                  "управление [w]",
                  "выход [Esc]"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    return controlling_screen()
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_s:
                    return 'wd'
        pygame.display.flip()
        clock.tick(FPS)


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png'),
    'win': load_image('flag.png'),
    'coin': load_image('coin.png')

}
player_image = load_image('mario.png')

tile_width = tile_height = 50
guh = 0


def coinm():
    pygame.mixer.init()  # инициализация модуля микшера
    pygame.mixer.music.load('data/coin.mp3')
    pygame.mixer.music.play()


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x
        self.y = pos_y

    def repoz(self):
        u = (self.x, self.y)
        return u

    def move(self, px, py):
        u = None
        global guh
        if px < 0:
            u = (self.x - 1, self.y)
            if not(u in h):
                self.x -= 1
                player.rect.x += px
                if u in gh:
                    gh.remove(u)
                    print(gh)
                    guh += 1
                    Tile('coin', self.x, self.y)
                    coinm()

        elif px > 0:
            u = (self.x + 1, self.y)
            if not(u in h):
                self.x += 1
                player.rect.x += px
                if u in gh:
                    guh += 1
                    gh.remove(u)
                    print(gh)
                    Tile('coin', self.x, self.y)
                    coinm()
        elif py < 0:
            u = (self.x, self.y - 1)
            if not(u in h):
                self.y -= 1
                player.rect.y += py
                if u in gh:
                    guh += 1
                    gh.remove(u)
                    print(gh)
                    Tile('coin', self.x, self.y)
                    coinm()
        elif py > 0:
            u = (self.x, self.y + 1)
            if not(u in h):
                self.y += 1
                player.rect.y += py
                if u in gh:
                    guh += 1
                    gh.remove(u)
                    print(gh)
                    Tile('coin', self.x, self.y)
                    coinm()


player = None

# группы спрайтов
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
h = []
g = 0
gh = []


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                if random.choice((1, 2, 3)) == 2:
                    gh.append((x, y))
                    Tile('coin', x, y)
                else:
                    Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
                h.append((x, y))
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
            elif level[y][x] == '!':
                Tile('empty', x, y)
                Tile('win', x, y)
                win_poz = (x, y)
    # вернем игрока, а также размер поля в клетках
    print(gh)
    return new_player, x, y, win_poz


def controlling_screen():
    intro_text = ["ZOPYJ",
                  "вправо [d]",
                  "влево  [a]",
                  'назад  [s]',
                  "вперёд [w]",
                  "выход [Esc]",
                  '',
                  'start [s]']

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    terminate()
                if event.key == pygame.K_s:
                    return 'wd'
        pygame.display.flip()
        clock.tick(FPS)




camera = Camera()
teim = 0  # время
if start_screen() == 'wd':
    contng_screen()
    player, level_x, level_y, w_p = generate_level(load_level('map.txt'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    t = 0 - STEP
                    player.move(0, t)
                if event.key == pygame.K_a:
                    t = 0 - STEP
                    player.move(t, 0)
                if event.key == pygame.K_s:
                    player.move(0, STEP)
                if event.key == pygame.K_d:
                    player.move(STEP, 0)
        screen.fill(pygame.Color('black'))
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.set_caption('ZOPYJ' + 'время: ' + str(teim) + 'монетки: ' + str(guh))
        pygame.display.flip()
        teim += 1
        clock.tick(FPS)

        if player.repoz() == w_p:
            player = None
            g = 1
            tiles_group.empty()
            pygame.mixer.init()  # инициализация модуля микшера
            pygame.mixer.music.load('data/vic.mp3')
            pygame.mixer.music.play()
            time.sleep(3)
            break
gh = []
if g == 1:
    player = None
    player, level_x, level_y, w_p = generate_level(load_level('map1.txt'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    t = 0 - STEP
                    player.move(0, t)
                if event.key == pygame.K_a:
                    t = 0 - STEP
                    player.move(t, 0)
                if event.key == pygame.K_s:
                    player.move(0, STEP)
                if event.key == pygame.K_d:
                    player.move(STEP, 0)
        screen.fill(pygame.Color('black'))
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.set_caption('ZOPYJ' + 'время: ' + str(teim) + 'монетки: ' + str(guh))
        pygame.display.flip()
        teim += 1
        clock.tick(FPS)

        if player.repoz() == w_p:
            player_group.remove(player)
            g = 2
            tiles_group.empty()
            pygame.mixer.init()  # инициализация модуля микшера
            pygame.mixer.music.load('data/vic.mp3')
            pygame.mixer.music.play()
            time.sleep(3)
            break
gh = []
if g == 2:
    player = None
    player, level_x, level_y, w_p = generate_level(load_level('map2.txt'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    t = 0 - STEP
                    player.move(0, t)
                if event.key == pygame.K_a:
                    t = 0 - STEP
                    player.move(t, 0)
                if event.key == pygame.K_s:
                    player.move(0, STEP)
                if event.key == pygame.K_d:
                    player.move(STEP, 0)
        screen.fill(pygame.Color('black'))
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.set_caption('ZOPYJ' + 'время: ' + str(teim) + 'монетки: ' + str(guh))
        pygame.display.flip()
        teim += 1
        clock.tick(FPS)

        if player.repoz() == w_p:
            g = 3
            tiles_group.empty()
            pygame.mixer.init()  # инициализация модуля микшера
            pygame.mixer.music.load('data/vic.mp3')
            pygame.mixer.music.play()
            time.sleep(3)
            break
if g == 3:
    player = None
    player, level_x, level_y, w_p = generate_level(load_level('map3.txt'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    t = 0 - STEP
                    player.move(0, t)
                if event.key == pygame.K_a:
                    t = 0 - STEP
                    player.move(t, 0)
                if event.key == pygame.K_s:
                    player.move(0, STEP)
                if event.key == pygame.K_d:
                    player.move(STEP, 0)
        screen.fill(pygame.Color('black'))
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.set_caption('ZOPYJ' + 'время: ' + str(teim) + 'монетки: ' + str(guh))
        pygame.display.flip()
        teim += 1
        clock.tick(FPS)

        if player.repoz() == w_p:
            g = 4
            tiles_group.empty()
            pygame.mixer.init()  # инициализация модуля микшера
            pygame.mixer.music.load('data/vic.mp3')
            pygame.mixer.music.play()
            time.sleep(3)
            break
if g == 4:
    player = None
    player, level_x, level_y, w_p = generate_level(load_level('map4.txt'))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    t = 0 - STEP
                    player.move(0, t)
                if event.key == pygame.K_a:
                    t = 0 - STEP
                    player.move(t, 0)
                if event.key == pygame.K_s:
                    player.move(0, STEP)
                if event.key == pygame.K_d:
                    player.move(STEP, 0)
        screen.fill(pygame.Color('black'))
        # изменяем ракурс камеры
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            camera.apply(sprite)
        tiles_group.draw(screen)
        player_group.draw(screen)
        pygame.display.set_caption('ZOPYJ' + 'время: ' + str(teim) + 'монетки: ' + str(guh))
        pygame.display.flip()
        teim += 1
        clock.tick(FPS)

        if player.repoz() == w_p:
            g = 5
            tiles_group.empty()
            pygame.mixer.init()  # инициализация модуля микшера
            pygame.mixer.music.load('data/vic.mp3')
            pygame.mixer.music.play()
            time.sleep(3)
            break
final_screen(teim)
for i in player_group:
    print(i)
terminate()