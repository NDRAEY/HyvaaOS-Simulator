import dataclasses
import random

import pygame
from dataclasses import dataclass

import widget

TITLEBAR_HEIGHT = 35

@dataclass
class Window:
    name: str
    widgets: list[widget.Widget]
    on_click: object
    on_hover: object
    
    closable: bool
    has_titlebar: bool

    x: int
    y: int
    width: int
    height: int
    surface: pygame.surface.Surface

    transparent: bool

    def preonclick(self, desktop, event):
        if desktop.winsys.dragging: return
        
        mx, my = event.pos
        
        realx = mx - self.x
        realy = my - self.y

        if realx < 0 or realy < 0:
            return

        if realx > self.width or realy > self.height:
            return
        
        for i in self.widgets:
            widgetx = realx - i.x
            widgety = realy - i.y 

            if widgetx < 0 or widgety < 0:
                continue
            
            if widgetx > i.width or widgety > i.height:
                continue
            
            i.on_click(desktop, event, i)
            return
        
        desktop.app_run_wrapper(None, None, None, lambda: ...)
        self.on_click(desktop, event)

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
    
    def new_window(self, name="Untitled", x=None, y=None, width=100, height=100, titlebar=True, transparent=False):
        print("New window:", name)

        if x is None:
            x = random.randint(100, 450)
        
        if y is None:
            y = random.randint(100, 450)

        if titlebar:
            if y == 0:
                y += 10
        
        self.windows.append(
            Window(
                name,
                [],
                lambda desktop, event: ...,
                lambda desktop, event: ...,

                True,
                titlebar,

                x,
                y,
                width,
                height,

                pygame.surface.Surface((width, height), pygame.SRCALPHA),

                transparent
            )
        )

        self.desktop.external_events.append(
            (pygame.MOUSEBUTTONDOWN, self.windows[-1].preonclick)
        )

        # pygame.draw.rect(self.windows[-1].surface, (0, 0, 255), (0, 0, self.windows[-1].surface.get_width(), self.windows[-1].surface.get_height()))
        self.windows[-1].surface.fill((0, 0, 0))

        return self.windows[-1]

    def render_window(self, window: Window):
        name = window.name[:(window.width + 10) // (22)]

        if name != window.name:
            name += "..."
        
        rendered_name = self.sysfont.render(name, True, (0, 0, 0))

        if window.has_titlebar:
            # Titlebar 
            pygame.draw.rect(
                self.screen,
                (0, 231, 255),
                (window.x, window.y - TITLEBAR_HEIGHT, window.width, TITLEBAR_HEIGHT)
            )

            # Name
            self.screen.blit(
                rendered_name,
                (window.x + 10, ((32 - rendered_name.get_height()) // 2) + window.y - TITLEBAR_HEIGHT)
            )

            if window.closable:
                # Close button
                pygame.draw.rect(
                    self.screen,
                    (255, 0, 0),
                    (window.x + window.width - TITLEBAR_HEIGHT, window.y - TITLEBAR_HEIGHT, TITLEBAR_HEIGHT, TITLEBAR_HEIGHT)
                )

                pygame.draw.line(
                    self.screen,
                    (0, 0, 0),
                    (window.x + window.width - TITLEBAR_HEIGHT + 5, window.y + 5 - TITLEBAR_HEIGHT),
                    (window.x + window.width - 5, window.y - 5),
                    3
                )

                pygame.draw.line(
                    self.screen,
                    (0, 0, 0),
                    (window.x + window.width - 5, window.y + 5 - TITLEBAR_HEIGHT),
                    (window.x + window.width - TITLEBAR_HEIGHT + 5, window.y - 5),
                    3
                )

        window.surface = pygame.transform.scale(
            window.surface,
            (window.width, window.height)
        )

        for i in window.widgets:
            i.render()
        
        # Window content
        self.screen.blit(
            window.surface,
            (window.x, window.y)
        )


    def render_windows(self):
        for i in self.windows:
            if not i.transparent:
                i.surface.fill((64, 64, 64))
            else:
                i.surface.fill((255, 255, 255, 145))


            self.render_window(i)

    def get_win_by_coord(self, x, y):
        for i in self.windows:
            if (i.x <= x <= i.x + i.width and
                    i.y <= y <= i.y + i.height):
                return i

    def get_titlebar_win_by_coord(self, x, y):
        for i in self.windows:
            if (i.x <= x <= i.x + i.width and
                    i.y - TITLEBAR_HEIGHT <= y <= i.y):
                return i

    def get_closebtn_win_by_coord(self, x, y):
        win = self.get_titlebar_win_by_coord(x, y)

        relp = win.x - (x - win.width)

        if 0 <= relp <= TITLEBAR_HEIGHT and win.closable and win.has_titlebar:
            return win

    def get_window_by_name(self, name: str):
        for i in self.windows:
            if i.name == name:
                return i

    def delete_window_by_name(self, name: str):
        if (win := self.get_window_by_name("ctxmenu")):
            del self.windows[self.windows.index(win)]

            return True

    def create_file(self, desktop, event, widget: widget.Button):
        self.delete_window_by_name("ctxmenu")

        with open("New File.txt", "wb") as file:
            file.close()

    def create_context_menu_for_desktop(self, x, y):
        win = self.new_window("ctxmenu", x, y, 160, 50, False)

        button = widget.Button(win, "New file", 5, 5, 150, 40, (166, 166, 166))
        button.on_click = self.create_file

        win.widgets.append(button)

    def up_action(self, desktop, event: pygame.event.Event):
        if event.button == 3:
            if self.get_win_by_coord(*event.pos):
                return

            if self.delete_window_by_name("ctxmenu"):
                return

            self.create_context_menu_for_desktop(*event.pos)
            return

        self.dragging = None

    def down_action(self, desktop, event):
        x, y = event.pos

        win = self.get_titlebar_win_by_coord(x, y)

        if win:
            subwin = self.get_closebtn_win_by_coord(x, y)

            if subwin:
                del self.windows[self.windows.index(subwin)]
            elif win.has_titlebar:
                self.dragging = win
                self.dcoords = win.x - x, win.y - y
        else:
            win = self.get_win_by_coord(x, y)

            if win and win.on_click:
                win.on_click(self, event)

    def move_action(self, desktop, event):
        if self.dragging:
            self.dragging.x = event.pos[0] + self.dcoords[0]
            self.dragging.y = event.pos[1] + self.dcoords[1]