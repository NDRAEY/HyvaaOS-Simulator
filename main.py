import pygame

pygame.init()

class Simulator:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("HyvaaOS")

        self.handlers = []
        self.workers = []

        self.clock = pygame.time.Clock()

    def step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            else:
                for i in self.handlers:
                    i(self, event)
                
                print("Other event:", event.type)

    def run(self):
        while True:
            self.step()
            
            for i in self.workers:
                i(self, i)

            self.clock.tick(60)

if __name__ == "__main__":
    import hy_bios

    sim = Simulator()
    
    sim.workers.append(hy_bios.BIOS(sim))
    sim.run()