import os
import sys

sys.path.insert(0, "./system/desktop")

import pygame
import toml

import widget
import datetime

import window_system

from calculator import Calculator
from subprocess import run

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
        
        self.taskbar = self.winsys.new_window(
            "Titlebar",
            0,
            self.screen.get_height() - 35,
            self.screen.get_width(),
            35,
            titlebar=False
        )

        self.timetext = widget.Label(
            self.taskbar,
            "HELLO WORLD",
            0,
            0
        )

        self.menubtn = widget.Button(
            self.taskbar,
            "Menu",
            10,
            5,
            60,
            25,
            (198, 45, 77)
        )

        self.menubtn.on_click = self.add_apps_window

        self.timetext.x = (self.taskbar.width - self.timetext.render_text().get_width())
        self.timetext.y = (self.taskbar.height - self.timetext.render_text().get_height()) // 2

        self.taskbar.widgets.append(self.menubtn)
        self.taskbar.widgets.append(self.timetext)

        self.fileswin = self.winsys.new_window("AAAA", self.screen.get_width() - 210, 10, 200, 300, False, True)

    def run_file(self, name):
        print(os.name)
        if os.name.startswith("linux") or os.name.startswith("posix"):
            run(["xdg-open", name])
        else:
            run("start " + name, shell=True)
    
    def create_file_icon(self, window, icon="res/file.png", name="Unnamed File", addto=None, xpos=5, ypos=5):
        btn = widget.Image(window, icon, xpos, ypos, 48, 48)
        txt = widget.Label(window, name, xpos, ypos, fontsize=14)

        btn.on_click = lambda _, __, ___: print("BUTTON")
        txt.on_click = lambda _, __, ___: self.run_file(___.text)

        group = widget.HorizontalAutoArrangeableGroup(window, btn, txt)

        if addto is not None:
            addto.append(group)
        else:
            window.widgets.append(group)

        return group

    def start(self):
        self.sim.workers.append(self.render)
        self.sim.handlers.append(self.input_handler)

    def render(self, sim, worker):
        self.screen.blit(
            self.background,
            (0, 0)
        )

        self.timetext.text = f"{datetime.datetime.now().strftime('%H:%M:%S')}"

        self.winsys.render_windows()

        self.fileswin.widgets.clear()
        ypos = 5

        for i in list(os.walk("."))[0][-1]:
            self.create_file_icon(self.fileswin, name=i, ypos=ypos)
            ypos += 56

        self.fileswin.height = ypos + 5

        self.draw_cursor()

        pygame.display.flip()

    def draw_cursor(self):
        self.screen.blit(
            self.cursor_sfc,
            self.mouse_coords
        )

    def add_apps_window(self, desktop, event, widget_):
        if self.app_run_wrapper(None, None, None, lambda: ...):
            return

        apps = self.winsys.new_window("apps_panel", 0, self.screen.get_height() - 200 - 35, 200, 200, False)

        calcapp = widget.Button(apps, "Calculator", 10, 10)
        calcapp.on_click = lambda _, __, ___: self.app_run_wrapper(_, __, ___, lambda: Calculator(self.winsys))

        exitbtn = widget.Button(apps, "Exit", 10, 60, color=(255, 0, 0))
        exitbtn.on_click = lambda desktop_, __, ___: desktop_.sim.quit()

        apps.widgets.append(calcapp)
        apps.widgets.append(exitbtn)

    def app_run_wrapper(self, desktop, event, widget_, fn):
        panwin = self.winsys.get_window_by_name("apps_panel")
        ctxwin = self.winsys.get_window_by_name("ctxmenu")

        if panwin:
            del self.winsys.windows[self.winsys.windows.index(panwin)]
        
        if ctxwin:
            del self.winsys.windows[self.winsys.windows.index(ctxwin)]

        if panwin or ctxwin:
            fn()

            return True

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