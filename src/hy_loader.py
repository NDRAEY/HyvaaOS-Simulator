import os
import pygame
import hy_tty

import sys

sys.path.insert(0, "..")
sys.path.insert(0, ".")

from system.stage2 import Stage2

class Loader:
    def __init__(self, sim):
        self.sim = sim

        self.tty = hy_tty.TTY(sim.screen, "Monotype", 16)

    def __call__(self, sim, worker):
        # Clear screen

        a: pygame.Surface = self.sim.screen
        a.fill(0, (0, 0, a.get_width(), a.get_height()))

        # Scan filesystem for files.
        path, dirs, files = list(os.walk("system"))[0]

        self.tty.putsf("Filesystem: Built-In\n")
        self.tty.putsf("Files:\n")

        for i in files:
            self.tty.putsf(f"- File: {i} => {os.stat('system/'+i).st_size} bytes\n")
        
        for i in dirs:
            self.tty.putsf(f"- Directory: {i}\n")

        self.tty.putsf("\n")

        if "stage2.py" not in files:
            self.tty.putsf("File `stage2.py` not found!")
            del sim.workers[sim.workers.index(worker)]
            return

        self.tty.putsf("Loading...\n")

        glbs = {}
        locs = {}

        del sim.workers[sim.workers.index(worker)]
        
        stage2 = Stage2(self.sim, self.tty)

