import pygame as pg
import sys
import pytmx

from os import path
from config import *
from sprites import *
from tilemap import *

pg.init()
dplay = pg.display.set_mode((WIDTH, HEIGHT))
UI = UserInterface(Player)
    
class Game:

    def __init__(self):

        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption("Chip's Challenge")
        self.clock = pg.time.Clock()
        self.load_data()

    def load_data(self):

        game_folder = path.dirname(__file__)
        assets_folder = path.join(game_folder, 'Assets')
        map_folder = path.join(game_folder, 'Maps')
        self.map = TiledMap(path.join(map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()
        self.player_img = pg.image.load(path.join(assets_folder, PLAYER_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(assets_folder, WALL_IMG)).convert_alpha()

        self.item_images = {}
        
        for item in ITEM_IMAGES:

            self.item_images[item] = pg.image.load(path.join(assets_folder, ITEM_IMAGES[item])).convert_alpha()     
        
    def new(self):
        
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.items = pg.sprite.Group()

        for tile_object in self.map.tmxdata.objects:

            if tile_object.name == 'player':
                self.player = Player(self, tile_object.x/TILESIZE, tile_object.y/TILESIZE)

            if tile_object.name == 'walls':
                Obstacle(self, tile_object.x/TILESIZE, tile_object.y/TILESIZE)

            if tile_object.name in ['gkey']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name in ['ykey']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name in ['fboots']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name in ['wboots']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name in ['fire']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name in ['water']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name in ['ggate']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

            if tile_object.name in ['ygate']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)
                
            if tile_object.name in ['chip']:
                Item(self, tile_object.x, tile_object.y, tile_object.name)

        self.camera = Camera(self.map.width, self.map.height)

    def run(self):
        
        self.playing = True

        while self.playing:

            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.update()
            self.draw()

    def quit(self):

        pg.quit()
        sys.exit()

    def update(self):
        
        self.all_sprites.update()
        self.camera.update(self.player)

        hits = pg.sprite.spritecollide(self.player, self.items, False)

        for hit in hits:
            
            if hit.type == 'gkey':
                hit.kill()

            if hit.type == 'ykey':
                hit.kill()

            if hit.type == 'fboots':
                hit.kill()

            if hit.type == 'wboots':
                hit.kill()

            if hit.type == 'fire':
                self.quit()

            if hit.type == 'water':
                self.quit()

            if hit.type == 'ggate':
                hit.kill()

            if hit.type == 'ygate':
                hit.kill()

            if hit.type == 'chip':
                hit.kill()

    def draw(self):

        self.screen.blit(self.map_img, self.camera.apply_rect(self.map_rect))

        for sprite in self.all_sprites:

            self.screen.blit(sprite.image, self.camera.apply(sprite))

        UI.render(dplay)
            
        pg.display.flip()

    def events(self):
        
        for event in pg.event.get():

            if event.type == pg.QUIT:

                self.quit()
                
            if event.type == pg.KEYDOWN:

                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT or event.key == pg.K_a:
                    self.player.move(dx = -1)
                if event.key == pg.K_RIGHT or event.key == pg.K_d:
                    self.player.move(dx = 1)
                if event.key == pg.K_UP or event.key == pg.K_w:
                    self.player.move(dy = -1)
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    self.player.move(dy = 1)

g = Game()
while True:
    g.new()
    g.run()
