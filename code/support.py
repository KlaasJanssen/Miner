import pygame
from os import walk

def import_folder(path):
    image_dict = {}
    for _,__,image_files in walk(path):
        for image in image_files:
            key = image.split('.png')[0]
            full_path = path + "/" + image
            image_dict[key] = pygame.image.load(full_path).convert_alpha()
    return image_dict
