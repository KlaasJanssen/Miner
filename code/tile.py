import pygame
from settings import *

class Tile(pygame.sprite.Sprite):
    def __init__(self, pos, type, level_surface, groups, surface = pygame.Surface((TILE_SIZE, TILE_SIZE))):
        super().__init__(groups)
        self.level_surface = level_surface
        self.pos = pygame.math.Vector2(pos)
        self.type = type
        self.drop = tile_data[self.type]["drop"]
        self.drop_amount = tile_data[self.type]["drop_amount"]

        #self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))\
        self.image = surface.copy()

        self.rect = self.image.get_rect(topleft = self.pos)
        self.vertical_mine_hitbox = pygame.Rect(0,0,TILE_SIZE // 1.5,16)
        self.horizontal_mine_hitbox = pygame.Rect(0,0,16,TILE_SIZE // 1.5)
        self.vertical_mine_hitbox.center = self.rect.center
        self.horizontal_mine_hitbox.center = self.rect.center

        self.level_surface.blit(self.image, pos)

    def mine_tile(self):
        self.image.fill(MINE_BACKGROUND_COLOR)
        self.level_surface.blit(self.image, self.pos)
        self.kill()
