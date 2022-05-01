import pygame
from settings import *
from random import random
from tile import Tile
from player import Player
from support import import_folder

class Level:
    def __init__(self, ID):
        self.display_surface = pygame.display.get_surface()
        self.ID = ID

        self.level_surface = pygame.Surface((MAP_BLOCK_WIDTH*TILE_SIZE, MAP_BLOCK_HEIGHT*TILE_SIZE))
        self.tiles = TileGroup()
        self.tile_surfaces = import_folder("../graphics/tile")

        self.create_map()

        self.visible_sprites = CameraGroup(self.ID, self.level_surface)
        self.player = Player([self.visible_sprites])



    def create_map(self):
        for i in range(MAP_BLOCK_WIDTH):
            for j in range(MAP_BLOCK_HEIGHT):
                if j == 0:
                    type = "grass"
                else:
                    r = random()
                    if r < 0.05:
                        type = "coal"
                    elif r < 0.07:
                        type = "iron"
                    else:
                        type = "dirt"


                x = i * TILE_SIZE
                y = j * TILE_SIZE

                surface = self.tile_surfaces[type]
                Tile((x,y), type, self.level_surface, [self.tiles], surface)

    def run(self,dt):
        self.visible_sprites.draw(self.player)
        self.visible_sprites.update(self.tiles, dt)



class CameraGroup(pygame.sprite.Group):
    def __init__(self, ID, level_surface):
        super().__init__()
        self.ID = ID
        self.level_surface = level_surface

        self.display_surface = pygame.display.get_surface()
        self.left_lim = LEFT_LIMIT
        self.right_lim = RIGHT_LIMIT - WIDTH
        self.up_lim = UP_LIMIT
        self.down_lim = DOWN_LIMIT - HEIGHT

    def draw(self, player):
        self.offset = pygame.math.Vector2()
        self.offset.x = player.rect.centerx - WIDTH // 2
        self.offset.y = player.rect.centery - HEIGHT // 2 #+ 4*TILE_SIZE

        if self.offset.x <= self.left_lim:
            self.offset.x = self.left_lim
        elif self.offset.x > self.right_lim:
            self.offset.x = self.right_lim

        if self.offset.y < self.up_lim:
            self.offset.y = self.up_lim
        elif self.offset.y > self.down_lim:
            self.offset.y = self.down_lim

        self.display_surface.blit(self.level_surface, - self.offset)

        for sprite in self.sprites():
            self.display_surface.blit(sprite.image, sprite.rect.topleft - self.offset)

class TileGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

    def get_near_tiles(self, player):
        nearby_sprites = []
        for sprite in self.sprites():
            if abs(sprite.rect.centerx - player.rect.centerx) < TILE_SIZE * 3 or abs(sprite.rect.centery - player.rect.centery) < TILE_SIZE * 3:
                nearby_sprites.append(sprite)
        return nearby_sprites
