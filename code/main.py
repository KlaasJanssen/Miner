import pygame, sys, time
from settings import *
from level import Level
from debug import debug

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.previous_time = time.perf_counter()

        # Level Data
        self.levels = {}
        self.levels[0] = Level(0)
        self.active_level = 0

    def run(self):
        while True:
            # Delta time
            current_time = time.perf_counter()
            dt = current_time - self.previous_time
            self.previous_time = current_time
            

            # Event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.screen.fill("lightblue")
            self.levels[self.active_level].run(dt)
            debug(dt)
            pygame.display.update()
            #self.clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
