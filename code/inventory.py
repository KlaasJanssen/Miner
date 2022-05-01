import pygame
from settings import *
from support import import_folder
from debug import debug

class Inventory:
    def __init__(self, player):
        self.display_surface = pygame.display.get_surface()
        self.player = player
        self.slots = PLAYER_INV_SLOTS
        self.inventory = {}

        self.tile_surfaces = import_folder("../graphics/tile")
        self.font = pygame.font.Font(None, 40)
        self.display_inventory = False
        self.e_pressed = False
        self.r_pressed = False

        for i in range(self.slots):
            self.inventory[i] = {"item": None, "number": 0}

        self.create_inventory_surface()

    def add_item(self, item, amount):
        for slot in self.inventory.values():
            if slot["item"] == item:
                slot["number"] += amount
                self.create_inventory_surface()
                return True

        for slot in self.inventory.values():
            if slot["item"] == None:
                slot["item"] = item
                slot["number"] += amount
                self.create_inventory_surface()
                return True

        return False

    def remove_item(self, item, amount):
        old_inventory = {}
        for key, value in self.inventory.items():
            old_inventory[key] = {**value}

        for slot in self.inventory.values():
            if slot["item"] == item:
                if slot["number"] >= amount:
                    slot["number"] -= amount
                    if slot["number"] == 0:
                        slot["item"] = None
                    self.create_inventory_surface()
                    return True
                else:
                    amount -= slot["number"]
                    slot["item"] = None
                    slot["number"] = 0

        self.inventory = old_inventory
        return False

    def clear_inventory(self):
        self.inventory = {}
        for i in range(self.slots):
            self.inventory[i] = {"item": None, "number": 0}
        self.create_inventory_surface()

    def create_inventory_surface(self):
        if self.slots > 9:
            row_slots = 5
        elif self.slots > 7:
            row_slots = 4
        elif self.slots > 4:
            row_slots = 3
        else:
            row_slots = 2

        nrow = (self.slots - 1) // row_slots + 1
        self.inv_surface = pygame.Surface((INV_TILE_SIZE * row_slots, INV_TILE_SIZE * nrow), pygame.SRCALPHA).convert_alpha()
        self.inv_rect = self.inv_surface.get_rect(midbottom = (WIDTH // 2, HEIGHT  - 40))

        for i in range(nrow):
            for j in range(row_slots):
                if (i * row_slots + j) < self.slots:
                    slot_surf = pygame.Surface((INV_TILE_SIZE, INV_TILE_SIZE))
                    slot_surf.fill("#5c5652")
                    slot_rect = slot_surf.get_rect(topleft = (j * INV_TILE_SIZE, i * INV_TILE_SIZE))
                    slot = i*row_slots + j
                    if self.inventory[slot]["item"] != None:
                        item_surf = self.tile_surfaces[self.inventory[slot]["item"]]
                        item_rect = item_surf.get_rect(center = (INV_TILE_SIZE // 2, INV_TILE_SIZE // 2))
                        slot_surf.blit(item_surf, item_rect)
                        number_surf = self.font.render(str(self.inventory[slot]["number"]), True, (255,255,255))
                        number_rect = number_surf.get_rect(bottomright = (INV_TILE_SIZE * (13/16), INV_TILE_SIZE * (13/16)))
                        slot_surf.blit(number_surf, number_rect)

                    self.inv_surface.blit(slot_surf, slot_rect)
                    pygame.draw.rect(self.inv_surface, (255,255,255), slot_rect, 2)


    def draw_inventory(self):
        if self.display_inventory:
            self.display_surface.blit(self.inv_surface, self.inv_rect)
        
    def toggle_inventory(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            if not self.e_pressed:
                self.display_inventory = not self.display_inventory
                self.e_pressed = True
        else:
            self.e_pressed = False

        if keys[pygame.K_r]:
            if not self.r_pressed:
                self.inventory[self.slots] = {"item": None, "number": 0}
                self.slots += 1
                self.create_inventory_surface()
                self.r_pressed = True
        else:
            self.r_pressed = False

        




