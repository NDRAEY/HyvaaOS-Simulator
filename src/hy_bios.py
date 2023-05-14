import os

import pygame
import hy_tty

import hy_loader

class BIOS:
    def __init__(self, sim):
        self.tty = hy_tty.TTY(sim.screen, "Monotype", 18)
        self.logo = pygame.image.load("res/bios.png")
        
    def __call__(self, sim, worker):
        self.tty.puts("LirBIOS v1.0 by NDRAEY\n")
        sim.screen.blit(self.logo, (
            (sim.screen.get_width() - self.logo.get_width()) // 2, 
            (sim.screen.get_height() - self.logo.get_height()) // 2
        ))
        pygame.display.flip()

        self.tty.putsf("Loading from DEV!CD0:// - ")

        pygame.time.wait(500)

        self.tty.putsf("OKAY\n")

        self.tty.putsf("Booting...")
        
        pygame.time.wait(1000)

        del sim.workers[sim.workers.index(worker)]

        sim.workers.append(hy_loader.Loader(sim, "system.img"))
