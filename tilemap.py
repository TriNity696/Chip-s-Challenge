import pygame as pg
import sys
import pytmx

from config import *

class Map:

    def __init__(self, filename):

        self.data = []

        with open(filename, 'rt') as f:

            for line in f:

                self.data.append(line.strip())

        self.tilewidth = len(self.data[0])
        self.tileheight = len(self.data)
        self.width = self.tilewidth * TILESIZE
        self.height = self.tileheight * TILESIZE

class  TiledMap:

    def __init__(self, filename):

        tm = pytmx.load_pygame(filename, pixelalpha = True)
        self.width = tm.width * tm.tilewidth
        self.height = tm.height * tm.tileheight
        self.tmxdata = tm

    def render(self, surface):

        ti = self.tmxdata.get_tile_image_by_gid

        for layer in self.tmxdata.visible_layers:

            if isinstance(layer, pytmx.TiledTileLayer):

                for x, y, gid, in layer:

                    tile = ti(gid)

                    if tile:
                        surface.blit(tile,(x * self.tmxdata.tilewidth, y * self.tmxdata.tileheight))

    def make_map(self):
        
        temp_surface = pg.Surface((self.width, self.height))
        self.render(temp_surface)

        return temp_surface

class Camera:

    def __init__(self, width, height):

        self.camera = pg.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):

        return entity.rect.move(self.camera.topleft)

    def apply_rect(self, rect):
        
        return rect.move(self.camera.topleft)

    def update(self, target):

        x = -target.rect.x + int(WIDTH / 2)
        y = -target.rect.y + int(HEIGHT / 2)

        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - WIDTH), x)
        y = max(-(self.height - HEIGHT), y)
        
        self.camera = pg.Rect(x, y, self.width, self.height)       
    
class UserInterface:
    
    def __init__(self, player):

        self._layer = UI_LAYER
        self.smallfont = pg.font.SysFont("Fonts/MinecraftRegular-Bmg3.otf", 12)
        self.regularfont = pg.font.SysFont("Fonts/MinecraftRegular-Bmg3.otf", 20)
        self.largefont = pg.font.SysFont("Fonts/MinecraftRegular-Bmg3.otf", 40)

        self.playerRef = player
        
        self.inventory = Inventory(player)
        self.showInventory = True

    def update(self):

        self.inventory.update()
        
    def render(self, dplay):
        
        if self.showInventory:
            self.inventory.render(dplay)

class Inventory:

    def __init__(self, player):

        self._layer = UI_LAYER
        self.image = pg.image.load("Assets/inventory.png")
        self.slots = []
        self.playerRef = player

        self.slots.append(InventorySlot("Assets/chipbar.png", (2.25 * TILESIZE, 10.1 * TILESIZE)))
        self.slots.append(InventorySlot("Assets/greenkeybar.png", (3.4 * TILESIZE, 10.1 * TILESIZE)))
        self.slots.append(InventorySlot("Assets/yellowkeybar.png", (4.7 * TILESIZE, 10.1 * TILESIZE)))
        self.slots.append(InventorySlot("Assets/firebootsbar.png", (6.1 * TILESIZE, 10.1 * TILESIZE)))
        self.slots.append(InventorySlot("Assets/waterbootsbar.png", (7.4 * TILESIZE, 10.1 * TILESIZE)))

    def update(self):

        self.slots[0].count = self.playerRef.chips
        self.slots[1].count = self.playerRef.gkeys
        self.slots[2].count = self.playerRef.ykeys
        self.slots[3].count = self.playerRef.fboots
        self.slots[4].count = self.playerRef.wboots

    def render(self, dplay):

         dplay.blit(self.image, (2 * TILESIZE, 10 * TILESIZE))

         for slot in self.slots:

             slot.render(dplay)

class InventorySlot:

    def __init__(self, name, pos):
        
        self._layer = UI_LAYER
        self.image = pg.image.load(name)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.font = pg.font.Font("Fonts/MinecraftRegular-Bmg3.otf", 18)
        self.count = 0

    def render(self, dplay):

        dplay.blit(self.image, self.rect)
        text = self.font.render(str(self.count), True, (WHITE))
        dplay.blit(text, self.rect.midright)
