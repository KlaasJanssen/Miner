import pygame
from settings import *
from debug import debug
from support import import_folder
from ui import UI
from inventory import Inventory

class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.Surface((TILE_SIZE - 8, TILE_SIZE - 8))
        self.image.fill("white")
        self.rect = self.image.get_rect(midbottom = (MAP_BLOCK_WIDTH*TILE_SIZE/2, 0))

        self.pos = pygame.math.Vector2(self.rect.topleft)
        self.speed = 500
        self.direction = pygame.math.Vector2()

        self.gravity = 1000
        self.fall_velocity = 0
        self.max_fall_velocity = 2000

        self.on_ground = True
        self.drilling = False

        self.drill_duration = 1000
        self.drill_time = self.drill_duration
        self.drill_direction = None

        self.images = import_folder("../graphics/player")
        self.last_direction = "left"
        self.down_mine_delay = 0

        # UI
        self.max_health = 200
        self.health = self.max_health
        self.max_fuel = 20
        self.fuel = self.max_fuel
        self.inventory_manager = Inventory(self)
        self.ui = UI(self)

    def input(self):
        if not self.drilling:
            keys = pygame.key.get_pressed()
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and not (keys[pygame.K_RIGHT] or keys[pygame.K_d]):
                self.direction.x = -1
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and not (keys[pygame.K_LEFT] or keys[pygame.K_a]):
                self.direction.x = 1
            else:
                self.direction.x = 0

            # if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and not (keys[pygame.K_UP] or keys[pygame.K_w]):
            #     self.direction.y = 1
            if (keys[pygame.K_UP] or keys[pygame.K_w]) and not (keys[pygame.K_DOWN] or keys[pygame.K_s]):
                self.direction.y = -1
                self.fall_velocity = 0
                self.on_ground = False
            else:
                self.direction.y = 0

    def move(self, tiles, dt):
        if not self.drilling:
            if self.direction.magnitude() != 0:
                self.direction = self.direction.normalize()

            self.nearby_tiles = tiles.get_near_tiles(self)

            self.pos.x += self.direction.x * self.speed * dt
            self.rect.x = round(self.pos.x)
            self.collision(self.nearby_tiles, "horizontal", dt)

            self.apply_gravity(dt)
            self.on_ground = False
            self.pos.y += (self.direction.y * self.speed + self.fall_velocity) * dt
            self.rect.y = round(self.pos.y)
            self.collision(self.nearby_tiles, "vertical", dt)

            #debug(self.on_ground)

    def apply_gravity(self, dt):
        self.fall_velocity += self.gravity * dt
        if self.fall_velocity >= self.max_fall_velocity:
            self.fall_velocity = self.max_fall_velocity

    def collision(self, tiles, direction, dt):
        if direction == "horizontal":
            if self.rect.left < LEFT_LIMIT:
                self.rect.left = LEFT_LIMIT
                self.pos.x = self.rect.x
            elif self.rect.right > RIGHT_LIMIT:
                self.rect.right = RIGHT_LIMIT
                self.pos.x = self.rect.x

            for tile in tiles:
                if tile.rect.colliderect(self.rect):
                    if self.direction.x > 0:
                        self.rect.right = tile.rect.left
                    else:
                        self.rect.left = tile.rect.right
                    self.pos.x = self.rect.x

        if direction == "vertical":
            if self.rect.top < UP_LIMIT:
                self.rect.top = UP_LIMIT
                self.pos.y = self.rect.top
            elif self.rect.bottom > DOWN_LIMIT:
                self.rect.bottom = DOWN_LIMIT
                self.pos.y = self.rect.y
                self.on_ground = True

            for tile in tiles:
                if tile.rect.colliderect(self.rect):
                    if (self.direction.y * self.speed + self.fall_velocity) > 0:
                        self.fall_velocity = 0
                        self.rect.bottom = tile.rect.y
                        self.on_ground = True
                    else:
                        self.rect.top = tile.rect.bottom
                    self.pos.y = self.rect.y

    def mine_block(self):
        if not self.drilling:
            keys = pygame.key.get_pressed()
            if self.on_ground:
                if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                    for tile in self.nearby_tiles:
                        if tile.vertical_mine_hitbox.collidepoint(self.rect.center + pygame.math.Vector2(0,TILE_SIZE)):
                            self.drill_block(tile)
                            self.drill_direction = "down"

                elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    for tile in self.nearby_tiles:
                        if tile.horizontal_mine_hitbox.collidepoint(self.rect.center + pygame.math.Vector2(-TILE_SIZE,0)):
                            self.drill_block(tile)
                            self.drill_direction = "left"

                elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    for tile in self.nearby_tiles:
                        if tile.horizontal_mine_hitbox.collidepoint(self.rect.center + pygame.math.Vector2(TILE_SIZE,0)):
                            self.drill_block(tile)
                            self.drill_direction = "right"



    def drill_block(self, tile):
        self.start_pos = pygame.math.Vector2(self.rect.center)
        self.end_pos = pygame.math.Vector2(tile.rect.center)
        self.end_pos.y += 4
        self.drill_vector = self.end_pos - self.start_pos
        self.drilling = True
        self.drill_time = self.drill_duration
        self.mined_tile = tile

    def drill_move(self, dt):
        if self.drilling:
            self.pos += self.drill_vector * (dt*1000 / self.drill_duration)
            self.rect.topleft = self.pos
            self.drill_time -= dt*1000
            if self.drill_time <= 0:
                self.drilling = False
                self.inventory_manager.add_item(self.mined_tile.drop, self.mined_tile.drop_amount)
                self.mined_tile.mine_tile()
                self.down_mine_delay = 50

    def set_image(self, dt):
        if self.direction.x < 0:
            img_direction = "left"
        elif self.direction.x > 0:
            img_direction = "right"
        else:
            img_direction = self.last_direction
        self.last_direction = img_direction

        if (self.drilling or self.down_mine_delay > 0) and self.drill_direction == "down":
            if self.down_mine_delay > 0:
                self.down_mine_delay -= dt * 1000
            img_direction = f"down_{img_direction}"

        self.image = self.images[img_direction]


    def update(self, tiles, dt):
        self.input()
        self.move(tiles, dt)
        self.mine_block()
        self.drill_move(dt)
        self.set_image(dt)
        self.inventory_manager.toggle_inventory()
        self.inventory_manager.draw_inventory()
