import lucario_fs
import pygame
import hy_tty

class Loader:
    def __init__(self, sim, file):
        self.filename = file
        self.fd = open(self.filename, "rb")

        self.sim = sim

        self.fs = lucario_fs.LucarioFS(self.fd)
        self.tty = hy_tty.TTY(sim.screen, "Monotype", 16)

    def __call__(self, sim, worker):
        # Clear screen

        a: pygame.Surface = self.sim.screen
        a.fill(0, (0, 0, a.get_width(), a.get_height()))

        # Scan filesystem for files.
        filecount, files = self.fs.get_file_table()

        self.tty.putsf("Filesystem: LucarioFS\n")
        self.tty.putsf(f"Filesystem max file count: {filecount}\n")
        self.tty.putsf("Files:\n")

        for i in files:
            self.tty.putsf(f"- File: {i.name} => {i.real_size} bytes\n")

        self.tty.putsf("\n")

        filenames = [i.name for i in files]

        if "stage2.py" not in filenames:
            self.tty.putsf("File `stage2.py` not found!")
            del sim.workers[sim.workers.index(worker)]
            return

        self.tty.putsf("Loading...\n")

        glbs = {}
        locs = {}

        tmp = self.fs.read_file("stage2.py").decode("utf-8")
        tmp = exec(tmp, glbs, locs)

        Stage2 = locs['Stage2']

        stage2 = Stage2(self.sim, self.fs, self.tty)

        del sim.workers[sim.workers.index(worker)]
