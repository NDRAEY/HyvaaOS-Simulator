import pygame

class TTY:
    def __init__(self, sfc: pygame.Surface, fontname: str = None, fontsize = 18):
        self.x = 0
        self.y = 0
        self.color = (255, 255, 255)

        self.size = fontsize

        self.font = pygame.font.SysFont(fontname, self.size)
        self.surface = sfc

    def putchar(self, char):
        ch = self.font.render(char[0], True, self.color)
        
        if char == "\n":
            self.y += ch.get_height()
            self.x = 0
            return

        if self.x > self.surface.get_width():
            self.y += ch.get_height()
            self.x = 0

        if self.y > self.surface.get_height() - ch.get_height():
            self.surface.blit(self.surface, (0, -ch.get_height()))
            pygame.draw.rect(self.surface, (0, 0, 0), (
                0,
                self.surface.get_height() - ch.get_height(),
                self.surface.get_width(),
                ch.get_height()
            ))

            self.y -= ch.get_height()

        self.surface.blit(ch, (self.x, self.y))

        self.x += ch.get_width()
    
    def puts(self, string):
        for i in string:
            self.putchar(i)

    def putsf(self, string):
        self.puts(string)
        pygame.display.flip()