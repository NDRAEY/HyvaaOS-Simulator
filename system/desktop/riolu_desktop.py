import pygame
import io

import toml

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

        pygame.mouse.set_visible(False)

    def start(self):
        self.sim.workers.append(self.render)
        self.sim.handlers.append(self.input_handler)

    def render(self, sim, worker):
        self.screen.blit(
            self.background,
            (0, 0)
        )

        self.draw_cursor()

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
        else:
            for i in self.external_events:
                ev, fn = i

                if ev == event.type:
                    fn(self, event)