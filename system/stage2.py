from dataclasses import dataclass

class Stage2:
    def __init__(self, sim, tty):
        self.sim = sim
        self.tty = tty

        self.tty.putsf("Stage 2!\n")
        
        self.start()

    def exec_extern(self, filename):
        with open(filename, "r") as f:
            exec(f.read(), globals())

    def start(self):
        self.exec_extern("system/desktop/riolu_desktop.py")

        desktop = Desktop(self.sim, self.tty)

        desktop.start()