import sys

sys.path.insert(0, "./system/desktop")

import pygame
import toml

import widget

import window_system

class Desktop:
    def __init__(self, sim, tty):
        self.sim = sim
        self.tty = tty

        self.screen: pygame.surface.Surface = self.tty.surface

        self.external_events = []

        self.mouse_coords = (
            self.screen.get_width() / 2,
            self.screen.get_height() / 2,
        )

        self.config = toml.load("config.toml")

        self.background = pygame.image.load(self.config['desktop']['background'])
        self.cursor_sfc = pygame.image.load(self.config['desktop']['cursor'])

        self.external_events.append(
            (pygame.KEYDOWN, self.exit_handler)
        )

        self.background = pygame.transform.scale(self.background, (
            self.screen.get_width(),
            self.screen.get_height(),
        ))

        self.winsys = window_system.WindowSystem(self)

        window = self.winsys.new_window("Lucario", 150, 150, 600)
        window.widgets.append(widget.Button(window, "HELLO WORLD", 10, 10))

    def start(self):
        self.sim.workers.append(self.render)
        self.sim.handlers.append(self.input_handler)

    def render(self, sim, worker):
        self.screen.blit(
            self.background,
            (0, 0)
        )

        self.winsys.render_windows()

        self.draw_cursor()

        # self.winsys.windows[0].widgets[0].width += 1

        pygame.display.flip()

    def draw_cursor(self):
        self.screen.blit(
            self.cursor_sfc,
            self.mouse_coords
        )

    def exit_handler(self, sim, event: pygame.event.Event):
        if event.key == pygame.K_ESCAPE and pygame.key.get_mods() & pygame.KMOD_SHIFT:
            self.sim.quit()

    def input_handler(self, sim, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self.mouse_coords = event.pos

        for i in self.external_events:
            ev, fn = i

            if ev == event.type:
                fn(self, event)