import pygame as pg
import sys
import pytmx

from config import *

class Player(pg.sprite.Sprite):

    def __init__(self, game, x, y):

        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_img
        self.rect = self.image.get_rect()

        self.chips = 1
        self.gkeys = 0
        self.ykeys = 3
        self.fboots = 0
        self.wboots = 0

        self.x = x
        self.y = y

    def move(self, dx = 0, dy = 0):

        if not self.collide_with_walls(dx, dy):

            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx = 0, dy = 0):

        for wall in self.game.walls:

            if wall.x == self.x + dx and wall.y == self.y + dy:

                return True

        return False

    def update(self):

        self.rect.x = self.x * TILESIZE
        self.rect.y = self.y * TILESIZE

class Obstacle(pg.sprite.Sprite):

    def __init__(self, game, x, y):

        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.wall_img
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Item(pg.sprite.Sprite):

    def __init__(self, game, x, y, type):

        self._layer = ITEM_LAYER
        self.groups = game.all_sprites, game.items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.item_images[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
