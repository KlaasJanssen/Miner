import pygame

pygame.init()
font = pygame.font.Font(None,30)

def debug(text, x = 10, y = 10):
    text_surface = font.render(str(text), True, "white")
    text_rect = text_surface.get_rect(topleft = (x,y))
    screen = pygame.display.get_surface()
    pygame.draw.rect(screen, "black", text_rect)
    screen.blit(text_surface, text_rect)
