import pygame
from dataclasses import dataclass

@dataclass
class Window:
    name: str | None
    widgets: list
    on_click: object
    on_hover: object
    
    closable: bool
    maximizable: bool

    x: int
    y: int

    width: int
    height: int

class WindowSystem:
    def __init__(self, screen: pygame.Surface):
        self.windows = []

        self.sysfont = pygame.font.Font("./res/JetBrains.ttf", 16)

        self.screen = screen
    
    def new_window(self, name="Untitled", x=0, y=0, width=100, height=100):
        self.windows.append(
            Window(
                name,
                [],
                lambda: ...,
                lambda: ...,

                True,
                True,

                x,
                y,
                width,
                height
            )
        )
    
    def render_window(self, window: Window):
        name = window.name  # [:(window.width + 10) // (22)]

        if name != window.name:
            name += "..."
        
        rendered_name = self.sysfont.render(name, True, (0, 0, 0))

        pygame.draw.rect(
            self.screen,
            (67, 231, 33),
            (window.x, window.y, window.width, window.height)
        )

        self.screen.blit(
            rendered_name,
            (window.x + 10, ((32 - rendered_name.get_height()) // 2) + window.y)
        )

        if window.closable:
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                (window.x + window.width - 32, window.y, 32, 32)
            )

        pygame.draw.rect(
            self.screen,
            (0, 128, 128),
            (window.x, window.y + 32, window.width, window.height)
        )

    def render_windows(self):
        for i in self.windows:
            self.render_window(i)