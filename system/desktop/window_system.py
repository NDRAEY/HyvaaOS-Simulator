import pygame
from dataclasses import dataclass

TITLEBAR_HEIGHT = 35

@dataclass
class Window:
    name: str
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
    def __init__(self, desktop):
        self.windows: list[Window] = []
        self.desktop = desktop

        self.desktop.external_events.append((pygame.MOUSEBUTTONUP, self.up_action))
        self.desktop.external_events.append((pygame.MOUSEBUTTONDOWN, self.down_action))
        self.desktop.external_events.append((pygame.MOUSEMOTION, self.move_action))

        self.sysfont = pygame.font.Font("./res/JetBrains.ttf", 16)

        self.screen: pygame.surface.Surface = desktop.screen

        self.dragging = None
        self.dcoords = None
    
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

        # Canvas
        pygame.draw.rect(
            self.screen,
            (67, 231, 33),
            (window.x, window.y, window.width, window.height)
        )

        # Name
        self.screen.blit(
            rendered_name,
            (window.x + 10, ((32 - rendered_name.get_height()) // 2) + window.y)
        )

        if window.closable:
            # Close button
            pygame.draw.rect(
                self.screen,
                (255, 0, 0),
                (window.x + window.width - TITLEBAR_HEIGHT, window.y, TITLEBAR_HEIGHT, TITLEBAR_HEIGHT)
            )

            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (window.x + window.width - TITLEBAR_HEIGHT + 5, window.y + 5),
                (window.x + window.width - 5, window.y + TITLEBAR_HEIGHT - 5),
                3
            )

            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                (window.x + window.width - 5, window.y + 5),
                (window.x + window.width - TITLEBAR_HEIGHT + 5, window.y + TITLEBAR_HEIGHT - 5),
                3
            )

        # Titlebar
        pygame.draw.rect(
            self.screen,
            (0, 128, 128),
            (window.x, window.y + TITLEBAR_HEIGHT, window.width, window.height)
        )

    def render_windows(self):
        for i in self.windows:
            self.render_window(i)

    def get_win_by_coord(self, x, y):
        for i in self.windows:
            if (x >= i.x and
              x <= i.x + i.width and
              y >= i.y and
              y <= i.y + i.height):
                return i

    def get_titlebar_win_by_coord(self, x, y):
        for i in self.windows:
            if (x >= i.x and
              x <= i.x + i.width and
              y >= i.y and
              y <= i.y + TITLEBAR_HEIGHT):
                return i

    def get_closebtn_win_by_coord(self, x, y):
        win = self.get_titlebar_win_by_coord(x, y)

        relp = win.x - (x - win.width)

        if relp >= 0 and relp <= TITLEBAR_HEIGHT:
            return win

    def up_action(self, desktop, event: pygame.event.Event):
        self.dragging = None
        self.drag_start = None

    def down_action(self, desktop, event):
        x, y = event.pos

        win = self.get_titlebar_win_by_coord(x, y)

        if win:
            clsbtn = self.get_closebtn_win_by_coord(x, y)

            if clsbtn:
                del self.windows[self.windows.index(clsbtn)]
            else:
                self.dragging = win
                self.dcoords = win.x - x, win.y - y

    def move_action(self, desktop, event):
        if self.dragging:
            self.dragging.x = event.pos[0] + self.dcoords[0]
            self.dragging.y = event.pos[1] + self.dcoords[1]