import subprocess

import pygame
from config import *
import math
import random


class Spritesheet:
    def __init__(self, file):
        self.sheet = pygame.image.load(file).convert_alpha()

    def get_sprite(self, x, y, width, height):
        sprite = pygame.Surface((width, height))
        sprite.blit(self.sheet, (0, 0), (x, y, 32, 32))
        sprite.set_colorkey(BLACK)
        return sprite


class Player(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = 1
        self.game = game
        self._layer = PLAYER_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.frame_counter = 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE
        self.x_change = 0
        self.y_change = 0

        self.facing = 'down'

        self.image = pygame.image.load("img/down.png").convert_alpha()
        self.image.set_colorkey([255, 255, 255])

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def update(self):
        if (self.game.paused == False):
            self.movement()
            self.collide_enemy()
            self.rect.x += self.x_change
            self.collide_blocks('x')
            self.rect.y += self.y_change
            self.collide_blocks('y')

            self.x_change = 0
            self.y_change = 0

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            # for sprite in self.game.all_sprites:
            # sprite.rect.x += PLAYER_SPEED
            self.frame_counter += 1
            if self.frame_counter >= 1:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/left0.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/left1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/left2.png").convert_alpha()

                self.image.set_colorkey([255, 255, 255])
                # self.image = pygame.Surface((self.width, self.height))
                self.image.blit(self.image, (0, 0))

                self.x_change -= PLAYER_SPEED
                self.facing = 'left'
                self.i = self.i + 1
                self.frame_counter = 0
        if keys[pygame.K_RIGHT] and not keys[pygame.K_UP] and not keys[pygame.K_DOWN]:
            self.frame_counter += 1
            # for sprite in self.game.all_sprites:
            # sprite.rect.x -= PLAYER_SPEED
            if self.frame_counter >= 1:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/right0.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/right1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/right2.png").convert_alpha()

                self.image.set_colorkey([255, 255, 255])
                # self.image = pygame.Surface((self.width, self.height))
                self.image.blit(self.image, (0, 0))

                self.x_change += PLAYER_SPEED
                self.facing = 'right'
                self.i = self.i + 1
                self.frame_counter = 0
        if keys[pygame.K_UP] and not keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
            self.frame_counter += 1
            # for sprite in self.game.all_sprites:
            # sprite.rect.y += PLAYER_SPEED
            if self.frame_counter >= 1:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/up0.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/up1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/up2.png").convert_alpha()

                self.image.set_colorkey([255, 255, 255])
                self.image.blit(self.image, (0, 0))
                self.y_change -= PLAYER_SPEED
                self.facing = 'up'
                self.i = self.i + 1
                self.frame_counter = 0

        if keys[pygame.K_DOWN] and not keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
            # for sprite in self.game.all_sprites:
            # sprite.rect.y -= PLAYER_SPEED
            self.frame_counter += 1
            if self.frame_counter >= 1:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/down.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/down1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/down2.png").convert_alpha()

                self.image.set_colorkey([255, 255, 255])
                self.image.blit(self.image, (0, 0))
                self.y_change += PLAYER_SPEED
                self.facing = 'down'
                self.i = self.i + 1
                self.frame_counter = 0

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.game.playing = False
            self.kill()

            # self.battle()

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def battle(self):
        self.game.paused = True
        self.game.game_over()
        pokemon_name1 = str(random.randint(1, 500))
        pokemon_name2 = str(random.randint(1, 500))
        pokemon_name3 = str(random.randint(1, 500))
        pokemon_name = pokemon_name1 + "," + pokemon_name2 + "," + pokemon_name3

        try:
            subprocess.Popen(["py", "pokemon.py", pokemon_name])
        except Exception as e:
            print("Wystąpił błąd podczas uruchamiania programu Java:", e)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.i = 1
        self.game = game
        self.left_animations = []
        self.right_animations = []
        self.frame_counter = 0
        self._layer = ENEMY_LAYER
        self.groups = self.game.all_sprites, self.game.enemies
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.x_change = 0
        self.y_change = 0

        self.facing = random.choice(['left', 'right'])
        self.animation_loop = 1
        self.movement_loop = 0
        self.max_travel = random.randint(7, 30)

        self.image = pygame.image.load("img/enedown0.png").convert_alpha()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def collide_blocks(self, direction):
        if direction == "x":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.x_change > 0:
                    self.rect.x = hits[0].rect.left - self.rect.width
                if self.x_change < 0:
                    self.rect.x = hits[0].rect.right
        if direction == "y":
            hits = pygame.sprite.spritecollide(self, self.game.blocks, False)
            if hits:
                if self.y_change > 0:
                    self.rect.y = hits[0].rect.top - self.rect.height
                if self.y_change < 0:
                    self.rect.y = hits[0].rect.bottom

    def collide_enemy(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, False)
        if hits:
            self.kill()

    def update(self):
        if (self.game.paused == False):
            self.movement()
            self.rect.x += self.x_change
            self.collide_blocks('x')
            self.rect.y += self.y_change
            self.collide_blocks('y')
            # self.collide_enemy()

            self.x_change = 0
            self.y_change = 0

    def movement(self):
        self.frame_counter += 1
        if self.facing == 'left':
            self.frame_counter += 1
            if self.frame_counter >= 27:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft0.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft2.png").convert_alpha()
                self.i = self.i + 1
                self.frame_counter = 0

            self.x_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.max_travel = random.randint(1, 50)
                self.i = 1
                self.facing = 'up'
        if self.facing == 'up':
            self.frame_counter += 1
            if self.frame_counter >= 27:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft0.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft2.png").convert_alpha()
                self.i = self.i + 1
                self.frame_counter = 0

            self.y_change += ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.max_travel = random.randint(1, 50)
                self.i = 1
                self.facing = 'down'
        if self.facing == 'down':
            self.frame_counter += 1
            if self.frame_counter >= 27:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft0.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/eneleft2.png").convert_alpha()
                self.i = self.i + 1
                self.frame_counter = 0

            self.y_change -= ENEMY_SPEED
            self.movement_loop -= 1
            if self.movement_loop <= -self.max_travel:
                self.max_travel = random.randint(1, 50)
                self.i = 1
                self.facing = 'right'
        if self.facing == 'right':
            self.frame_counter += 1
            if self.frame_counter >= 27:
                if (self.i % 3 == 0):
                    print(self.i)
                    self.image = pygame.image.load("img/eneright0.png").convert_alpha()

                if (self.i % 3 == 1):
                    print(self.i)
                    self.image = pygame.image.load("img/eneright1.png").convert_alpha()
                if (self.i % 3 == 2):
                    print(self.i)
                    self.image = pygame.image.load("img/eneright2.png").convert_alpha()
                self.i = self.i + 1
                self.frame_counter = 0
            self.x_change += ENEMY_SPEED
            self.movement_loop += 1
            if self.movement_loop >= self.max_travel:
                self.max_travel = random.randint(1, 50)
                self.i = 1
                self.facing = 'left'


class Button:
    def __init__(self, x, y, width, height, fg, bg, content, fontsize):
        self.font = pygame.font.Font("arial.ttf", fontsize)
        self.content = content

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.fg = fg
        self.bg = bg
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(self.bg)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.text = self.font.render(self.content, True, self.fg)
        self.text_rect = self.text.get_rect(center=(self.width / 2, self.height / 2))
        self.image.blit(self.text, self.text_rect)

    def is_pressed(self, pas, pressed):
        if self.rect.collidepoint(pas):
            if pressed[0]:
                return True
            return False
        return False


class Block(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.blocks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.terrain_spritesheet.get_sprite(0, 0, 32, 32)

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Ground(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = GROUND_LAYER
        self.groups = self.game.all_sprites
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.width = TILESIZE
        self.height = TILESIZE

        self.image = self.game.grass.get_sprite(100, 100, self.width, self.height)
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y


class Attack(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        self.game = game
        self._layer = BLOCK_LAYER
        self.groups = self.game.all_sprites, self.game.attacks
        pygame.sprite.Sprite.__init__(self, self.groups)

        self.x = x
        self.y = y
        #self.width = TILESIZE
        self.height = TILESIZE
        self.i = 0
        self.animation_loop = 0
        self.animation_frames_right = [pygame.image.load("img/attack1.png").convert_alpha(),
                                 pygame.image.load("img/attack2.png").convert_alpha(),
                                 pygame.image.load("img/attack3.png").convert_alpha()]
        self.animation_frames_left = [pygame.image.load("img/attack1_l.png").convert_alpha(),
                                 pygame.image.load("img/attack2_l.png").convert_alpha(),
                                 pygame.image.load("img/attack3_l.png").convert_alpha()]
        self.animation_frames_down = [pygame.image.load("img/attack1_d.png").convert_alpha(),
                                 pygame.image.load("img/attack2_d.png").convert_alpha(),
                                 pygame.image.load("img/attack3_d.png").convert_alpha()]
        self.animation_frames_up = [pygame.image.load("img/attack1_u.png").convert_alpha(),
                                 pygame.image.load("img/attack2_u.png").convert_alpha(),
                                 pygame.image.load("img/attack3_u.png").convert_alpha()]
        self.current_frame_index = 0

        self.image = pygame.image.load("img/attack1.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.duration  = 10
        self.current_frame = 0
        self.animation_speed = 5
        self.frame_counter = 0

    def update(self):
        self.animate()
        self.collide()
        self.current_frame += 1
        if self.current_frame >= self.duration:
            self.kill()

    def collide(self):
        hits = pygame.sprite.spritecollide(self, self.game.enemies, True)

    def animate(self):
        direction = self.game.player.facing

        if direction == "up":
            self.image = self.animation_frames_up[self.current_frame_index]
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames_up)
        if direction == "down":
            self.image = self.animation_frames_down[self.current_frame_index]
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames_down)
        if direction == "left":
            self.image = self.animation_frames_left[self.current_frame_index]
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames_left)
        if direction == "right":
            self.image = self.animation_frames_right[self.current_frame_index]
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_frame_index = (self.current_frame_index + 1) % len(self.animation_frames_right)

